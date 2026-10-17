#!/usr/bin/env python3
"""
Tests for SVG Maestro Distribution Manifests (Ticket 03).
Validates JSON schema compliance, required fields, entrypoint existence,
and zero-drift version parity across SKILL.md, plugin.json, and skills.json.
"""

import os
import sys
import json
import re
import unittest
from typing import Dict, Any, List, Optional

# Setup sys.path
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TESTS_DIR, ".."))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")

if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from update_notifier import (
    DEFAULT_VERSION,
    get_current_version,
    get_manifest_version,
    parse_version,
)

SEMVER_REGEX = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


def extract_frontmatter_version(file_path: str) -> Optional[str]:
    """Extract version from YAML frontmatter of a markdown file."""
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read(2048)
    match = re.search(r"version:\s*([0-9a-zA-Z\.\-]+)", content)
    return match.group(1).strip() if match else None


def validate_plugin_manifest(data: Dict[str, Any], base_dir: str) -> List[str]:
    """Validate Claude Code plugin.json manifest structure and referenced files."""
    errors = []
    required_keys = ["name", "version", "description", "author", "repository"]
    for key in required_keys:
        if key not in data or not data[key]:
            errors.append(f"Missing or empty required field in plugin.json: '{key}'")

    if "name" in data and not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", str(data["name"])):
        errors.append(f"Invalid plugin name format (must be kebab-case): '{data['name']}'")

    if "version" in data and not SEMVER_REGEX.match(str(data["version"])):
        errors.append(f"Invalid SemVer in plugin.json: '{data['version']}'")

    if "author" in data:
        author = data["author"]
        if isinstance(author, dict):
            if "name" not in author or not author["name"]:
                errors.append("Author object must contain a non-empty 'name' field")
        elif not isinstance(author, str) or not author.strip():
            errors.append("Author field must be a valid dict or non-empty string")

    # Validate entrypoint if present
    if "entrypoint" in data:
        entrypoint_path = os.path.normpath(os.path.join(base_dir, data["entrypoint"]))
        if not os.path.exists(entrypoint_path):
            errors.append(f"Referenced entrypoint does not exist on disk: '{data['entrypoint']}'")

    # Validate skills if present
    if "skills" in data:
        skills = data["skills"]
        if not isinstance(skills, list) or len(skills) == 0:
            errors.append("'skills' field in plugin.json must be a non-empty list")
        else:
            for i, skill in enumerate(skills):
                if isinstance(skill, dict):
                    if "name" not in skill:
                        errors.append(f"Skill entry #{i} missing 'name'")
                    if "path" in skill:
                        skill_path = os.path.normpath(os.path.join(base_dir, skill["path"]))
                        if not os.path.exists(skill_path):
                            errors.append(f"Skill path does not exist on disk: '{skill['path']}'")
                elif isinstance(skill, str):
                    skill_path = os.path.normpath(os.path.join(base_dir, skill))
                    if not os.path.exists(skill_path):
                        errors.append(f"Skill path does not exist on disk: '{skill}'")

    return errors


def validate_skills_manifest(data: Dict[str, Any], base_dir: str) -> List[str]:
    """Validate npx skills skills.json manifest structure and referenced files."""
    errors = []
    required_keys = ["name", "version", "description", "author", "repository", "skills"]
    for key in required_keys:
        if key not in data or not data[key]:
            errors.append(f"Missing or empty required field in skills.json: '{key}'")

    if "name" in data and not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", str(data["name"])):
        errors.append(f"Invalid skills package name format (must be kebab-case): '{data['name']}'")

    if "version" in data and not SEMVER_REGEX.match(str(data["version"])):
        errors.append(f"Invalid SemVer in skills.json: '{data['version']}'")

    if "skills" in data:
        skills = data["skills"]
        if not isinstance(skills, list) or len(skills) == 0:
            errors.append("'skills' list must not be empty in skills.json")
        else:
            for i, s in enumerate(skills):
                if not isinstance(s, dict):
                    errors.append(f"Skill entry #{i} in skills.json must be an object")
                    continue
                for sk_key in ["name", "version", "description", "path"]:
                    if sk_key not in s or not s[sk_key]:
                        errors.append(f"Skill entry #{i} missing required property '{sk_key}'")
                if "path" in s:
                    full_p = os.path.normpath(os.path.join(base_dir, s["path"]))
                    if not os.path.exists(full_p):
                        errors.append(f"Skill path does not exist on disk: '{s['path']}'")

    return errors


