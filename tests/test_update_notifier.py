#!/usr/bin/env python3
"""
Tests for SVG Maestro Version Checker and Update Notifier (scripts/update_notifier.py).
Validates SemVer comparisons, 24-hour file caching, graceful network failure handling,
banner formatting, and CLI integration.
"""

import os
import sys
import json
import time
import unittest
from unittest.mock import patch, MagicMock
import urllib.error

# Setup sys.path
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TESTS_DIR, ".."))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")

if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from update_notifier import (
    parse_version,
    compare_versions,
    is_newer_version,
    get_current_version,
    load_cache,
    save_cache,
    fetch_latest_release_from_github,
    check_for_updates,
    format_update_banner,
    DEFAULT_REPO,
    CACHE_TTL_SECONDS
)


class TestSemverComparison(unittest.TestCase):
    """Unit tests for semantic version parsing and comparison."""

    def test_parse_standard_version(self):
        base, prerelease = parse_version("0.1.0")
        self.assertEqual(base, (0, 1, 0))
        self.assertIsNone(prerelease)

    def test_parse_version_with_v_prefix(self):
        base, prerelease = parse_version("v1.2.3")
        self.assertEqual(base, (1, 2, 3))
        self.assertIsNone(prerelease)

    def test_parse_prerelease_version(self):
        base, prerelease = parse_version("0.1.0-beta.1")
        self.assertEqual(base, (0, 1, 0))
        self.assertEqual(prerelease, ("beta", 1))

    def test_compare_major_minor_patch(self):
        self.assertEqual(compare_versions("0.2.0", "0.1.0"), 1)
        self.assertEqual(compare_versions("0.1.0", "0.2.0"), -1)
        self.assertEqual(compare_versions("1.0.0", "0.9.9"), 1)
        self.assertEqual(compare_versions("0.1.1", "0.1.0"), 1)
        self.assertEqual(compare_versions("0.1.0", "0.1.0"), 0)

    def test_compare_prereleases(self):
        # 0.1.0 is newer than 0.1.0-beta.1
        self.assertEqual(compare_versions("0.1.0", "0.1.0-beta.1"), 1)
        self.assertEqual(compare_versions("0.1.0-beta.1", "0.1.0"), -1)
        # beta.2 is newer than beta.1
        self.assertEqual(compare_versions("0.1.0-beta.2", "0.1.0-beta.1"), 1)
        # higher base version beats pre-release of higher base
        self.assertEqual(compare_versions("0.2.0-beta.1", "0.1.0"), 1)

    def test_is_newer_version(self):
        self.assertTrue(is_newer_version("0.2.0", "0.1.0"))
        self.assertTrue(is_newer_version("v0.2.0", "0.1.0-beta.1"))
        self.assertTrue(is_newer_version("0.1.0", "0.1.0-beta.1"))
        self.assertFalse(is_newer_version("0.1.0-beta.1", "0.1.0-beta.1"))
        self.assertFalse(is_newer_version("0.1.0-beta.1", "0.2.0"))
        self.assertFalse(is_newer_version("0.0.9", "0.1.0"))


class TestGetCurrentVersion(unittest.TestCase):
    """Unit tests for reading version from SKILL.md."""

    def test_reads_version_from_skill_md(self):
        version = get_current_version()
        self.assertTrue(len(version) > 0)
        self.assertIn("0.1.0", version)

    def test_fallback_when_skill_md_missing(self):
        version = get_current_version(skill_path="/nonexistent/path/SKILL.md")
        self.assertEqual(version, "0.1.0-beta.1")


class TestCacheOperations(unittest.TestCase):
    """Unit tests for cache loading and saving."""

    def setUp(self):
        import tempfile
        self.temp_dir = tempfile.mkdtemp()
        self.cache_file = os.path.join(self.temp_dir, ".test_cache.json")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save_and_load_cache(self):
        data = {
            "last_checked": time.time(),
            "latest_version": "0.2.0",
            "release_url": "https://github.com/Tel-BR/svg-maestro/releases/tag/v0.2.0",
            "published_at": "2026-10-16T12:00:00Z"
        }
        success = save_cache(self.cache_file, data)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(self.cache_file))

        loaded = load_cache(self.cache_file)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["latest_version"], "0.2.0")

    def test_load_nonexistent_cache_returns_none(self):
        self.assertIsNone(load_cache("/nonexistent/file.json"))

    def test_load_corrupted_cache_returns_none(self):
        with open(self.cache_file, "w", encoding="utf-8") as f:
            f.write("{invalid json content---")
        self.assertIsNone(load_cache(self.cache_file))


