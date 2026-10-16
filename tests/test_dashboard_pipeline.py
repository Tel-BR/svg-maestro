#!/usr/bin/env python3
"""
SVG Maestro - Dashboard Widgets & Power BI DAX Pipeline Test Suite
Validates that generated telemetry cards and DAX measures in Operate mode
adhere to the system specification:
- Golden ratio proportions (800x494 ~ 1.618)
- Zero linter errors and zero warnings under strict validation
- Strict Inkscape semantic layers (layer-background, layer-grid, layer-telemetry, layer-typography)
- Decoupled typography (<text> tags in layer-typography, no text-to-path)
- Strict Wrapper Pattern and CSS transform contracts (transform-box: fill-box; transform-origin: center;)
- DAX escaping rules (data:image/svg+xml;utf8,, %23 hex replacement, double quotes escaping, dynamic interpolation)
- Full CLI and programmatic interface testing across all themes
"""

import os
import sys
import re
import shutil
import tempfile
import unittest
import subprocess
import xml.etree.ElementTree as ET

# Ensure repo root and scripts are in sys.path
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TESTS_DIR, ".."))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
EXAMPLES_DASHBOARD_DIR = os.path.join(REPO_ROOT, "examples", "dashboard")

if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from validate_svg import validate_svg_file
from dashboard_pipeline import (
    generate_telemetry_card,
    convert_svg_to_dax_measure,
    export_dashboard_assets,
    get_theme,
    THEMES
)