class TestManifestExistenceAndIntegrity(unittest.TestCase):
    """Test presence and parse integrity of all distribution manifests."""

    def test_manifest_files_exist(self):
        claude_plugin_path = os.path.join(REPO_ROOT, ".claude-plugin", "plugin.json")
        root_plugin_path = os.path.join(REPO_ROOT, "plugin.json")
        skills_json_path = os.path.join(REPO_ROOT, "skills.json")
        skill_md_path = os.path.join(REPO_ROOT, "SKILL.md")
        ask_maestro_path = os.path.join(REPO_ROOT, "skills", "ask-maestro", "SKILL.md")

        self.assertTrue(os.path.isfile(claude_plugin_path), f"Missing {claude_plugin_path}")
        self.assertTrue(os.path.isfile(root_plugin_path), f"Missing {root_plugin_path}")
        self.assertTrue(os.path.isfile(skills_json_path), f"Missing {skills_json_path}")
        self.assertTrue(os.path.isfile(skill_md_path), f"Missing {skill_md_path}")
        self.assertTrue(os.path.isfile(ask_maestro_path), f"Missing {ask_maestro_path}")

    def test_json_parses_cleanly(self):
        for path in [
            os.path.join(REPO_ROOT, ".claude-plugin", "plugin.json"),
            os.path.join(REPO_ROOT, "plugin.json"),
            os.path.join(REPO_ROOT, "skills.json"),
        ]:
            with self.subTest(manifest=path):
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.assertIsInstance(data, dict)

    def test_claude_plugin_and_root_plugin_are_identical(self):
        claude_plugin_path = os.path.join(REPO_ROOT, ".claude-plugin", "plugin.json")
        root_plugin_path = os.path.join(REPO_ROOT, "plugin.json")

        with open(claude_plugin_path, "r", encoding="utf-8") as f1:
            data1 = json.load(f1)
        with open(root_plugin_path, "r", encoding="utf-8") as f2:
            data2 = json.load(f2)

        self.assertEqual(data1, data2, "Root plugin.json and .claude-plugin/plugin.json must have identical configuration")