class TestCheckForUpdates(unittest.TestCase):
    """Unit tests for check_for_updates caching, network calls, and resilience."""

    def setUp(self):
        import tempfile
        self.temp_dir = tempfile.mkdtemp()
        self.cache_file = os.path.join(self.temp_dir, ".update_cache.json")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("update_notifier.fetch_latest_release_from_github")
    def test_cache_hit_within_24h_avoids_network(self, mock_fetch):
        # Save cache created 1 hour ago
        cache_data = {
            "last_checked": time.time() - 3600,
            "latest_version": "0.2.0",
            "release_url": "https://github.com/Tel-BR/svg-maestro/releases/tag/v0.2.0",
            "published_at": "2026-10-16T10:00:00Z"
        }
        save_cache(self.cache_file, cache_data)

        result = check_for_updates(
            current_version="0.1.0-beta.1",
            force=False,
            cache_path=self.cache_file
        )

        mock_fetch.assert_not_called()
        self.assertIsNotNone(result)
        self.assertTrue(result["update_available"])
        self.assertTrue(result["cached"])
        self.assertEqual(result["latest_version"], "0.2.0")
        self.assertEqual(result["current_version"], "0.1.0-beta.1")

    @patch("update_notifier.fetch_latest_release_from_github")
    def test_cache_expiration_triggers_network(self, mock_fetch):
        # Save cache created 25 hours ago (> 86400s)
        cache_data = {
            "last_checked": time.time() - (CACHE_TTL_SECONDS + 100),
            "latest_version": "0.1.5",
            "release_url": "https://github.com/Tel-BR/svg-maestro/releases/tag/v0.1.5",
            "published_at": "2026-10-15T08:00:00Z"
        }
        save_cache(self.cache_file, cache_data)

        mock_fetch.return_value = {
            "tag_name": "v0.3.0",
            "html_url": "https://github.com/Tel-BR/svg-maestro/releases/tag/v0.3.0",
            "published_at": "2026-10-16T15:00:00Z"
        }

        result = check_for_updates(
            current_version="0.1.0-beta.1",
            force=False,
            cache_path=self.cache_file
        )

        mock_fetch.assert_called_once()
        self.assertIsNotNone(result)
        self.assertTrue(result["update_available"])
        self.assertFalse(result["cached"])
        self.assertEqual(result["latest_version"], "0.3.0")

        # Verify cache file was refreshed with the new version
        refreshed_cache = load_cache(self.cache_file)
        self.assertEqual(refreshed_cache["latest_version"], "0.3.0")

    @patch("update_notifier.fetch_latest_release_from_github")
    def test_force_flag_bypasses_valid_cache(self, mock_fetch):
        # Fresh cache created 5 minutes ago
        cache_data = {
            "last_checked": time.time() - 300,
            "latest_version": "0.1.0",
            "release_url": "https://github.com/Tel-BR/svg-maestro/releases/tag/v0.1.0",
            "published_at": "2026-10-16T12:00:00Z"
        }
        save_cache(self.cache_file, cache_data)

        mock_fetch.return_value = {
            "tag_name": "v0.2.5",
            "html_url": "https://github.com/Tel-BR/svg-maestro/releases/tag/v0.2.5",
            "published_at": "2026-10-16T14:00:00Z"
        }

        result = check_for_updates(
            current_version="0.1.0",
            force=True,
            cache_path=self.cache_file
        )

        mock_fetch.assert_called_once()
        self.assertIsNotNone(result)
        self.assertTrue(result["update_available"])
        self.assertFalse(result["cached"])
        self.assertEqual(result["latest_version"], "0.2.5")

    @patch("update_notifier.fetch_latest_release_from_github")
    def test_network_failure_returns_none_without_exception(self, mock_fetch):
        # Simulates network timeout or HTTP error
        mock_fetch.return_value = None

        result = check_for_updates(
            current_version="0.1.0-beta.1",
            force=True,
            cache_path=self.cache_file
        )

        # Must gracefully return None, never raise an exception
        self.assertIsNone(result)

    @patch("update_notifier.fetch_latest_release_from_github")
    def test_up_to_date_version_detected(self, mock_fetch):
        mock_fetch.return_value = {
            "tag_name": "v0.1.0",
            "html_url": "https://github.com/Tel-BR/svg-maestro/releases/tag/v0.1.0",
            "published_at": "2026-10-16T12:00:00Z"
        }

        result = check_for_updates(
            current_version="0.1.0",
            force=True,
            cache_path=self.cache_file
        )

        self.assertIsNotNone(result)
        self.assertFalse(result["update_available"])
        self.assertEqual(result["latest_version"], "0.1.0")


