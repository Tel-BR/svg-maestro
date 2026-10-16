#!/usr/bin/env python3
"""
SVG Maestro - Internationalization and Decoupled Typography Test Suite
Validates multilingual typography contracts, outlined text detection,
native SVG <switch> with systemLanguage inspection, and Inkscape text editability.
"""

import os
import sys
import json
import unittest
import subprocess
import xml.etree.ElementTree as ET

# Ensure repo root and scripts are in sys.path
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TESTS_DIR, ".."))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
EXAMPLES_DIR = os.path.join(REPO_ROOT, "examples")

if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from validate_svg import validate_svg_file, ValidationResult


class TestTypographyLinterRules(unittest.TestCase):
    """Tests validate_svg.py diagnostics for typography layers and <switch> elements."""

    def setUp(self):
        self.temp_files = []

    def tearDown(self):
        for path in self.temp_files:
            if os.path.exists(path):
                os.remove(path)

    def create_temp_svg(self, content):
        import tempfile
        fd, path = tempfile.mkstemp(suffix=".svg")
        os.close(fd)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        self.temp_files.append(path)
        return path

    def test_outlined_text_warning_in_typography_layer(self):
        """A typography layer with paths/shapes but zero <text> or <switch> flags OUTLINED_TEXT_WARNING."""
        svg_content = """<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     viewBox="0 0 500 300">
  <g inkscape:groupmode="layer" id="layer-bg" inkscape:label="Background">
    <rect width="500" height="300" fill="#000" />
  </g>
  <g inkscape:groupmode="layer" id="layer-typography" inkscape:label="Typography">
    <!-- Path representing outlined text glyphs rather than editable <text> -->
    <path d="M 50,50 L 60,70 L 40,70 Z" fill="#fff" />
  </g>
</svg>"""
        path = self.create_temp_svg(svg_content)
        result = validate_svg_file(path)
        warning_codes = [w["code"] for w in result.warnings]
        self.assertIn("OUTLINED_TEXT_WARNING", warning_codes)
        warning_entry = next(w for w in result.warnings if w["code"] == "OUTLINED_TEXT_WARNING")
        self.assertIn("Typography layer", warning_entry["message"])

    def test_valid_typography_layer_with_text_nodes(self):
        """A typography layer containing semantic <text> nodes produces no OUTLINED_TEXT_WARNING."""
        svg_content = """<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     viewBox="0 0 500 300">
  <g inkscape:groupmode="layer" id="layer-bg" inkscape:label="Background">
    <rect width="500" height="300" fill="#000" />
  </g>
  <g inkscape:groupmode="layer" id="layer-typography" inkscape:label="Typography &amp; Labels">
    <text x="50" y="50" fill="#fff" font-family="sans-serif" font-size="16">SYSTEM STATUS</text>
  </g>
</svg>"""
        path = self.create_temp_svg(svg_content)
        result = validate_svg_file(path)
        warning_codes = [w["code"] for w in result.warnings]
        self.assertNotIn("OUTLINED_TEXT_WARNING", warning_codes)
        self.assertEqual(result.stats["text_nodes_count"], 1)

    def test_switch_empty_warning(self):
        """An empty <switch> element flags SWITCH_EMPTY."""
        svg_content = """<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     viewBox="0 0 500 300">
  <g inkscape:groupmode="layer" id="layer-bg" inkscape:label="Background">
    <rect width="500" height="300" fill="#000" />
  </g>
  <g inkscape:groupmode="layer" id="layer-typography" inkscape:label="Typography">
    <switch></switch>
  </g>
</svg>"""
        path = self.create_temp_svg(svg_content)
        result = validate_svg_file(path)
        warning_codes = [w["code"] for w in result.warnings]
        self.assertIn("SWITCH_EMPTY", warning_codes)

    def test_switch_missing_fallback_warning(self):
        """A <switch> where all children have systemLanguage flags SWITCH_MISSING_FALLBACK."""
        svg_content = """<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     viewBox="0 0 500 300">
  <g inkscape:groupmode="layer" id="layer-bg" inkscape:label="Background">
    <rect width="500" height="300" fill="#000" />
  </g>
  <g inkscape:groupmode="layer" id="layer-typography" inkscape:label="Typography">
    <switch>
      <text systemLanguage="pt" x="50" y="50">OLÁ</text>
      <text systemLanguage="es" x="50" y="50">HOLA</text>
    </switch>
  </g>
</svg>"""
        path = self.create_temp_svg(svg_content)
        result = validate_svg_file(path)
        warning_codes = [w["code"] for w in result.warnings]
        self.assertIn("SWITCH_MISSING_FALLBACK", warning_codes)

    def test_switch_fallback_order_warning(self):
        """A fallback child without systemLanguage placed before the last child flags SWITCH_FALLBACK_ORDER."""
        svg_content = """<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     viewBox="0 0 500 300">
  <g inkscape:groupmode="layer" id="layer-bg" inkscape:label="Background">
    <rect width="500" height="300" fill="#000" />
  </g>
  <g inkscape:groupmode="layer" id="layer-typography" inkscape:label="Typography">
    <switch>
      <text x="50" y="50">HELLO</text>
      <text systemLanguage="pt" x="50" y="50">OLÁ</text>
    </switch>
  </g>
</svg>"""
        path = self.create_temp_svg(svg_content)
        result = validate_svg_file(path)
        warning_codes = [w["code"] for w in result.warnings]
        self.assertIn("SWITCH_FALLBACK_ORDER", warning_codes)
        self.assertIn("SWITCH_MISSING_FALLBACK", warning_codes)

    def test_valid_multilingual_switch(self):
        """A properly structured <switch> with systemLanguage and fallback passes with zero warnings."""
        svg_content = """<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     viewBox="0 0 500 300">
  <g inkscape:groupmode="layer" id="layer-bg" inkscape:label="Background">
    <rect width="500" height="300" fill="#000" />
  </g>
  <g inkscape:groupmode="layer" id="layer-typography" inkscape:label="Typography">
    <switch>
      <text systemLanguage="pt" x="50" y="50">TELEMETRIA AO VIVO</text>
      <text systemLanguage="es" x="50" y="50">TELEMETRÍA EN VIVO</text>
      <text x="50" y="50">LIVE TELEMETRY</text>
    </switch>
  </g>
</svg>"""
        path = self.create_temp_svg(svg_content)
        result = validate_svg_file(path)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.warnings), 0)
        self.assertEqual(result.stats["switch_nodes_count"], 1)
        self.assertEqual(result.stats["text_nodes_count"], 3)


