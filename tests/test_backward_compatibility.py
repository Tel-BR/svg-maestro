#!/usr/bin/env python3
"""
SVG Maestro - Backward Compatibility & Legacy SVG Tolerance Test Suite
Ticket 04 Regression Suite:
Verifies ingestion robustness across scripts/refinement_verbs.py and scripts/validate_svg.py.
Guarantees that older or un-versioned SVGs (lacking wrapper patterns, missing Inkscape layers,
or using legacy attributes) are safely processed, validated, and auto-upgraded in-memory.
"""

import os
import sys
import json
import shutil
import tempfile
import unittest
import subprocess
import xml.etree.ElementTree as ET

# Ensure repo root and scripts are in sys.path
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TESTS_DIR, ".."))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
FIXTURES_DIR = os.path.join(TESTS_DIR, "fixtures")
LEGACY_FIXTURES_DIR = os.path.join(FIXTURES_DIR, "legacy")

if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from validate_svg import validate_svg_file, ValidationResult
from refinement_verbs import (
    bolder,
    quieter,
    distill,
    delight,
    animate,
    critique,
    upgrade_legacy_svg,
    apply_verb,
    apply_verb_file,
    format_critique_markdown
)


class TestLegacyLinterRobustness(unittest.TestCase):
    """Verifies scripts/validate_svg.py handles legacy SVGs cleanly with actionable upgrade hints."""

    def setUp(self):
        self.fixtures = {
            "bare": os.path.join(LEGACY_FIXTURES_DIR, "bare_legacy.svg"),
            "unwrapped_anim": os.path.join(LEGACY_FIXTURES_DIR, "unwrapped_animation_legacy.svg"),
            "early_beta": os.path.join(LEGACY_FIXTURES_DIR, "early_beta_v010.svg"),
            "telemetry_card": os.path.join(LEGACY_FIXTURES_DIR, "legacy_telemetry_card.svg"),
        }
        for name, path in self.fixtures.items():
            self.assertTrue(os.path.exists(path), f"Legacy fixture '{name}' not found at {path}")

    def test_linter_never_crashes_on_legacy_assets(self):
        """validate_svg_file must execute cleanly without unhandled exceptions on all legacy fixtures."""
        for name, path in self.fixtures.items():
            result = validate_svg_file(path)
            self.assertIsInstance(result, ValidationResult, f"Failed on fixture {name}")
            self.assertIsInstance(result.errors, list)
            self.assertIsInstance(result.warnings, list)
            self.assertIsInstance(result.hints, list)

    def test_bare_legacy_produces_layer_and_namespace_hints(self):
        """bare_legacy.svg must trigger layer and namespace warnings/errors with actionable hints."""
        result = validate_svg_file(self.fixtures["bare"])
        self.assertFalse(result.is_valid)

        error_codes = [e["code"] for e in result.errors]
        self.assertIn("MISSING_INKSCAPE_NS", error_codes)
        self.assertIn("NO_INKSCAPE_LAYERS", error_codes)

        hint_codes = [h["code"] for h in result.hints]
        self.assertIn("UPGRADE_MISSING_INKSCAPE_NS", hint_codes)
        self.assertIn("UPGRADE_NO_INKSCAPE_LAYERS", hint_codes)

        # Confirm hints contain actionable instructions
        layer_hint = next(h for h in result.hints if h["code"] == "UPGRADE_NO_INKSCAPE_LAYERS")
        self.assertIn("semantic layer groups", layer_hint["message"])

    def test_unwrapped_animation_produces_motion_wrapper_hints(self):
        """unwrapped_animation_legacy.svg must detect transform-box, transform-origin, and wrapper collision."""
        result = validate_svg_file(self.fixtures["unwrapped_anim"])
        self.assertFalse(result.is_valid)

        error_codes = [e["code"] for e in result.errors]
        warning_codes = [w["code"] for w in result.warnings]
        self.assertIn("MISSING_TRANSFORM_BOX", error_codes)
        self.assertIn("MISSING_TRANSFORM_ORIGIN", warning_codes)
        self.assertIn("WRAPPER_PATTERN_COLLISION", warning_codes)

        hint_codes = [h["code"] for h in result.hints]
        self.assertIn("UPGRADE_MISSING_TRANSFORM_BOX", hint_codes)
        self.assertIn("UPGRADE_WRAPPER_PATTERN_COLLISION", hint_codes)

    def test_early_beta_produces_defs_and_layers_hints(self):
        """early_beta_v010.svg must detect generic def IDs and provide rename hints."""
        result = validate_svg_file(self.fixtures["early_beta"])
        warning_codes = [w["code"] for w in result.warnings]
        self.assertIn("GENERIC_DEF_ID", warning_codes)

        hint_codes = [h["code"] for h in result.hints]
        self.assertIn("UPGRADE_GENERIC_DEF_ID", hint_codes)

    def test_legacy_telemetry_card_detects_missing_viewbox_and_unlabeled_layer(self):
        """legacy_telemetry_card.svg must flag missing viewBox and unlabeled layer."""
        result = validate_svg_file(self.fixtures["telemetry_card"])
        self.assertFalse(result.is_valid)

        error_codes = [e["code"] for e in result.errors]
        warning_codes = [w["code"] for w in result.warnings]
        self.assertIn("MISSING_VIEWBOX", error_codes)
        self.assertIn("UNLABELED_LAYER", warning_codes)

        hint_codes = [h["code"] for h in result.hints]
        self.assertIn("UPGRADE_MISSING_VIEWBOX", hint_codes)
        self.assertIn("UPGRADE_UNLABELED_LAYER", hint_codes)

    def test_linter_cli_json_includes_actionable_hints(self):
        """validate_svg.py CLI --json output must serialize hints array."""
        cmd = [
            sys.executable,
            os.path.join(SCRIPTS_DIR, "validate_svg.py"),
            self.fixtures["bare"],
            "--json"
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 1)  # Invalid document exits 1

        data = json.loads(proc.stdout)
        self.assertIn("hints", data)
        self.assertIn("hints_count", data)
        self.assertGreater(data["hints_count"], 0)
        self.assertTrue(any("UPGRADE_NO_INKSCAPE_LAYERS" == h["code"] for h in data["hints"]))

    def test_linter_cli_human_output_displays_upgrade_hints_section(self):
        """validate_svg.py CLI human output must render ACTIONABLE UPGRADE HINTS section."""
        cmd = [
            sys.executable,
            os.path.join(SCRIPTS_DIR, "validate_svg.py"),
            self.fixtures["unwrapped_anim"]
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("ACTIONABLE UPGRADE HINTS", proc.stdout)
        self.assertIn("UPGRADE_WRAPPER_PATTERN_COLLISION", proc.stdout)


class TestRefinementVerbsLegacyCompatibility(unittest.TestCase):
    """Verifies that all refinement verbs auto-upgrade legacy assets in-memory to 100% compliance."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="svg_maestro_compat_test_")
        self.fixtures = {
            "bare": os.path.join(LEGACY_FIXTURES_DIR, "bare_legacy.svg"),
            "unwrapped_anim": os.path.join(LEGACY_FIXTURES_DIR, "unwrapped_animation_legacy.svg"),
            "early_beta": os.path.join(LEGACY_FIXTURES_DIR, "early_beta_v010.svg"),
            "telemetry_card": os.path.join(LEGACY_FIXTURES_DIR, "legacy_telemetry_card.svg"),
        }

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _assert_valid_modern_svg(self, svg_content: str, label: str):
        """Helper asserting that refined SVG markup strictly passes validator with 0 errors and 0 warnings."""
        temp_file = os.path.join(self.temp_dir, f"{label}.svg")
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(svg_content)

        res = validate_svg_file(temp_file)
        self.assertTrue(res.is_valid, f"{label} produced errors: {res.errors}")
        self.assertEqual(len(res.errors), 0, f"{label} errors: {res.errors}")
        self.assertEqual(len(res.warnings), 0, f"{label} warnings: {res.warnings}")
        self.assertTrue(res.stats["has_inkscape_ns"], f"{label} missing Inkscape NS")
        self.assertTrue(res.stats["has_viewbox"], f"{label} missing viewBox")
        self.assertGreater(res.stats["layers_count"], 0, f"{label} has 0 layers")

    # -------------------------------------------------------------------------
    # 1. BOLDER VERB ON LEGACY
    # -------------------------------------------------------------------------
    def test_bolder_verb_upgrades_and_amplifies_legacy_fixtures(self):
        """'bolder' must auto-upgrade all legacy fixtures in-memory and amplify strokes/contrast."""
        for name, fixture_path in self.fixtures.items():
            with open(fixture_path, "r", encoding="utf-8") as f:
                content = f.read()

            refined = bolder(content, factor=1.6)
            self._assert_valid_modern_svg(refined, f"bolder_{name}")

    # -------------------------------------------------------------------------
    # 2. QUIETER VERB ON LEGACY
    # -------------------------------------------------------------------------
    def test_quieter_verb_upgrades_and_softens_legacy_fixtures(self):
        """'quieter' must auto-upgrade all legacy fixtures in-memory and soften strokes/saturation."""
        for name, fixture_path in self.fixtures.items():
            with open(fixture_path, "r", encoding="utf-8") as f:
                content = f.read()

            refined = quieter(content, factor=0.7)
            self._assert_valid_modern_svg(refined, f"quieter_{name}")

    # -------------------------------------------------------------------------
    # 3. DISTILL VERB ON LEGACY
    # -------------------------------------------------------------------------
    def test_distill_verb_upgrades_and_strips_decorations_from_legacy(self):
        """'distill' must auto-upgrade bare SVGs and remove secondary tics while preserving hierarchy."""
        with open(self.fixtures["bare"], "r", encoding="utf-8") as f:
            content = f.read()

        refined = distill(content)
        self._assert_valid_modern_svg(refined, "distill_bare")

        # Confirm secondary tics were stripped
        self.assertNotIn("accent-dot-1", refined)
        self.assertNotIn("accent-dot-2", refined)

        # Confirm core geometry and typography were preserved
        self.assertIn("core-circle", refined)
        self.assertIn("BARE LEGACY ASSET", refined)
        self.assertIn("layer-background", refined)
        self.assertIn("layer-geometry", refined)
        self.assertIn("layer-typography", refined)

    # -------------------------------------------------------------------------
    # 4. DELIGHT VERB ON LEGACY
    # -------------------------------------------------------------------------
    def test_delight_verb_injects_wrapper_pattern_into_legacy(self):
        """'delight' must auto-upgrade bare SVGs and inject micro-motion adhering to the Wrapper Pattern."""
        for name, fixture_path in self.fixtures.items():
            with open(fixture_path, "r", encoding="utf-8") as f:
                content = f.read()

            refined = delight(content)
            self._assert_valid_modern_svg(refined, f"delight_{name}")
            self.assertIn("anim-delight-orbit", refined)
            self.assertIn("transform-box: fill-box;", refined)
            self.assertIn("transform-origin: center;", refined)

    # -------------------------------------------------------------------------
    # 5. ANIMATE VERB ON LEGACY
    # -------------------------------------------------------------------------
    def test_animate_verb_transforms_legacy_static_into_motion_asset(self):
        """'animate' must wrap target shapes in anim-wrapper groups and pass validation with 0 errors/warnings."""
        for name in ("bare", "early_beta"):
            with open(self.fixtures[name], "r", encoding="utf-8") as f:
                content = f.read()

            refined = animate(content)
            self._assert_valid_modern_svg(refined, f"animate_{name}")
            self.assertIn("anim-wrapper-", refined)
            self.assertIn("@keyframes", refined)
            self.assertIn("transform-box: fill-box;", refined)
            self.assertIn("transform-origin: center;", refined)

    # -------------------------------------------------------------------------
    # 6. CRITIQUE VERB ON LEGACY
    # -------------------------------------------------------------------------
    def test_critique_evaluates_legacy_assets_with_upgrade_recommendations(self):
        """'critique' must score legacy flaws accurately and emit actionable upgrade recommendations."""
        for name, fixture_path in self.fixtures.items():
            with open(fixture_path, "r", encoding="utf-8") as f:
                content = f.read()

            report = critique(content)
            self.assertIn("technical_standards", report)
            self.assertIn("aesthetic_craft", report)
            self.assertIn("composite_score", report)
            self.assertIn("recommendations", report)

            # Confirm legacy flaw is reflected in low technical standards
            self.assertLessEqual(report["technical_standards"]["score"], 70)
            self.assertIn(report["technical_standards"]["grade"], ["D", "F"])

            # Confirm upgrade recommendations are present
            recs = " ".join(report["recommendations"])
            self.assertIn("Legacy or non-compliant SVG detected", recs)
            self.assertTrue(any("bolder" in v or "animate" in v for v in report["suggested_verbs"]))

            # Markdown report formatting must succeed without error
            md = format_critique_markdown(report, target_name=name)
            self.assertIn("SVG Maestro Design Critique", md)
            self.assertIn("Axis 1: Technical Standards", md)

    # -------------------------------------------------------------------------
    # 7. DIRECT UPGRADE VERB
    # -------------------------------------------------------------------------
    def test_direct_upgrade_legacy_svg_api(self):
        """upgrade_legacy_svg must transform raw legacy SVG into a compliant modern SVG without aesthetic changes."""
        for name, fixture_path in self.fixtures.items():
            with open(fixture_path, "r", encoding="utf-8") as f:
                content = f.read()

            upgraded = upgrade_legacy_svg(content)
            self._assert_valid_modern_svg(upgraded, f"upgrade_{name}")

    # -------------------------------------------------------------------------
    # 8. CHAINED REFINEMENTS ON LEGACY ASSETS
    # -------------------------------------------------------------------------
    def test_chained_refinements_on_legacy_asset(self):
        """Chaining multiple refinement verbs (bolder -> delight -> quieter) on bare legacy SVG must remain 100% compliant."""
        with open(self.fixtures["bare"], "r", encoding="utf-8") as f:
            bare_content = f.read()

        step1 = bolder(bare_content)
        self._assert_valid_modern_svg(step1, "chain_step1")

        step2 = delight(step1)
        self._assert_valid_modern_svg(step2, "chain_step2")

        step3 = quieter(step2)
        self._assert_valid_modern_svg(step3, "chain_step3")

    # -------------------------------------------------------------------------
    # 9. NON-DESTRUCTIVE DEFAULT CLI CONTRACT
    # -------------------------------------------------------------------------
    def test_cli_refinement_on_legacy_is_non_destructive_by_default(self):
        """CLI execution on legacy SVG must create <stem>_<verb>.svg and leave original fixture unmutated."""
        test_file = os.path.join(self.temp_dir, "test_legacy_copy.svg")
        with open(self.fixtures["bare"], "r", encoding="utf-8") as f:
            original_content = f.read()
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(original_content)

        cmd = [
            sys.executable,
            os.path.join(SCRIPTS_DIR, "refinement_verbs.py"),
            "bolder",
            "--input", test_file
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 0, f"CLI command failed: {proc.stderr}")

        # Derived file must exist and be valid
        derived_file = os.path.join(self.temp_dir, "test_legacy_copy_bolder.svg")
        self.assertTrue(os.path.exists(derived_file))
        res = validate_svg_file(derived_file)
        self.assertTrue(res.is_valid)
        self.assertEqual(len(res.errors), 0)
        self.assertEqual(len(res.warnings), 0)

        # Original file must remain untouched
        with open(test_file, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), original_content)

    def test_cli_refinement_in_place_explicit_overwrite(self):
        """CLI with --in-place must cleanly overwrite the legacy file with compliant markup."""
        test_file = os.path.join(self.temp_dir, "inplace_legacy.svg")
        with open(self.fixtures["early_beta"], "r", encoding="utf-8") as f:
            original_content = f.read()
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(original_content)

        cmd = [
            sys.executable,
            os.path.join(SCRIPTS_DIR, "refinement_verbs.py"),
            "upgrade",
            "--input", test_file,
            "--in-place"
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 0, f"CLI in-place failed: {proc.stderr}")

        # Overwritten file must now be fully compliant
        res = validate_svg_file(test_file)
        self.assertTrue(res.is_valid)
        self.assertEqual(len(res.errors), 0)
        self.assertEqual(len(res.warnings), 0)


if __name__ == "__main__":
    unittest.main()