class TestClaudePluginManifestSchema(unittest.TestCase):
    """Validate structure of .claude-plugin/plugin.json."""

    def setUp(self):
        self.path = os.path.join(REPO_ROOT, ".claude-plugin", "plugin.json")
        with open(self.path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def test_schema_conformance(self):
        errors = validate_plugin_manifest(self.data, REPO_ROOT)
        self.assertEqual(errors, [], f"Validation errors in plugin.json: {errors}")

    def test_metadata_values(self):
        self.assertEqual(self.data["name"], "svg-maestro")
        self.assertEqual(self.data["repository"], "https://github.com/Tel-BR/svg-maestro")
        self.assertEqual(self.data["homepage"], "https://github.com/Tel-BR/svg-maestro")
        self.assertEqual(self.data["license"], "MIT")
        self.assertEqual(self.data["author"]["name"], "Tel")
        self.assertIn("vector", self.data.get("keywords", []))
        self.assertIn("svg", self.data.get("keywords", []))

    def test_entrypoint_and_skills(self):
        self.assertEqual(self.data["entrypoint"], "./SKILL.md")
        self.assertTrue(os.path.exists(os.path.join(REPO_ROOT, self.data["entrypoint"])))

        skill_names = [s["name"] for s in self.data["skills"]]
        self.assertIn("svg-maestro", skill_names)
        self.assertIn("ask-maestro", skill_names)


class TestSkillsJsonManifestSchema(unittest.TestCase):
    """Validate structure of skills.json for npx skills registry."""

    def setUp(self):
        self.path = os.path.join(REPO_ROOT, "skills.json")
        with open(self.path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def test_schema_conformance(self):
        errors = validate_skills_manifest(self.data, REPO_ROOT)
        self.assertEqual(errors, [], f"Validation errors in skills.json: {errors}")

    def test_package_metadata(self):
        self.assertEqual(self.data["name"], "svg-maestro")
        self.assertEqual(self.data["repository"], "https://github.com/Tel-BR/svg-maestro")
        self.assertEqual(self.data["author"]["name"], "Tel")
        self.assertTrue(len(self.data["description"]) > 20)

    def test_catalog_skills_entries(self):
        skills = self.data["skills"]
        self.assertGreaterEqual(len(skills), 2)
        names = {s["name"]: s for s in skills}

        self.assertIn("svg-maestro", names)
        self.assertEqual(names["svg-maestro"]["path"], "./SKILL.md")
        self.assertTrue(os.path.exists(os.path.join(REPO_ROOT, names["svg-maestro"]["path"])))

        self.assertIn("ask-maestro", names)
        self.assertEqual(names["ask-maestro"]["path"], "./skills/ask-maestro/SKILL.md")
        self.assertTrue(os.path.exists(os.path.join(REPO_ROOT, names["ask-maestro"]["path"])))


class TestVersionParityAcrossEcosystem(unittest.TestCase):
    """Test zero-drift semantic version consistency across all skill manifests and scripts."""

    def test_all_versions_match_expected_beta(self):
        expected_version = "0.1.0-beta.1"

        root_skill_md = os.path.join(REPO_ROOT, "SKILL.md")
        ask_maestro_skill = os.path.join(REPO_ROOT, "skills", "ask-maestro", "SKILL.md")
        claude_plugin = os.path.join(REPO_ROOT, ".claude-plugin", "plugin.json")
        root_plugin = os.path.join(REPO_ROOT, "plugin.json")
        skills_json = os.path.join(REPO_ROOT, "skills.json")

        v_root_skill = extract_frontmatter_version(root_skill_md)
        v_ask_maestro = extract_frontmatter_version(ask_maestro_skill)

        with open(claude_plugin, "r", encoding="utf-8") as f:
            v_claude_plugin = json.load(f).get("version")

        with open(root_plugin, "r", encoding="utf-8") as f:
            v_root_plugin = json.load(f).get("version")

        with open(skills_json, "r", encoding="utf-8") as f:
            skills_data = json.load(f)
            v_skills_json = skills_data.get("version")
            catalog_versions = [s.get("version") for s in skills_data.get("skills", [])]

        v_update_notifier_default = DEFAULT_VERSION
        v_notifier_current = get_current_version()
        v_notifier_manifest = get_manifest_version(claude_plugin)

        # Assert all match expected
        self.assertEqual(v_root_skill, expected_version, "SKILL.md version drift")
        self.assertEqual(v_ask_maestro, expected_version, "ask-maestro SKILL.md version drift")
        self.assertEqual(v_claude_plugin, expected_version, ".claude-plugin/plugin.json version drift")
        self.assertEqual(v_root_plugin, expected_version, "root plugin.json version drift")
        self.assertEqual(v_skills_json, expected_version, "skills.json version drift")
        self.assertEqual(v_update_notifier_default, expected_version, "update_notifier.DEFAULT_VERSION drift")
        self.assertEqual(v_notifier_current, expected_version, "get_current_version() drift")
        self.assertEqual(v_notifier_manifest, expected_version, "get_manifest_version() drift")

        for cat_ver in catalog_versions:
            self.assertEqual(cat_ver, expected_version, "skills.json catalog entry version drift")

    def test_version_parities_are_mutually_equal(self):
        root_skill_ver = extract_frontmatter_version(os.path.join(REPO_ROOT, "SKILL.md"))
        manifest_ver = get_manifest_version()

        with open(os.path.join(REPO_ROOT, "skills.json"), "r", encoding="utf-8") as f:
            skills_ver = json.load(f).get("version")

        self.assertEqual(root_skill_ver, manifest_ver)
        self.assertEqual(manifest_ver, skills_ver)


class TestValidationRobustnessAndNegativeCases(unittest.TestCase):
    """Test validator functions with deliberately malformed or incomplete schemas."""

    def test_plugin_validator_catches_missing_fields(self):
        bad_manifest = {"name": "svg-maestro"}
        errors = validate_plugin_manifest(bad_manifest, REPO_ROOT)
        self.assertTrue(any("version" in e for e in errors))
        self.assertTrue(any("description" in e for e in errors))
        self.assertTrue(any("author" in e for e in errors))
        self.assertTrue(any("repository" in e for e in errors))

    def test_plugin_validator_catches_invalid_name_and_semver(self):
        bad_manifest = {
            "name": "Invalid_Name!",
            "version": "not-a-semver",
            "description": "test",
            "author": {"name": "Tel"},
            "repository": "https://github.com/Tel-BR/svg-maestro",
        }
        errors = validate_plugin_manifest(bad_manifest, REPO_ROOT)
        self.assertTrue(any("kebab-case" in e for e in errors))
        self.assertTrue(any("SemVer" in e for e in errors))

    def test_plugin_validator_catches_nonexistent_entrypoint(self):
        bad_manifest = {
            "name": "svg-maestro",
            "version": "1.0.0",
            "description": "test",
            "author": {"name": "Tel"},
            "repository": "https://github.com/Tel-BR/svg-maestro",
            "entrypoint": "./does_not_exist.md",
        }
        errors = validate_plugin_manifest(bad_manifest, REPO_ROOT)
        self.assertTrue(any("entrypoint does not exist" in e for e in errors))

    def test_skills_validator_catches_empty_skills_list(self):
        bad_manifest = {
            "name": "svg-maestro",
            "version": "1.0.0",
            "description": "test",
            "author": {"name": "Tel"},
            "repository": "https://github.com/Tel-BR/svg-maestro",
            "skills": [],
        }
        errors = validate_skills_manifest(bad_manifest, REPO_ROOT)
        self.assertTrue(any("must not be empty" in e for e in errors))

    def test_skills_validator_catches_nonexistent_skill_path(self):
        bad_manifest = {
            "name": "svg-maestro",
            "version": "1.0.0",
            "description": "test",
            "author": {"name": "Tel"},
            "repository": "https://github.com/Tel-BR/svg-maestro",
            "skills": [
                {
                    "name": "ghost",
                    "version": "1.0.0",
                    "description": "does not exist",
                    "path": "./ghost/SKILL.md",
                }
            ],
        }
        errors = validate_skills_manifest(bad_manifest, REPO_ROOT)
        self.assertTrue(any("Skill path does not exist" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
