#!/usr/bin/env python3
"""
SVG Maestro - Interactive Briefing Protocol Test Suite
Tests for scripts/briefing.py:
- Verification of ask_question options format (recommended default first, direct response phrasing)
- Multilingual support (PT-BR and EN)
- Generation and parsing of binding BRIEF.md files
- Validation checks for required dimensions and failure diagnostic codes
- CLI commands and JSON export
"""

import os
import sys
import json
import unittest
import subprocess
import tempfile

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TESTS_DIR, ".."))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")

if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from briefing import (
    build_briefing_questions,
    generate_brief_markdown,
    parse_brief_content,
    validate_brief_content,
    validate_brief_file,
    BriefValidationResult,
    VIEWPORTS,
    SURFACE_MODES,
    MOTION_PROFILES,
    HANDOFF_TARGETS,
)


class TestBriefingElicitationProtocol(unittest.TestCase):
    """Verifies that ask_question payloads conform to agent tool contracts."""

    def test_english_questions_payload_structure(self):
        payload = build_briefing_questions(language="en")
        self.assertIn("questions", payload)
        questions = payload["questions"]
        self.assertEqual(len(questions), 4, "Must prompt across 4 core vector dimensions")

        dimension_keys = [q.get("dimension") for q in questions]
        self.assertIn("viewport", dimension_keys)
        self.assertIn("mode", dimension_keys)
        self.assertIn("motion", dimension_keys)
        self.assertIn("handoff", dimension_keys)

        for q in questions:
            self.assertIn("question", q)
            self.assertIn("options", q)
            self.assertIn("is_multi_select", q)
            self.assertFalse(q["is_multi_select"], "Each core dimension requires single decisive choice")
            self.assertGreaterEqual(len(q["options"]), 2, "Each question must have at least 2 options")
            
            # Recommendation rules
            first_opt = q["options"][0]
            self.assertTrue(
                first_opt.startswith("(Recommended)"),
                f"First option must begin with '(Recommended)': {first_opt}"
            )
            for other_opt in q["options"][1:]:
                self.assertFalse(
                    other_opt.startswith("(Recommended)"),
                    f"Subsequent option should not be marked recommended: {other_opt}"
                )

            # Absence of forbidden phrases
            self.assertNotIn("select all that apply", q["question"].lower())
            for opt in q["options"]:
                self.assertNotEqual(opt.strip().lower(), "other")
                self.assertFalse(opt.lower().startswith("other:"))

    def test_portuguese_questions_payload_structure(self):
        for lang_code in ["pt", "pt-br", "pt-BR"]:
            payload = build_briefing_questions(language=lang_code)
            self.assertIn("questions", payload)
            questions = payload["questions"]
            self.assertEqual(len(questions), 4)

            for q in questions:
                first_opt = q["options"][0]
                self.assertTrue(
                    first_opt.startswith("(Recomendado)"),
                    f"In PT, first option must begin with '(Recomendado)': {first_opt}"
                )
                self.assertNotIn("select all that apply", q["question"].lower())
                self.assertNotIn("selecione todas", q["question"].lower())
                for opt in q["options"]:
                    self.assertNotEqual(opt.strip().lower(), "outro")

    def test_custom_recommended_defaults(self):
        custom_defaults = {
            "viewport": "telemetry_card",
            "mode": "operate",
            "motion": "static",
            "handoff": "powerbi_dax",
        }
        payload = build_briefing_questions(language="en", defaults=custom_defaults)
        questions = {q["dimension"]: q for q in payload["questions"]}

        # Check that telemetry card is recommended
        self.assertTrue(questions["viewport"]["options"][0].startswith("(Recommended)"))
        self.assertIn("Telemetry Card", questions["viewport"]["options"][0])

        # Check that operate is recommended
        self.assertTrue(questions["mode"]["options"][0].startswith("(Recommended)"))
        self.assertIn("Operate", questions["mode"]["options"][0])

        # Check that static is recommended
        self.assertTrue(questions["motion"]["options"][0].startswith("(Recommended)"))
        self.assertIn("Static", questions["motion"]["options"][0])

        # Check that power bi dax is recommended
        self.assertTrue(questions["handoff"]["options"][0].startswith("(Recommended)"))
        self.assertIn("Power BI DAX", questions["handoff"]["options"][0])

    def test_options_direct_response_phrasing(self):
        payload = build_briefing_questions(language="en")
        for q in payload["questions"]:
            for opt in q["options"]:
                # Should not phrase as agent actions like "I will create..."
                self.assertFalse(opt.startswith("I will"), f"Option must be direct user response: {opt}")
                self.assertFalse(opt.startswith("Agent will"), f"Option must be direct user response: {opt}")


