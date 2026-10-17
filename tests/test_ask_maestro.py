#!/usr/bin/env python3
"""
Test suite for ask-maestro skill and navigation router.
Verifies:
- Skill frontmatter and metadata
- Main flow, on-ramps, context hygiene, and vocabulary anchors
- Internationalization (i18n) protocol compliance
- Synchronization between repository skill and global agent skill
"""

import os
import re
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOCAL_SKILL_PATH = os.path.join(REPO_ROOT, "skills", "ask-maestro", "SKILL.md")
GLOBAL_SKILL_PATH = os.path.expanduser(r"~\.gemini\config\skills\ask-maestro\SKILL.md")


class TestAskMaestroSkill(unittest.TestCase):
    """Verifies that ask-maestro follows Matt Pocock router principles and i18n standards."""

    def setUp(self):
        self.assertTrue(
            os.path.exists(LOCAL_SKILL_PATH),
            f"Local skill file must exist at {LOCAL_SKILL_PATH}",
        )
        with open(LOCAL_SKILL_PATH, "r", encoding="utf-8") as f:
            self.content = f.read()

    def test_frontmatter_validity(self):
        """Verifies YAML frontmatter conforms to Antigravity / Gemini skills standard."""
        self.assertTrue(self.content.startswith("---"))
        parts = self.content.split("---", 2)
        self.assertGreaterEqual(len(parts), 3, "Skill must have valid YAML frontmatter delimiters")
        frontmatter = parts[1]

        self.assertIn("name: ask-maestro", frontmatter)
        self.assertIn("description:", frontmatter)
        self.assertIn("disable-model-invocation: true", frontmatter)

    def test_main_flow_presence_and_phases(self):
        """Verifies canonical main flow from briefing to production handoff."""
        self.assertTrue(
            re.search(r"main flow", self.content, re.IGNORECASE),
            "Must define the canonical main flow",
        )
        self.assertIn("brief", self.content.lower(), "Must reference briefing step")
        self.assertIn("BRIEF.md", self.content, "Must reference binding BRIEF.md")
        self.assertIn("validate_svg.py", self.content, "Must require autonomous linter step")
        self.assertIn("Wrapper Pattern", self.content, "Must mandate Wrapper Pattern")

    def test_on_ramps_presence(self):
        """Verifies on-ramps for foreign assets, bugs, and dashboard/powerbi pipelines."""
        self.assertTrue(re.search(r"on-ramps", self.content, re.IGNORECASE))
        # On-ramp 1: Foreign / legacy SVG
        self.assertTrue(
            re.search(r"(figma|inkscape|foreign|existing)", self.content, re.IGNORECASE)
        )
        # On-ramp 2: Broken transforms or mutation collisions
        self.assertTrue(
            re.search(r"(broken|collision|diagnos|transform-box)", self.content, re.IGNORECASE)
        )
        # On-ramp 3: Multi-asset / kits
        self.assertTrue(
            re.search(r"(kit|multi-asset|ticket)", self.content, re.IGNORECASE)
        )
        # On-ramp 4: Power BI DAX
        self.assertTrue(
            re.search(r"(power bi|dax|dashboard)", self.content, re.IGNORECASE)
        )

    def test_context_hygiene_and_smart_zone(self):
        """Verifies operational context hygiene guidance for large XML/vector projects."""
        self.assertTrue(re.search(r"context hygiene", self.content, re.IGNORECASE))
        self.assertIn("smart zone", self.content.lower())

    def test_refinement_verbs_anchors(self):
        """Verifies that all 6 creative refinement verbs are documented."""
        verbs = ["bolder", "quieter", "distill", "delight", "animate", "critique"]
        for verb in verbs:
            self.assertIn(verb, self.content.lower(), f"Refinement verb '{verb}' must be documented")

    def test_i18n_protocol_present(self):
        """Verifies polyglot agent behavior and canonical English code standards."""
        self.assertTrue(
            re.search(r"(i18n|internationalization|multilingual|polyglot)", self.content, re.IGNORECASE),
            "Must include internationalization protocol",
        )
        # Must mandate canonical English XML/tokens and polyglot user interaction
        self.assertTrue(
            re.search(r"(canonical english|portuguese)", self.content, re.IGNORECASE)
        )

    def test_global_skill_mirrored(self):
        """Verifies that the global skill directory in ~/.gemini/config/skills has the skill."""
        if os.path.exists(os.path.dirname(GLOBAL_SKILL_PATH)):
            self.assertTrue(
                os.path.exists(GLOBAL_SKILL_PATH),
                f"Global skill must exist at {GLOBAL_SKILL_PATH}",
            )
            with open(GLOBAL_SKILL_PATH, "r", encoding="utf-8") as f:
                global_content = f.read()
            self.assertEqual(
                self.content,
                global_content,
                "Global skill must be an exact mirror of repository skill",
            )

    def test_version_metadata_and_consistency(self):
        """Verifies metadata version exists in both ask-maestro and root SKILL.md and are consistent."""
        root_skill_path = os.path.join(REPO_ROOT, "SKILL.md")
        with open(root_skill_path, "r", encoding="utf-8") as f:
            root_content = f.read()

        match_child = re.search(r"version:\s*([0-9a-zA-Z\.\-]+)", self.content)
        self.assertIsNotNone(match_child, "ask-maestro must define metadata.version")
        child_version = match_child.group(1).strip()

        match_root = re.search(r"version:\s*([0-9a-zA-Z\.\-]+)", root_content)
        self.assertIsNotNone(match_root, "root SKILL.md must define metadata.version")
        root_version = match_root.group(1).strip()

        self.assertEqual(child_version, root_version, "Versions between root and child skill must be identical")

    def test_lifecycle_and_version_management_present(self):
        """Verifies Lifecycle & Version Management sections, update_notifier.py, and git -C pull commands."""
        root_skill_path = os.path.join(REPO_ROOT, "SKILL.md")
        with open(root_skill_path, "r", encoding="utf-8") as f:
            root_content = f.read()

        for content, name in [(root_content, "root SKILL.md"), (self.content, "ask-maestro SKILL.md")]:
            self.assertIn(
                "Lifecycle & Version Management",
                content,
                f"{name} must contain Lifecycle & Version Management section",
            )
            self.assertIn("update_notifier.py", content, f"{name} must reference update_notifier.py")
            self.assertIn("git -C", content, f"{name} must provide copy-paste git -C pull command")

        # Root skill must explicitly forbid halting the user's creative workflow
        self.assertTrue(
            re.search(r"(never halt|non-blocking)", root_content, re.IGNORECASE),
            "root SKILL.md must mandate non-blocking update checks that never halt creative flow",
        )

    def test_global_root_skill_mirrored(self):
        """Verifies that the global root skill directory in ~/.gemini/config/skills/svg-maestro is mirrored."""
        global_root_path = os.path.expanduser(r"~\.gemini\config\skills\svg-maestro\SKILL.md")
        if os.path.exists(os.path.dirname(global_root_path)):
            self.assertTrue(
                os.path.exists(global_root_path),
                f"Global root skill must exist at {global_root_path}",
            )
            root_skill_path = os.path.join(REPO_ROOT, "SKILL.md")
            with open(root_skill_path, "r", encoding="utf-8") as f:
                root_content = f.read()
            with open(global_root_path, "r", encoding="utf-8") as f:
                global_content = f.read()
            self.assertEqual(
                root_content,
                global_content,
                "Global root skill must be an exact mirror of repository SKILL.md",
            )


if __name__ == "__main__":
    unittest.main()
