#!/usr/bin/env python3
"""
SVG Maestro - Version Checker and Update Notifier
Standalone utility and API to check GitHub releases for new versions of SVG Maestro.
Features 24-hour local caching, offline/timeout resilience, SemVer comparison,
and non-intrusive console notifications.
"""

import os
import sys
import json
import time
import re
import argparse
import urllib.request
import urllib.error
from typing import Dict, Any, Optional, Tuple, Union

DEFAULT_REPO = "Tel-BR/svg-maestro"
CACHE_TTL_SECONDS = 86400  # 24 hours
DEFAULT_VERSION = "0.1.0-beta.1"

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_default_cache_path() -> str:
    """Return the default path for the update cache file."""
    candidate = os.path.join(REPO_ROOT, ".update_cache.json")
    try:
        if os.path.exists(candidate) and os.access(candidate, os.W_OK):
            return candidate
        if os.access(REPO_ROOT, os.W_OK):
            return candidate
    except Exception:
        pass
    # Fallback to user cache directory
    user_cache = os.path.expanduser("~/.cache/svg-maestro")
    try:
        os.makedirs(user_cache, exist_ok=True)
    except Exception:
        pass
    return os.path.join(user_cache, ".update_cache.json")


def get_manifest_version(manifest_path: Optional[str] = None) -> Optional[str]:
    """Extract version from a JSON manifest (plugin.json or skills.json)."""
    if manifest_path is None:
        for candidate in [
            os.path.join(REPO_ROOT, ".claude-plugin", "plugin.json"),
            os.path.join(REPO_ROOT, "plugin.json"),
            os.path.join(REPO_ROOT, "skills.json"),
        ]:
            if os.path.exists(candidate):
                manifest_path = candidate
                break

    if manifest_path and os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                val = data.get("version")
                if val:
                    return str(val).strip()
        except Exception:
            pass
    return None


def get_current_version(skill_path: Optional[str] = None) -> str:
    """Extract current semver from SKILL.md frontmatter or distribution manifests with fallback."""
    explicit_path = skill_path is not None
    if skill_path is None:
        skill_path = os.path.join(REPO_ROOT, "SKILL.md")

    if os.path.exists(skill_path):
        try:
            with open(skill_path, "r", encoding="utf-8") as f:
                content = f.read(2048)  # Read header/frontmatter
            match = re.search(r"version:\s*([0-9a-zA-Z\.\-]+)", content)
            if match:
                return match.group(1).strip()
        except Exception:
            pass

    if not explicit_path:
        manifest_ver = get_manifest_version()
        if manifest_ver:
            return manifest_ver

    return DEFAULT_VERSION


def parse_version(v_str: str) -> Tuple[Tuple[int, ...], Optional[Tuple[Union[int, str], ...]]]:
    """
    Parse a version string (e.g., '0.1.0', 'v0.1.0-beta.1', '1.0.0-rc.2') into:
    (base_tuple, prerelease_tuple_or_None).
    """
    cleaned = v_str.strip().lstrip("vV")
    if "-" in cleaned:
        base_part, pre_part = cleaned.split("-", 1)
    else:
        base_part, pre_part = cleaned, None

    # Base numbers (major, minor, patch)
    base_nums = []
    for num in base_part.split("."):
        try:
            base_nums.append(int(num))
        except ValueError:
            base_nums.append(0)
    while len(base_nums) < 3:
        base_nums.append(0)

    # Prerelease identifiers
    if pre_part is not None:
        pre_tokens = []
        for token in pre_part.split("."):
            if token.isdigit():
                pre_tokens.append(int(token))
            else:
                pre_tokens.append(token)
        pre_tuple = tuple(pre_tokens)
    else:
        pre_tuple = None

    return tuple(base_nums), pre_tuple


def compare_versions(v1_str: str, v2_str: str) -> int:
    """
    Compare two version strings according to SemVer 2.0.0 precedence.
    Returns:
       1 if v1 > v2
      -1 if v1 < v2
       0 if v1 == v2
    """
    base1, pre1 = parse_version(v1_str)
    base2, pre2 = parse_version(v2_str)

    if base1 > base2:
        return 1
    if base1 < base2:
        return -1

    # Base versions are identical.
    # SemVer: A normal release has higher precedence than a pre-release.
    if pre1 is None and pre2 is None:
        return 0
    if pre1 is None and pre2 is not None:
        return 1  # v1 is full release, v2 is prerelease -> v1 > v2
    if pre1 is not None and pre2 is None:
        return -1  # v1 is prerelease, v2 is full release -> v1 < v2

    # Both have prerelease identifiers: compare parts
    for part1, part2 in zip(pre1, pre2):
        if part1 == part2:
            continue
        # Numeric identifiers have lower precedence than string identifiers
        type1_str = isinstance(part1, str)
        type2_str = isinstance(part2, str)
        if type1_str != type2_str:
            return 1 if type1_str else -1
        return 1 if part1 > part2 else -1

    # If all shared parts are equal, longer pre-release wins
    if len(pre1) > len(pre2):
        return 1
    if len(pre1) < len(pre2):
        return -1

    return 0


def is_newer_version(latest_str: str, current_str: str) -> bool:
    """Return True if latest_str is strictly newer than current_str."""
    return compare_versions(latest_str, current_str) > 0


def load_cache(cache_path: str) -> Optional[Dict[str, Any]]:
    """Safely load cache JSON file."""
    if not os.path.exists(cache_path):
        return None
    try:
        with open(cache_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict) and "last_checked" in data and "latest_version" in data:
                return data
    except Exception:
        pass
    return None