class TestBriefGenerationAndMarkdown(unittest.TestCase):
    """Verifies generation of structured, binding BRIEF.md documents."""

    def test_generate_brief_markdown_english(self):
        brief_md = generate_brief_markdown(
            asset_name="Cyber Stream Frame",
            viewport="webcam_16_9",
            mode="experience",
            motion="radar_pulse",
            handoff="obs_browser_source",
            language="en",
            accent_color="#00f0ff",
            secondary_accent="#8a2be2",
        )
        self.assertIn("# Vector Design Brief: Cyber Stream Frame", brief_md)
        self.assertIn("Surface Viewport", brief_md)
        self.assertIn("1920x1080", brief_md)
        self.assertIn("Surface Mode", brief_md)
        self.assertIn("Experience", brief_md)
        self.assertIn("Motion Profile", brief_md)
        self.assertIn("Ambient Radar Spin / Breathing Pulse", brief_md)
        self.assertIn("Handoff Target", brief_md)
        self.assertIn("OBS Studio Browser Source", brief_md)
        self.assertIn("#00f0ff", brief_md)
        self.assertIn("layer-background", brief_md)
        self.assertIn("transform-box: fill-box", brief_md)

    def test_generate_brief_markdown_portuguese(self):
        brief_md = generate_brief_markdown(
            asset_name="Cartao Telemetria Financeira",
            viewport="telemetry_card",
            mode="operate",
            motion="static",
            handoff="powerbi_dax",
            language="pt-br",
        )
        self.assertIn("# Briefing de Design Vetorial: Cartao Telemetria Financeira", brief_md)
        self.assertIn("800x500", brief_md)
        self.assertIn("Operate", brief_md)
        self.assertIn("Static", brief_md)
        self.assertIn("Power BI DAX", brief_md)
        self.assertIn("transform-box: fill-box", brief_md)


