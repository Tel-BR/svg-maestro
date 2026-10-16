#!/usr/bin/env python3
"""
SVG Maestro - Core Linter Test Suite
Validates programmatic API and CLI behavior of scripts/validate_svg.py across
the full fixture matrix (namespaces, semantic layers, defs hygiene,
wrapper pattern isolation, CSS transform contracts, and error handling).
"""

import os
import sys
import json
import unittest
import subprocess

# Ensure repo root and scripts are in sys.path
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TESTS_DIR, ".."))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
FIXTURES_DIR = os.path.join(TESTS_DIR, "fixtures")

if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from validate_svg import validate_svg_file, ValidationResult


class TestValidationLinterAPI(unittest.TestCase):
    """Unit tests verifying validate_svg_file() programmatic outputs and codes."""

    def fixture(self, filename):
        return os.path.join(FIXTURES_DIR, filename)

    def test_valid_multilayer_fixture(self):
        result = validate_svg_file(self.fixture("valid_multilayer.svg"))
        self.assertTrue(result.is_valid, f"Expected valid, got errors: {result.errors}")
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.warnings), 0)
        self.assertEqual(result.stats["layers_count"], 4)
        self.assertTrue(result.stats["has_viewbox"])
        self.assertTrue(result.stats["has_inkscape_ns"])

    def test_existing_test_card(self):
        card_path = os.path.join(TESTS_DIR, "test_card.svg")
        result = validate_svg_file(card_path)
        self.assertTrue(result.is_valid, f"Expected valid, got errors: {result.errors}")
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.warnings), 0)
        self.assertEqual(result.stats["layers_count"], 4)

    def test_missing_inkscape_namespace(self):
        result = validate_svg_file(self.fixture("missing_inkscape_ns.svg"))
        self.assertFalse(result.is_valid)
        error_codes = [e["code"] for e in result.errors]
        self.assertIn("MISSING_INKSCAPE_NS", error_codes)

    def test_missing_semantic_layers(self):
        result = validate_svg_file(self.fixture("missing_layers.svg"))
        self.assertFalse(result.is_valid)
        error_codes = [e["code"] for e in result.errors]
        self.assertIn("NO_INKSCAPE_LAYERS", error_codes)
        self.assertEqual(result.stats["layers_count"], 0)

    def test_wrapper_pattern_collision(self):
        result = validate_svg_file(self.fixture("wrapper_collision.svg"))
        self.assertTrue(result.is_valid, "Warnings should not mark document invalid unless strict")
        self.assertEqual(len(result.errors), 0)
        warning_codes = [w["code"] for w in result.warnings]
        self.assertIn("WRAPPER_PATTERN_COLLISION", warning_codes)
        warning_entry = next(w for w in result.warnings if w["code"] == "WRAPPER_PATTERN_COLLISION")
        self.assertEqual(warning_entry.get("tag"), "circle")

    def test_missing_transform_box(self):
        result = validate_svg_file(self.fixture("missing_transform_box.svg"))
        self.assertFalse(result.is_valid)
        error_codes = [e["code"] for e in result.errors]
        self.assertIn("MISSING_TRANSFORM_BOX", error_codes)

    def test_missing_viewbox(self):
        result = validate_svg_file(self.fixture("missing_viewbox.svg"))
        self.assertFalse(result.is_valid)
        error_codes = [e["code"] for e in result.errors]
        self.assertIn("MISSING_VIEWBOX", error_codes)

    def test_invalid_viewbox(self):
        result = validate_svg_file(self.fixture("invalid_viewbox.svg"))
        self.assertFalse(result.is_valid)
        error_codes = [e["code"] for e in result.errors]
        self.assertIn("INVALID_VIEWBOX", error_codes)

    def test_missing_transform_origin_warning(self):
        result = validate_svg_file(self.fixture("missing_transform_origin.svg"))
        self.assertTrue(result.is_valid)
        warning_codes = [w["code"] for w in result.warnings]
        self.assertIn("MISSING_TRANSFORM_ORIGIN", warning_codes)

    def test_unlabeled_layer_warning(self):
        result = validate_svg_file(self.fixture("unlabeled_layer.svg"))
        self.assertTrue(result.is_valid)
        warning_codes = [w["code"] for w in result.warnings]
        self.assertIn("UNLABELED_LAYER", warning_codes)

    def test_generic_def_id_warning(self):
        result = validate_svg_file(self.fixture("generic_def_id.svg"))
        self.assertTrue(result.is_valid)
        warning_codes = [w["code"] for w in result.warnings]
        self.assertIn("GENERIC_DEF_ID", warning_codes)

    def test_missing_def_id_warning(self):
        result = validate_svg_file(self.fixture("missing_def_id.svg"))
        self.assertTrue(result.is_valid)
        warning_codes = [w["code"] for w in result.warnings]
        self.assertIn("MISSING_DEF_ID", warning_codes)

    def test_malformed_xml_error(self):
        result = validate_svg_file(self.fixture("malformed_xml.svg"))
        self.assertFalse(result.is_valid)
        error_codes = [e["code"] for e in result.errors]
        self.assertIn("XML_PARSE_ERROR", error_codes)

    def test_root_not_svg_error(self):
        result = validate_svg_file(self.fixture("root_not_svg.svg"))
        self.assertFalse(result.is_valid)
        error_codes = [e["code"] for e in result.errors]
        self.assertIn("ROOT_NOT_SVG", error_codes)

    def test_file_not_found_error(self):
        result = validate_svg_file(os.path.join(FIXTURES_DIR, "non_existent_file.svg"))
        self.assertFalse(result.is_valid)
        error_codes = [e["code"] for e in result.errors]
        self.assertIn("FILE_NOT_FOUND", error_codes)

    def test_validation_result_serialization(self):
        result = validate_svg_file(self.fixture("valid_multilayer.svg"))
        d = result.to_dict()
        self.assertIn("valid", d)
        self.assertIn("errors", d)
        self.assertIn("warnings", d)
        self.assertIn("stats", d)
        self.assertTrue(d["valid"])
        self.assertEqual(d["errors_count"], 0)
        self.assertEqual(d["warnings_count"], 0)