class TestMultilingualCardAsset(unittest.TestCase):
    """Validates the production asset examples/i18n/multilingual_card.svg."""

    @classmethod
    def setUpClass(cls):
        cls.asset_path = os.path.join(EXAMPLES_DIR, "i18n", "multilingual_card.svg")
        if not os.path.exists(cls.asset_path):
            raise FileNotFoundError(f"Missing asset: {cls.asset_path}")

        tree = ET.parse(cls.asset_path)
        cls.root = tree.getroot()

    def test_asset_file_exists(self):
        self.assertTrue(os.path.isfile(self.asset_path))

    def test_passes_strict_linter_validation(self):
        """The multilingual card must pass validate_svg.py --strict with 0 errors and 0 warnings."""
        result = validate_svg_file(self.asset_path)
        self.assertTrue(result.is_valid, f"Validation errors: {result.errors}")
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.warnings), 0, f"Validation warnings: {result.warnings}")

    def test_cli_strict_execution_zero_exit_code(self):
        cli_path = os.path.join(SCRIPTS_DIR, "validate_svg.py")
        proc = subprocess.run(
            [sys.executable, cli_path, self.asset_path, "--strict", "--json"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.assertEqual(proc.returncode, 0, f"STDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
        data = json.loads(proc.stdout)
        self.assertTrue(data["valid"])
        self.assertEqual(data["errors_count"], 0)
        self.assertEqual(data["warnings_count"], 0)

    def test_root_attributes_and_namespaces(self):
        tag = self.root.tag.split("}")[-1]
        self.assertEqual(tag, "svg")
        self.assertEqual(self.root.attrib.get("viewBox"), "0 0 800 500")

        with open(self.asset_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
        self.assertIn('xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"', raw_text)

    def test_semantic_layers_structure(self):
        """Card must contain the 4 canonical semantic layers."""
        inkscape_groupmode = "{http://www.inkscape.org/namespaces/inkscape}groupmode"
        inkscape_label = "{http://www.inkscape.org/namespaces/inkscape}label"

        layers = [
            g for g in self.root.findall("{http://www.w3.org/2000/svg}g") + self.root.findall("g")
            if g.attrib.get(inkscape_groupmode) == "layer" or g.attrib.get("inkscape:groupmode") == "layer"
        ]
        self.assertEqual(len(layers), 4)

        labels = [
            g.attrib.get(inkscape_label) or g.attrib.get("inkscape:label")
            for g in layers
        ]
        self.assertIn("Background Chassis", labels)
        self.assertIn("Structural Geometry", labels)
        self.assertIn("Dynamic Motion", labels)
        self.assertIn("Multilingual Typography", labels)

    def test_multilingual_typography_layer_content(self):
        """Typography layer must contain semantic <text> nodes and valid <switch> elements."""
        typo_layer = None
        for g in self.root.iter():
            if g.attrib.get("id") == "layer-typography":
                typo_layer = g
                break
        self.assertIsNotNone(typo_layer, "Layer 'layer-typography' not found")

        # Find switches inside typography layer
        switches = typo_layer.findall("{http://www.w3.org/2000/svg}switch") + typo_layer.findall("switch")
        self.assertGreaterEqual(len(switches), 5, "Expected at least 5 multilingual <switch> nodes")

        for sw in switches:
            children = list(sw)
            self.assertGreaterEqual(len(children), 2, "Each <switch> must have at least language alternative and fallback")

            # Check that Portuguese is supported
            languages = [c.attrib.get("systemLanguage") for c in children if c.attrib.get("systemLanguage")]
            self.assertIn("pt", languages, "Expected 'pt' (Portuguese) language alternative in <switch>")

            # Check that last child is default fallback (no systemLanguage)
            last_child = children[-1]
            self.assertIsNone(last_child.attrib.get("systemLanguage"), "Last child of <switch> must be fallback without systemLanguage")

            # Check that all alternatives are semantic <text> elements
            for child in children:
                tag = child.tag.split("}")[-1]
                self.assertEqual(tag, "text", f"Child of <switch> must be <text>, got <{tag}>")

    def test_inkscape_text_editability(self):
        """All text elements must be 100% editable in Inkscape text tool (not outlined to paths)."""
        typo_layer = None
        for g in self.root.iter():
            if g.attrib.get("id") == "layer-typography":
                typo_layer = g
                break

        # Zero path or polygon elements in typography layer
        banned_tags = {"path", "polygon", "polyline"}
        for elem in typo_layer.iter():
            tag = elem.tag.split("}")[-1]
            self.assertNotIn(tag, banned_tags, f"Typography layer must not contain outlined vector shape <{tag}>")

        # Text nodes must have font-family and valid text content
        text_nodes = typo_layer.findall(".//{http://www.w3.org/2000/svg}text") + typo_layer.findall(".//text")
        self.assertGreater(len(text_nodes), 15)

        for text_elem in text_nodes:
            self.assertIn("font-family", text_elem.attrib, "Text element must specify font-family for Inkscape editing")
            self.assertIn("x", text_elem.attrib, "Text element must specify x coordinate")
            self.assertIn("y", text_elem.attrib, "Text element must specify y coordinate")
            text_val = (text_elem.text or "").strip()
            self.assertTrue(len(text_val) > 0, "Text element must contain non-empty textual content")

    def test_wrapper_pattern_and_css_contract(self):
        """Card motion elements must conform to Wrapper Pattern and Universal CSS Transform Contract."""
        with open(self.asset_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        self.assertIn("transform-box: fill-box;", raw_text)
        self.assertIn("transform-origin: center;", raw_text)

        # Confirm wrapper class groups wrap static geometry groups
        motion_layer = None
        for g in self.root.iter():
            if g.attrib.get("id") == "layer-motion":
                motion_layer = g
                break
        self.assertIsNotNone(motion_layer)

        wrapper_groups = [
            elem for elem in motion_layer.iter()
            if "anim-" in elem.attrib.get("class", "")
        ]
        self.assertGreaterEqual(len(wrapper_groups), 2)
        for w in wrapper_groups:
            tag = w.tag.split("}")[-1]
            self.assertEqual(tag, "g", "Animation wrapper must be a <g> element")


if __name__ == "__main__":
    unittest.main()