class TestBriefParsingAndValidation(unittest.TestCase):
    """Verifies that validate_brief correctly parses and validates binding dimensions."""

    def setUp(self):
        self.valid_brief_content = generate_brief_markdown(
            asset_name="Mission Telemetry",
            viewport="telemetry_card",
            mode="operate",
            motion="line_tracing",
            handoff="web_dom",
            language="en",
        )

    def test_valid_brief_validation_success(self):
        result = validate_brief_content(self.valid_brief_content)
        self.assertTrue(result.is_valid, f"Expected valid brief, got errors: {result.errors}")
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(result.dimensions["mode"], "Operate")
        self.assertEqual(result.dimensions["viewport_width"], 800)
        self.assertEqual(result.dimensions["viewport_height"], 500)
        self.assertEqual(result.dimensions["handoff"], "Web DOM / HTML")

    def test_missing_viewport_error(self):
        bad_content = self.valid_brief_content.replace("Surface Viewport", "Target Screen")
        result = validate_brief_content(bad_content)
        self.assertFalse(result.is_valid)
        error_codes = [e["code"] for e in result.errors]
        self.assertIn("MISSING_SURFACE_VIEWPORT", error_codes)

    def test_missing_mode_error(self):
        bad_content = self.valid_brief_content.replace("Surface Mode", "Visual Style")
        result = validate_brief_content(bad_content)
        self.assertFalse(result.is_valid)
        error_codes = [e["code"] for e in result.errors]
        self.assertIn("MISSING_SURFACE_MODE", error_codes)

    def test_missing_motion_profile_error(self):
        bad_content = self.valid_brief_content.replace("Motion Profile", "Movement Style")
        result = validate_brief_content(bad_content)
        self.assertFalse(result.is_valid)
        error_codes = [e["code"] for e in result.errors]
        self.assertIn("MISSING_MOTION_PROFILE", error_codes)

    def test_missing_handoff_target_error(self):
        bad_content = self.valid_brief_content.replace("Handoff Target", "Export Target")
        result = validate_brief_content(bad_content)
        self.assertFalse(result.is_valid)
        error_codes = [e["code"] for e in result.errors]
        self.assertIn("MISSING_HANDOFF_TARGET", error_codes)

    def test_invalid_mode_value_error(self):
        bad_content = self.valid_brief_content.replace("Operate", "CartoonFunStyle")
        result = validate_brief_content(bad_content)
        self.assertFalse(result.is_valid)
        error_codes = [e["code"] for e in result.errors]
        self.assertIn("INVALID_SURFACE_MODE", error_codes)

    def test_file_validation_with_tempfile(self):
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".md", encoding="utf-8") as f:
            f.write(self.valid_brief_content)
            temp_path = f.name

        try:
            result = validate_brief_file(temp_path)
            self.assertTrue(result.is_valid)
            self.assertEqual(result.file_path, temp_path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_template_reference_file_passes_validation(self):
        template_path = os.path.join(REPO_ROOT, "templates", "BRIEF.template.md")
        if os.path.exists(template_path):
            result = validate_brief_file(template_path)
            self.assertTrue(result.is_valid, f"Template file must be valid: {result.errors}")


class TestBriefingCLI(unittest.TestCase):
    """Verifies command line interface execution."""

    def run_cli(self, *args):
        cli_path = os.path.join(SCRIPTS_DIR, "briefing.py")
        cmd = [sys.executable, cli_path] + list(args)
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def test_cli_questions_json_en(self):
        proc = self.run_cli("questions", "--lang", "en", "--json")
        self.assertEqual(proc.returncode, 0, f"Error: {proc.stderr}")
        data = json.loads(proc.stdout)
        self.assertIn("questions", data)
        self.assertEqual(len(data["questions"]), 4)

    def test_cli_questions_json_pt(self):
        proc = self.run_cli("questions", "--lang", "pt", "--json")
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        self.assertIn("questions", data)
        self.assertTrue(data["questions"][0]["options"][0].startswith("(Recomendado)"))

    def test_cli_create_and_validate(self):
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".md", encoding="utf-8") as f:
            temp_path = f.name

        try:
            # Create brief via CLI
            proc_create = self.run_cli(
                "create",
                "--name", "CLI Stream Overlay",
                "--viewport", "webcam_16_9",
                "--mode", "experience",
                "--motion", "radar_pulse",
                "--handoff", "obs_browser_source",
                "--output", temp_path,
            )
            self.assertEqual(proc_create.returncode, 0, f"Create stderr: {proc_create.stderr}")
            self.assertTrue(os.path.exists(temp_path))

            # Validate brief via CLI
            proc_val = self.run_cli("validate", temp_path)
            self.assertEqual(proc_val.returncode, 0, f"Validate stdout: {proc_val.stdout}\nstderr: {proc_val.stderr}")
            self.assertIn("[PASS] VALID BRIEF", proc_val.stdout)

            # Validate with JSON output
            proc_val_json = self.run_cli("validate", temp_path, "--json")
            self.assertEqual(proc_val_json.returncode, 0)
            val_data = json.loads(proc_val_json.stdout)
            self.assertTrue(val_data["valid"])
            self.assertEqual(val_data["dimensions"]["mode"], "Experience")

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