class TestDashboardWidgetsAndDAXPipeline(unittest.TestCase):
    """Test suite for Dashboard Widgets and Power BI DAX Pipeline."""

    @classmethod
    def setUpClass(cls):
        """Ensure canonical examples/dashboard assets are generated before tests run."""
        cls.svg_path = os.path.join(EXAMPLES_DASHBOARD_DIR, "telemetry_card.svg")
        cls.dax_path = os.path.join(EXAMPLES_DASHBOARD_DIR, "telemetry_card.dax")

        if not os.path.exists(cls.svg_path) or not os.path.exists(cls.dax_path):
            export_dashboard_assets(output_dir=EXAMPLES_DASHBOARD_DIR, theme_name="dark_slate", validate=False)

    def test_canonical_card_passes_strict_linter_validation(self):
        """Canonical telemetry_card.svg must pass validate_svg_file with 0 errors and 0 warnings."""
        result = validate_svg_file(self.svg_path)
        self.assertTrue(result.is_valid, f"Telemetry card failed validation: {result.errors}")
        self.assertEqual(len(result.errors), 0, f"Expected 0 errors, got: {result.errors}")
        self.assertEqual(len(result.warnings), 0, f"Expected 0 warnings, got: {result.warnings}")

    def test_golden_ratio_proportions_and_viewbox(self):
        """Telemetry card must have golden ratio aspect ratio (approx 1.618) and viewBox 0 0 800 494."""
        tree = ET.parse(self.svg_path)
        root = tree.getroot()
        viewbox = root.attrib.get("viewBox", "")
        parts = [float(p) for p in viewbox.split()]
        self.assertEqual(len(parts), 4, f"viewBox should have 4 values: {viewbox}")
        min_x, min_y, width, height = parts
        self.assertEqual(min_x, 0.0)
        self.assertEqual(min_y, 0.0)
        self.assertEqual(width, 800.0)
        self.assertEqual(height, 494.0)
        # Check Golden Ratio approximation (800 / 494 = 1.6194, within 0.15% of phi = 1.61803)
        aspect_ratio = width / height
        self.assertAlmostEqual(aspect_ratio, 1.618, delta=0.005)

    def test_semantic_inkscape_layers_present(self):
        """Telemetry card must declare the 4 required Inkscape layers with exact IDs and labels."""
        tree = ET.parse(self.svg_path)
        root = tree.getroot()

        required_layers = {
            "layer-background": "Card Background & Chassis",
            "layer-grid": "Data Grid & Markings",
            "layer-telemetry": "Telemetry & Visuals",
            "layer-typography": "Typography & Metrics"
        }

        found_layers = {}
        for g in root.iter("{http://www.w3.org/2000/svg}g"):
            groupmode = g.attrib.get("{http://www.inkscape.org/namespaces/inkscape}groupmode")
            if groupmode == "layer":
                lid = g.attrib.get("id")
                label = g.attrib.get("{http://www.inkscape.org/namespaces/inkscape}label")
                found_layers[lid] = label

        for expected_id in required_layers:
            self.assertIn(expected_id, found_layers, f"Missing semantic layer: {expected_id}")
            self.assertIsNotNone(found_layers[expected_id], f"Layer {expected_id} has no label")

    def test_decoupled_typography_contract(self):
        """Typography must be decoupled: all <text> nodes must reside in layer-typography, none as raw paths."""
        tree = ET.parse(self.svg_path)
        root = tree.getroot()

        # 1. Locate layer-typography
        typography_layer = None
        for g in root.iter("{http://www.w3.org/2000/svg}g"):
            if g.attrib.get("id") == "layer-typography":
                typography_layer = g
                break

        self.assertIsNotNone(typography_layer, "layer-typography group not found")

        # 2. Count text nodes inside typography layer
        text_nodes_in_layer = list(typography_layer.iter("{http://www.w3.org/2000/svg}text"))
        self.assertGreaterEqual(len(text_nodes_in_layer), 10, "Expected at least 10 decoupled text elements")

        # 3. Verify NO text nodes exist outside layer-typography
        all_text_nodes = list(root.iter("{http://www.w3.org/2000/svg}text"))
        self.assertEqual(
            len(all_text_nodes),
            len(text_nodes_in_layer),
            "All <text> nodes must reside exclusively inside layer-typography"
        )

        # 4. Check that KPI value and change are present in text nodes
        text_contents = [t.text for t in text_nodes_in_layer if t.text]
        self.assertIn("$1,284,500", text_contents, "Primary KPI readout must be present as text")
        self.assertIn("+14.2% ↑", text_contents, "KPI change readout must be present as text")
        self.assertIn("TOTAL SYSTEM THROUGHPUT", text_contents, "KPI label must be present as text")

    def test_wrapper_pattern_and_css_transform_contracts(self):
        """Motion elements must adhere to the Wrapper Pattern and CSS transform-box: fill-box contract."""
        with open(self.svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()

        # Check CSS transform contract
        self.assertIn("transform-box: fill-box;", svg_content)
        self.assertIn("transform-origin: center;", svg_content)

        # Parse XML tree
        tree = ET.parse(self.svg_path)
        root = tree.getroot()

        # Find all elements with anim- classes
        animated_wrappers = []
        for elem in root.iter():
            cls_val = elem.attrib.get("class", "")
            if "anim-" in cls_val:
                tag = elem.tag.split("}")[-1]
                animated_wrappers.append((tag, cls_val, elem))

        self.assertGreaterEqual(len(animated_wrappers), 3, "Expected at least 3 animated wrapper elements")

        # Every element using an anim- class that transforms MUST be a <g> tag (Wrapper Pattern)
        for tag, cls_val, elem in animated_wrappers:
            self.assertEqual(
                tag, "g",
                f"Element with class '{cls_val}' is <{tag}>, but must be <g> to satisfy the Wrapper Pattern"
            )
            # Must contain a child <g> with inkscape:label for static geometry
            child_geom = elem.find("{http://www.w3.org/2000/svg}g")
            self.assertIsNotNone(
                child_geom,
                f"Animated wrapper <g class='{cls_val}'> must encapsulate a child static geometry <g>"
            )
            label = child_geom.attrib.get("{http://www.inkscape.org/namespaces/inkscape}label")
            self.assertTrue(bool(label), f"Child static geometry group must have inkscape:label")

    def test_radar_sweep_and_sparkline_telemetry_elements(self):
        """Card must contain a glowing radar sweep indicator and sparkline trendline."""
        with open(self.svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()

        # Radar sweep elements
        self.assertIn("anim-radar-sweep", svg_content)
        self.assertIn("geom-radar-sweep", svg_content)
        self.assertIn("grad-radar-sweep", svg_content)
        self.assertIn("ACTIVE SCAN", svg_content)

        # Sparkline elements
        self.assertIn("grad-sparkline-area", svg_content)
        self.assertIn("geom-spark-pulse", svg_content)
        self.assertIn("TELEMETRY TIMELINE", svg_content)

    def test_canonical_dax_measure_format_and_escaping(self):
        """telemetry_card.dax must satisfy Power BI DAX URL escaping rules."""
        with open(self.dax_path, "r", encoding="utf-8") as f:
            dax_content = f.read()

        # 1. Measure declaration
        self.assertTrue(
            dax_content.startswith("TelemetryCard ="),
            f"DAX measure must begin with 'TelemetryCard =', got: {dax_content[:30]}"
        )

        # 2. data:image/svg+xml;utf8, prefix
        self.assertIn("data:image/svg+xml;utf8,", dax_content)

        # 3. No unescaped '#' outside of comments
        non_comment_lines = [line for line in dax_content.splitlines() if not line.strip().startswith("--")]
        for idx, line in enumerate(non_comment_lines):
            # Check for '#' not in comments
            code_part = line.split("--")[0]
            self.assertNotIn(
                "#", code_part,
                f"Found unescaped '#' on line {idx + 1}: {code_part}"
            )

        # 4. Escaped hex colors (%23)
        self.assertIn("%230a0e17", dax_content, "Background hex #0a0e17 must be encoded as %230a0e17")
        self.assertIn("%2300f0ff", dax_content, "Primary cyan hex #00f0ff must be encoded as %2300f0ff")

        # 5. Escaped double quotes ("")
        self.assertIn('viewBox=""0 0 800 494""', dax_content)
        self.assertIn('xmlns=""http://www.w3.org/2000/svg""', dax_content)

        # 6. Dynamic measure interpolation syntax
        self.assertIn("_KpiValue", dax_content)
        self.assertIn("_KpiChange", dax_content)
        self.assertIn("_KpiLabel", dax_content)
        self.assertIn('" & _KpiValue & "', dax_content)
        self.assertIn('" & _KpiChange & "', dax_content)
        self.assertIn('" & _KpiLabel & "', dax_content)

        # 7. VAR and RETURN contract
        self.assertIn("VAR SvgData =", dax_content)
        self.assertIn("RETURN", dax_content)
        self.assertIn("SvgData", dax_content)

    def test_convert_svg_to_dax_static_mode(self):
        """convert_svg_to_dax_measure in static mode generates a clean self-contained DAX string."""
        svg = generate_telemetry_card()
        dax = convert_svg_to_dax_measure(svg, measure_name="StaticTelemetryCard", dynamic_vars=None)

        self.assertTrue(dax.startswith("StaticTelemetryCard ="))
        self.assertIn('VAR SvgData = "data:image/svg+xml;utf8," &', dax)
        self.assertIn("RETURN", dax)
        self.assertIn("SvgData", dax)
        self.assertNotIn("#0a0e17", dax)
        self.assertIn("%230a0e17", dax)
        self.assertIn('""', dax)

    def test_convert_svg_to_dax_custom_variables(self):
        """convert_svg_to_dax_measure handles custom variable mappings and definitions."""
        svg = generate_telemetry_card(kpi_value="$999,999", kpi_label="CUSTOM METRIC")
        custom_vars = {"$999,999": "[RevenueMeasure]", "CUSTOM METRIC": "[TitleMeasure]"}
        custom_defs = {
            "KpiVal": "COALESCE([RevenueMeasure], \"$999,999\")",
            "KpiTitle": "COALESCE([TitleMeasure], \"CUSTOM METRIC\")"
        }

        dax = convert_svg_to_dax_measure(
            svg_content=svg,
            measure_name="CustomCard",
            dynamic_vars={"$999,999": "KpiVal", "CUSTOM METRIC": "KpiTitle"},
            var_definitions=custom_defs
        )

        self.assertTrue(dax.startswith("CustomCard ="))
        self.assertIn("VAR KpiVal = COALESCE([RevenueMeasure], \"$999,999\")", dax)
        self.assertIn("VAR KpiTitle = COALESCE([TitleMeasure], \"CUSTOM METRIC\")", dax)
        self.assertIn('" & KpiVal & "', dax)
        self.assertIn('" & KpiTitle & "', dax)

    def test_all_themes_pass_strict_validation(self):
        """Every visual theme palette must generate an SVG that passes strict linter validation."""
        temp_dir = tempfile.mkdtemp()
        try:
            for theme_key in THEMES.keys():
                card_svg = generate_telemetry_card(theme_name=theme_key)
                file_path = os.path.join(temp_dir, f"card_{theme_key}.svg")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(card_svg)

                res = validate_svg_file(file_path)
                self.assertTrue(
                    res.is_valid,
                    f"Theme '{theme_key}' failed validation: {res.errors}"
                )
                self.assertEqual(
                    len(res.errors), 0,
                    f"Theme '{theme_key}' produced errors: {res.errors}"
                )
                self.assertEqual(
                    len(res.warnings), 0,
                    f"Theme '{theme_key}' produced warnings: {res.warnings}"
                )
        finally:
            shutil.rmtree(temp_dir)

    def test_custom_parameters_in_telemetry_card(self):
        """Custom KPI values, labels, and status strings must be rendered into the SVG."""
        custom_svg = generate_telemetry_card(
            kpi_value="$42,000,000",
            kpi_change="+88.5% ↑",
            kpi_label="QUANTUM COMPUTE JOBS",
            scan_label="RADAR 9.6 GHz",
            status_label="SYNCED 100%"
        )

        self.assertIn("$42,000,000", custom_svg)
        self.assertIn("+88.5% ↑", custom_svg)
        self.assertIn("QUANTUM COMPUTE JOBS", custom_svg)
        self.assertIn("RADAR 9.6 GHz", custom_svg)
        self.assertIn("SYNCED 100%", custom_svg)

    def test_cli_card_generation(self):
        """CLI 'card' command must generate a valid SVG file."""
        temp_dir = tempfile.mkdtemp()
        try:
            out_file = os.path.join(temp_dir, "cli_card.svg")
            cmd = [
                sys.executable,
                os.path.join(SCRIPTS_DIR, "dashboard_pipeline.py"),
                "card",
                "--output", out_file,
                "--theme", "obsidian_amber",
                "--kpi-value", "$3,500,000",
                "--kpi-label", "ENTERPRISE PIPELINE"
            ]
            run_res = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(run_res.returncode, 0, f"CLI error: {run_res.stderr}")
            self.assertTrue(os.path.exists(out_file), "CLI did not create output file")

            val_res = validate_svg_file(out_file)
            self.assertTrue(val_res.is_valid)
            self.assertEqual(len(val_res.errors), 0)
            self.assertEqual(len(val_res.warnings), 0)
        finally:
            shutil.rmtree(temp_dir)

    def test_cli_dax_conversion(self):
        """CLI 'dax' command must generate a valid DAX measure file from an SVG."""
        temp_dir = tempfile.mkdtemp()
        try:
            svg_file = os.path.join(temp_dir, "test_input.svg")
            dax_file = os.path.join(temp_dir, "test_output.dax")

            card_svg = generate_telemetry_card()
            with open(svg_file, "w", encoding="utf-8") as f:
                f.write(card_svg)

            cmd = [
                sys.executable,
                os.path.join(SCRIPTS_DIR, "dashboard_pipeline.py"),
                "dax",
                "--input", svg_file,
                "--output", dax_file,
                "--measure-name", "TelemetryMeasure"
            ]
            run_res = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(run_res.returncode, 0, f"CLI error: {run_res.stderr}")
            self.assertTrue(os.path.exists(dax_file), "CLI did not create DAX file")

            with open(dax_file, "r", encoding="utf-8") as f:
                dax_content = f.read()

            self.assertTrue(dax_content.startswith("TelemetryMeasure ="))
            self.assertIn("data:image/svg+xml;utf8,", dax_content)
            self.assertIn("%230a0e17", dax_content)
            self.assertIn("VAR SvgData =", dax_content)
            self.assertIn("RETURN", dax_content)
        finally:
            shutil.rmtree(temp_dir)

    def test_cli_generate_all(self):
        """CLI 'generate-all' command must generate both SVG and DAX files in output dir."""
        temp_dir = tempfile.mkdtemp()
        try:
            cmd = [
                sys.executable,
                os.path.join(SCRIPTS_DIR, "dashboard_pipeline.py"),
                "generate-all",
                "--output-dir", temp_dir,
                "--theme", "matrix_emerald"
            ]
            run_res = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(run_res.returncode, 0, f"CLI error: {run_res.stderr}")

            svg_out = os.path.join(temp_dir, "telemetry_card.svg")
            dax_out = os.path.join(temp_dir, "telemetry_card.dax")

            self.assertTrue(os.path.exists(svg_out))
            self.assertTrue(os.path.exists(dax_out))

            val_res = validate_svg_file(svg_out)
            self.assertTrue(val_res.is_valid)
            self.assertEqual(len(val_res.errors), 0)
            self.assertEqual(len(val_res.warnings), 0)
        finally:
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    unittest.main()