class TestGitHubFetchResilience(unittest.TestCase):
    """Unit tests ensuring fetch_latest_release_from_github never raises exceptions."""

    @patch("urllib.request.urlopen")
    def test_http_error_handled_gracefully(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="https://api.github.com", code=403, msg="Rate limit exceeded", hdrs={}, fp=None
        )
        result = fetch_latest_release_from_github(repo="Tel-BR/svg-maestro")
        self.assertIsNone(result)

    @patch("urllib.request.urlopen")
    def test_url_error_handled_gracefully(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")
        result = fetch_latest_release_from_github(repo="Tel-BR/svg-maestro")
        self.assertIsNone(result)

    @patch("urllib.request.urlopen")
    def test_timeout_handled_gracefully(self, mock_urlopen):
        mock_urlopen.side_effect = TimeoutError("Timed out")
        result = fetch_latest_release_from_github(repo="Tel-BR/svg-maestro")
        self.assertIsNone(result)


class TestUpdateBannerFormatting(unittest.TestCase):
    """Unit tests for update notice banner presentation."""

    def test_banner_when_update_available(self):
        info = {
            "update_available": True,
            "current_version": "0.1.0-beta.1",
            "latest_version": "0.2.0",
            "release_url": "https://github.com/Tel-BR/svg-maestro/releases/tag/v0.2.0",
            "published_at": "2026-10-16T12:00:00Z",
            "cached": False
        }
        banner = format_update_banner(info)
        self.assertTrue(len(banner) > 0)
        self.assertIn("SVG Maestro update available", banner)
        self.assertIn("0.1.0-beta.1", banner)
        self.assertIn("0.2.0", banner)
        self.assertIn("git pull", banner)
        self.assertIn("https://github.com/Tel-BR/svg-maestro/releases/tag/v0.2.0", banner)

    def test_banner_when_no_update_available(self):
        info = {
            "update_available": False,
            "current_version": "0.2.0",
            "latest_version": "0.2.0",
            "release_url": "",
            "cached": True
        }
        banner = format_update_banner(info)
        self.assertEqual(banner, "")

    def test_banner_when_info_is_none(self):
        self.assertEqual(format_update_banner(None), "")


class TestCLIIntegration(unittest.TestCase):
    """Unit tests verifying CLI execution of update_notifier and flags in other scripts."""

    def test_update_notifier_cli_help(self):
        import subprocess
        cmd = [sys.executable, os.path.join(SCRIPTS_DIR, "update_notifier.py"), "--help"]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("--check-update", proc.stdout)

    def test_validate_svg_cli_check_update_flag(self):
        import subprocess
        cmd = [sys.executable, os.path.join(SCRIPTS_DIR, "validate_svg.py"), "--help"]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("--check-update", proc.stdout)

    def test_refinement_verbs_cli_check_update_flag(self):
        import subprocess
        cmd = [sys.executable, os.path.join(SCRIPTS_DIR, "refinement_verbs.py"), "--help"]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("--check-update", proc.stdout)

    def test_update_notifier_cli_json_run(self):
        import subprocess
        import tempfile
        with tempfile.TemporaryDirectory() as tmp_dir:
            cache_path = os.path.join(tmp_dir, ".test_cache.json")
            cache_data = {
                "last_checked": time.time(),
                "latest_version": "0.9.0",
                "release_url": "https://github.com/Tel-BR/svg-maestro/releases/tag/v0.9.0",
                "published_at": "2026-10-16T12:00:00Z"
            }
            save_cache(cache_path, cache_data)
            # Patch default cache path by setting environment or passing custom version
            cmd = [
                sys.executable,
                "-c",
                f"import sys; sys.path.insert(0, r'{SCRIPTS_DIR}'); "
                f"from update_notifier import check_for_updates; "
                f"import json; print(json.dumps(check_for_updates(current_version='0.1.0', cache_path=r'{cache_path}')))"
            ]
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
            self.assertEqual(proc.returncode, 0)
            data = json.loads(proc.stdout)
            self.assertTrue(data["update_available"])
            self.assertEqual(data["latest_version"], "0.9.0")
            self.assertTrue(data["cached"])

    def test_validate_svg_cli_check_update_run(self):
        import subprocess
        cmd = [sys.executable, os.path.join(SCRIPTS_DIR, "validate_svg.py"), "--check-update"]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 0)

    def test_refinement_verbs_cli_check_update_run(self):
        import subprocess
        cmd = [sys.executable, os.path.join(SCRIPTS_DIR, "refinement_verbs.py"), "--check-update"]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 0)



if __name__ == "__main__":
    unittest.main()