class TestValidationLinterCLI(unittest.TestCase):
    """Integration tests verifying CLI execution codes and flags."""

    def fixture(self, filename):
        return os.path.join(FIXTURES_DIR, filename)

    def run_linter(self, *args):
        cli_path = os.path.join(SCRIPTS_DIR, "validate_svg.py")
        cmd = [sys.executable, cli_path] + list(args)
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return proc

    def test_cli_valid_document_exits_zero(self):
        proc = self.run_linter(self.fixture("valid_multilayer.svg"))
        self.assertEqual(proc.returncode, 0, f"STDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
        self.assertIn("[PASS] VALID", proc.stdout)

    def test_cli_invalid_document_exits_one(self):
        proc = self.run_linter(self.fixture("missing_inkscape_ns.svg"))
        self.assertEqual(proc.returncode, 1, f"Expected returncode 1, got {proc.returncode}")
        self.assertIn("[FAIL] INVALID", proc.stdout)
        self.assertIn("MISSING_INKSCAPE_NS", proc.stdout)

    def test_cli_missing_layers_exits_one(self):
        proc = self.run_linter(self.fixture("missing_layers.svg"))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("NO_INKSCAPE_LAYERS", proc.stdout)

    def test_cli_missing_transform_box_exits_one(self):
        proc = self.run_linter(self.fixture("missing_transform_box.svg"))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("MISSING_TRANSFORM_BOX", proc.stdout)

    def test_cli_wrapper_collision_exits_zero_by_default(self):
        proc = self.run_linter(self.fixture("wrapper_collision.svg"))
        self.assertEqual(proc.returncode, 0)
        self.assertIn("[PASS] VALID", proc.stdout)
        self.assertIn("WRAPPER_PATTERN_COLLISION", proc.stdout)

    def test_cli_wrapper_collision_with_strict_exits_one(self):
        proc = self.run_linter(self.fixture("wrapper_collision.svg"), "--strict")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("[FAIL] INVALID", proc.stdout)
        self.assertIn("WRAPPER_PATTERN_COLLISION", proc.stdout)

    def test_cli_json_output_valid(self):
        proc = self.run_linter(self.fixture("valid_multilayer.svg"), "--json")
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        self.assertTrue(data["valid"])
        self.assertEqual(data["errors_count"], 0)
        self.assertEqual(data["warnings_count"], 0)
        self.assertEqual(data["stats"]["layers_count"], 4)

    def test_cli_json_output_invalid(self):
        proc = self.run_linter(self.fixture("missing_transform_box.svg"), "--json")
        self.assertEqual(proc.returncode, 1)
        data = json.loads(proc.stdout)
        self.assertFalse(data["valid"])
        self.assertEqual(data["errors_count"], 1)
        self.assertEqual(data["errors"][0]["code"], "MISSING_TRANSFORM_BOX")

    def test_cli_file_not_found_exits_one(self):
        proc = self.run_linter(os.path.join(FIXTURES_DIR, "non_existent_file.svg"))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("FILE_NOT_FOUND", proc.stdout)


if __name__ == "__main__":
    unittest.main()