def save_cache(cache_path: str, data: Dict[str, Any]) -> bool:
    """Safely save cache JSON file."""
    try:
        parent_dir = os.path.dirname(os.path.abspath(cache_path))
        os.makedirs(parent_dir, exist_ok=True)
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False


def fetch_latest_release_from_github(repo: str = DEFAULT_REPO, timeout: float = 3.0) -> Optional[Dict[str, Any]]:
    """
    Fetch the latest release information from GitHub API.
    Resilient: never raises exceptions on timeouts or HTTP/network errors.
    """
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "SVG-Maestro-UpdateNotifier",
            "Accept": "application/vnd.github.v3+json"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                body = response.read().decode("utf-8")
                data = json.loads(body)
                return {
                    "tag_name": data.get("tag_name", ""),
                    "html_url": data.get("html_url", f"https://github.com/{repo}/releases"),
                    "published_at": data.get("published_at")
                }
    except Exception:
        # Graceful failure: offline, rate limit, timeout, etc.
        pass

    return None


def check_for_updates(
    current_version: Optional[str] = None,
    force: bool = False,
    repo: str = DEFAULT_REPO,
    cache_path: Optional[str] = None,
    timeout: float = 3.0
) -> Optional[Dict[str, Any]]:
    """
    Check if a newer version of SVG Maestro exists on GitHub.
    Uses 24-hour local caching to avoid rate limits.
    Returns a dict with update details, or None on network error when no cache is available.
    """
    curr_v = current_version or get_current_version()
    cache_file = cache_path or get_default_cache_path()

    # 1. Check cache if not forcing refresh
    if not force:
        cached_data = load_cache(cache_file)
        if cached_data is not None:
            last_checked = cached_data.get("last_checked", 0)
            if time.time() - last_checked < CACHE_TTL_SECONDS:
                latest_v = cached_data.get("latest_version", "").lstrip("vV")
                return {
                    "update_available": is_newer_version(latest_v, curr_v),
                    "current_version": curr_v,
                    "latest_version": latest_v,
                    "release_url": cached_data.get("release_url", f"https://github.com/{repo}/releases"),
                    "published_at": cached_data.get("published_at"),
                    "cached": True
                }

    # 2. Fetch remote release
    remote_info = fetch_latest_release_from_github(repo=repo, timeout=timeout)
    if remote_info is None:
        # Graceful degradation on network failure / offline
        return None

    raw_tag = remote_info.get("tag_name", "")
    latest_v = raw_tag.lstrip("vV")
    release_url = remote_info.get("html_url", f"https://github.com/{repo}/releases")
    published_at = remote_info.get("published_at")

    # 3. Update cache
    new_cache = {
        "last_checked": time.time(),
        "latest_version": latest_v,
        "release_url": release_url,
        "published_at": published_at
    }
    save_cache(cache_file, new_cache)

    return {
        "update_available": is_newer_version(latest_v, curr_v),
        "current_version": curr_v,
        "latest_version": latest_v,
        "release_url": release_url,
        "published_at": published_at,
        "cached": False
    }


def format_update_banner(info: Optional[Dict[str, Any]]) -> str:
    """Format a clean, non-intrusive console notification box if an update is available."""
    if not info or not info.get("update_available"):
        return ""

    curr = info.get("current_version", "unknown")
    latest = info.get("latest_version", "unknown")
    url = info.get("release_url", "https://github.com/Tel-BR/svg-maestro/releases")

    line1 = f"  SVG Maestro update available: {curr} -> {latest}"
    line2 = f"  To update, run: git pull"
    line3 = f"  Release notes: {url}"

    max_len = max(len(line1), len(line2), len(line3)) + 2
    border_top = "┌" + "─" * max_len + "┐"
    border_bottom = "└" + "─" * max_len + "┘"

    pad1 = " " * (max_len - len(line1))
    pad2 = " " * (max_len - len(line2))
    pad3 = " " * (max_len - len(line3))

    return (
        f"\n{border_top}\n"
        f"│{line1}{pad1}│\n"
        f"│{line2}{pad2}│\n"
        f"│{line3}{pad3}│\n"
        f"{border_bottom}\n"
    )


def print_update_banner(info: Optional[Dict[str, Any]], stream=sys.stderr) -> None:
    """Print update banner to stderr if an update is available."""
    banner = format_update_banner(info)
    if banner:
        stream.write(banner)
        stream.flush()


def main():
    parser = argparse.ArgumentParser(description="SVG Maestro - Version Checker & Update Notifier")
    parser.add_argument("--check-update", action="store_true", help="Check for SVG Maestro updates")
    parser.add_argument("--force", action="store_true", help="Force check ignoring 24-hour cache")
    parser.add_argument("--json", action="store_true", help="Output check results in JSON format")
    parser.add_argument("--repo", default=DEFAULT_REPO, help=f"GitHub repository (default: {DEFAULT_REPO})")
    parser.add_argument("--current-version", default=None, help="Override current version for comparison")
    parser.add_argument("--quiet", action="store_true", help="Suppress output if up-to-date")

    args = parser.parse_args()

    result = check_for_updates(
        current_version=args.current_version,
        force=args.force,
        repo=args.repo
    )

    if args.json:
        print(json.dumps(result or {"error": "Network unavailable or failed to check"}, indent=2))
        sys.exit(0)

    if result is None:
        if not args.quiet:
            print("[!] Unable to check for updates (offline or network error).", file=sys.stderr)
        sys.exit(0)

    if result.get("update_available"):
        print_update_banner(result, stream=sys.stdout)
    else:
        if not args.quiet:
            print(f"[OK] SVG Maestro is up to date (v{result.get('current_version')}).")

    sys.exit(0)


if __name__ == "__main__":
    main()
