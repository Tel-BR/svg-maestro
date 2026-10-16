#!/usr/bin/env python3
"""
SVG Maestro - Art Direction Refinement Verbs Test Suite
Tests for the 6 expressive creative commands:
- bolder: Amplifies stroke weights, enhances gradient contrasts, increases filter glow intensity.
- quieter: Reduces saturation, softens lighting/glows, reduces stroke weights.
- distill: Strips secondary decorative shapes while preserving core geometric hierarchy and metrics.
- delight: Injects subtle micro-motion accents using the Wrapper Pattern and CSS transform contracts.
- animate: Transforms a static SVG into a motion asset with Wrapper Pattern groups and keyframes.
- critique: Emits structured two-axis review scoring Technical Standards and Aesthetic Craft.

Guaranteed Contract: All refined SVGs must pass validate_svg.py with 0 errors and 0 warnings.
"""

import os
import sys
import json
import shutil
import tempfile
import unittest
import subprocess
import xml.etree.ElementTree as ET

# Setup sys.path
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TESTS_DIR, ".."))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
FIXTURES_DIR = os.path.join(TESTS_DIR, "fixtures")
EXAMPLES_DASHBOARD_DIR = os.path.join(REPO_ROOT, "examples", "dashboard")
EXAMPLES_OBS_DIR = os.path.join(REPO_ROOT, "examples", "obs")

if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from validate_svg import validate_svg_file
from refinement_verbs import (
    bolder,
    quieter,
    distill,
    delight,
    animate,
    critique,
    critique_file,
    apply_verb,
    apply_verb_file,
    format_critique_markdown
)


# Static SVG fixture for testing animate and other verbs
STATIC_SVG_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 800 500"
     width="100%" height="100%">
  <defs>
    <linearGradient id="grad-card-bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0e1726" />
      <stop offset="100%" stop-color="#0a0e17" />
    </linearGradient>
    <linearGradient id="grad-accent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#0077aa" stop-opacity="0.3" />
    </linearGradient>
    <filter id="filter-core-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="blur-core" />
      <feMerge>
        <feMergeNode in="blur-core" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Layer 1: Background -->
  <g inkscape:groupmode="layer" id="layer-background" inkscape:label="Background">
    <rect width="800" height="500" fill="url(#grad-card-bg)" />
  </g>

  <!-- Layer 2: Grid & Secondary Accents -->
  <g inkscape:groupmode="layer" id="layer-grid" inkscape:label="Grid Accents">
    <path id="grid-primary-axis" d="M 50,400 L 750,400" stroke="#1b283d" stroke-width="1.0" />
    <circle id="grid-tic-01" cx="50" cy="400" r="1.5" fill="#00f0ff" class="secondary-tic" />
    <circle id="grid-tic-02" cx="150" cy="400" r="1.5" fill="#00f0ff" class="secondary-tic" />
    <circle id="accent-dot-micro" cx="720" cy="80" r="1.0" fill="#00f0ff" />
    <line id="tic-mark-vert" x1="100" y1="395" x2="100" y2="405" stroke="#00f0ff" stroke-width="0.5" />
  </g>

  <!-- Layer 3: Geometry & Primary Telemetry -->
  <g inkscape:groupmode="layer" id="layer-geometry" inkscape:label="Geometric Structure">
    <g id="geom-gauge-ring">
      <circle id="gauge-ring-outer" cx="400" cy="220" r="90" fill="none" stroke="#00f0ff" stroke-width="2.0" filter="url(#filter-core-glow)" />
      <circle id="gauge-ring-inner" cx="400" cy="220" r="70" fill="none" stroke="#0077aa" stroke-width="1.5" />
    </g>
    <polygon id="geom-center-diamond" points="400,190 430,220 400,250 370,220" fill="#00f0ff" opacity="0.8" />
  </g>

  <!-- Layer 4: Typography -->
  <g inkscape:groupmode="layer" id="layer-typography" inkscape:label="Typography &amp; Labels">
    <text x="50" y="80" fill="#ffffff" font-family="'JetBrains Mono', monospace" font-size="22" font-weight="700">CORE TELEMETRY</text>
    <text x="400" y="228" fill="#ffffff" font-family="'JetBrains Mono', monospace" font-size="28" font-weight="700" text-anchor="middle">98.4%</text>
  </g>
</svg>"""


class TestRefinementVerbs(unittest.TestCase):
    """Test suite for SVG Maestro Art Direction Refinement Verbs."""

    def setUp(self):
        """Create isolated temporary directory for test outputs."""
        self.temp_dir = tempfile.mkdtemp(prefix="svg_maestro_refine_test_")
        self.static_svg_path = os.path.join(self.temp_dir, "static_test.svg")
        with open(self.static_svg_path, "w", encoding="utf-8") as f:
            f.write(STATIC_SVG_TEMPLATE)

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    # -------------------------------------------------------------------------
    # 1. BOLDER VERB
    # -------------------------------------------------------------------------
    def test_bolder_amplifies_strokes_glow_and_contrast(self):
        """'bolder' must amplify stroke-widths, boost feGaussianBlur stdDeviation, and contrast."""
        refined = bolder(STATIC_SVG_TEMPLATE, factor=1.6)

        # Verify stroke width amplification
        self.assertIn('stroke-width="3.2"', refined)  # 2.0 * 1.6 = 3.2
        self.assertIn('stroke-width="2.4"', refined)  # 1.5 * 1.6 = 2.4
        self.assertIn('stroke-width="1.6"', refined)  # 1.0 * 1.6 = 1.6

        # Verify filter glow amplification (2.5 * 1.6 = 4.0)
        self.assertIn('stdDeviation="4.0"', refined)

        # Write to temporary file and validate with linter
        out_path = os.path.join(self.temp_dir, "bolder_out.svg")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(refined)

        res = validate_svg_file(out_path)
        self.assertTrue(res.is_valid, f"Bolder output failed validation: {res.errors}")
        self.assertEqual(len(res.errors), 0)
        self.assertEqual(len(res.warnings), 0)

    # -------------------------------------------------------------------------
    # 2. QUIETER VERB
    # -------------------------------------------------------------------------
    def test_quieter_reduces_strokes_glow_and_saturation(self):
        """'quieter' must reduce stroke-widths, soften glow, and desaturate colors."""
        refined = quieter(STATIC_SVG_TEMPLATE, factor=0.7)

        # Verify stroke width reduction (2.0 * 0.7 = 1.4, 1.5 * 0.7 = 1.05)
        self.assertIn('stroke-width="1.4"', refined)

        # Verify filter glow reduction (2.5 * 0.6 = 1.5)
        self.assertIn('stdDeviation="1.5"', refined)

        # Write to temporary file and validate with linter
        out_path = os.path.join(self.temp_dir, "quieter_out.svg")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(refined)

        res = validate_svg_file(out_path)
        self.assertTrue(res.is_valid, f"Quieter output failed validation: {res.errors}")
        self.assertEqual(len(res.errors), 0)
        self.assertEqual(len(res.warnings), 0)

    # -------------------------------------------------------------------------
    # 3. DISTILL VERB
    # -------------------------------------------------------------------------
    def test_distill_strips_secondary_decorations_preserving_hierarchy(self):
        """'distill' must remove micro tics and decorative noise while preserving core layers and metrics."""
        refined = distill(STATIC_SVG_TEMPLATE)

        # Secondary tics and micro-dots must be stripped
        self.assertNotIn('id="grid-tic-01"', refined)
        self.assertNotIn('id="grid-tic-02"', refined)
        self.assertNotIn('id="accent-dot-micro"', refined)
        self.assertNotIn('id="tic-mark-vert"', refined)

        # Core geometry and typography must be preserved
        self.assertIn('id="geom-gauge-ring"', refined)
        self.assertIn('id="layer-background"', refined)
        self.assertIn('id="layer-geometry"', refined)
        self.assertIn('id="layer-typography"', refined)
        self.assertIn('CORE TELEMETRY', refined)
        self.assertIn('98.4%', refined)

        # Validate with linter
        out_path = os.path.join(self.temp_dir, "distill_out.svg")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(refined)

        res = validate_svg_file(out_path)
        self.assertTrue(res.is_valid, f"Distill output failed validation: {res.errors}")
        self.assertEqual(len(res.errors), 0)
        self.assertEqual(len(res.warnings), 0)

    # -------------------------------------------------------------------------
    # 4. DELIGHT VERB
    # -------------------------------------------------------------------------
    def test_delight_injects_micro_motion_with_wrapper_pattern(self):
        """'delight' must inject micro-motion wrapped in <g> with transform-box and transform-origin."""
        refined = delight(STATIC_SVG_TEMPLATE)

        # Verify presence of delight CSS keyframes and wrapper group
        self.assertIn('delight-', refined)
        self.assertIn('transform-box: fill-box;', refined)
        self.assertIn('transform-origin: center;', refined)

        # Verify that motion wrapper is a <g> tag (Wrapper Pattern)
        root = ET.fromstring(refined)
        delight_wrappers = [elem for elem in root.iter() if 'delight' in elem.attrib.get('class', '')]
        self.assertTrue(len(delight_wrappers) > 0, "No delight wrapper elements found")
        for elem in delight_wrappers:
            tag = elem.tag.split('}')[-1]
            self.assertEqual(tag, 'g', f"Delight wrapper must be a <g> tag, got <{tag}>")

        # Validate with linter
        out_path = os.path.join(self.temp_dir, "delight_out.svg")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(refined)

        res = validate_svg_file(out_path)
        self.assertTrue(res.is_valid, f"Delight output failed validation: {res.errors}")
        self.assertEqual(len(res.errors), 0)
        self.assertEqual(len(res.warnings), 0)

    # -------------------------------------------------------------------------
    # 5. ANIMATE VERB
    # -------------------------------------------------------------------------
    def test_animate_transforms_static_svg_into_motion_asset(self):
        """'animate' must transform static SVG into motion asset adhering strictly to the Wrapper Pattern."""
        # Confirm input is static
        res_initial = validate_svg_file(self.static_svg_path)
        self.assertEqual(res_initial.stats['animated_elements_count'], 0)

        refined = animate(STATIC_SVG_TEMPLATE)

        # Must have CSS keyframe animation and transform contracts
        self.assertIn('@keyframes', refined)
        self.assertIn('transform-box: fill-box;', refined)
        self.assertIn('transform-origin: center;', refined)

        # Must contain anim-wrapper groups
        self.assertIn('anim-wrapper-', refined)

        # Save and validate with linter
        out_path = os.path.join(self.temp_dir, "animate_out.svg")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(refined)

        res = validate_svg_file(out_path)
        self.assertTrue(res.is_valid, f"Animate output failed validation: {res.errors}")
        self.assertEqual(len(res.errors), 0)
        self.assertEqual(len(res.warnings), 0)
        self.assertGreater(res.stats['animated_elements_count'], 0)

    # -------------------------------------------------------------------------
    # 6. CRITIQUE VERB
    # -------------------------------------------------------------------------
    def test_critique_evaluates_technical_and_aesthetic_axes(self):
        """'critique' must emit structured two-axis scoring for Technical Standards and Aesthetic Craft."""
        report = critique(STATIC_SVG_TEMPLATE)

        self.assertIn('technical_standards', report)
        self.assertIn('aesthetic_craft', report)
        self.assertIn('composite_score', report)
        self.assertIn('composite_grade', report)
        self.assertIn('highlights', report)
        self.assertIn('recommendations', report)
        self.assertIn('suggested_verbs', report)

        tech = report['technical_standards']
        self.assertIn('score', tech)
        self.assertIn('grade', tech)
        self.assertIn('breakdown', tech)
        self.assertGreaterEqual(tech['score'], 90, "High-quality fixture should score high technical standards")

        aest = report['aesthetic_craft']
        self.assertIn('score', aest)
        self.assertIn('grade', aest)
        self.assertIn('breakdown', aest)
        self.assertGreaterEqual(aest['score'], 80, "High-quality fixture should score good aesthetic craft")

        # Markdown formatter
        md = format_critique_markdown(report)
        self.assertIn('SVG Maestro Design Critique', md)
        self.assertIn('Technical Standards', md)
        self.assertIn('Aesthetic Craft', md)

    def test_critique_penalizes_flawed_svgs(self):
        """'critique' must accurately penalize SVGs with missing layers or missing transform contracts."""
        missing_layers_path = os.path.join(FIXTURES_DIR, "missing_layers.svg")
        if os.path.exists(missing_layers_path):
            with open(missing_layers_path, "r", encoding="utf-8") as f:
                flawed_svg = f.read()
            report = critique(flawed_svg)
            self.assertLess(report['technical_standards']['score'], 85)
            self.assertIn('F', [report['technical_standards']['grade'], report['composite_grade']] if report['technical_standards']['score'] < 60 else report['technical_standards']['grade'])

    # -------------------------------------------------------------------------
    # 7. REFINEMENT ON CANONICAL EXAMPLES
    # -------------------------------------------------------------------------
    def test_refinements_on_canonical_telemetry_card(self):
        """All verbs must succeed on canonical telemetry_card.svg and remain valid."""
        telemetry_card_path = os.path.join(EXAMPLES_DASHBOARD_DIR, "telemetry_card.svg")
        if not os.path.exists(telemetry_card_path):
            self.skipTest("telemetry_card.svg does not exist yet")

        with open(telemetry_card_path, "r", encoding="utf-8") as f:
            original = f.read()

        for verb_name, verb_fn in [('bolder', bolder), ('quieter', quieter), ('distill', distill), ('delight', delight)]:
            refined = verb_fn(original)
            out_path = os.path.join(self.temp_dir, f"canonical_{verb_name}.svg")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(refined)
            res = validate_svg_file(out_path)
            self.assertTrue(res.is_valid, f"Verb {verb_name} produced invalid SVG on canonical card: {res.errors}")
            self.assertEqual(len(res.errors), 0)
            self.assertEqual(len(res.warnings), 0)

    # -------------------------------------------------------------------------
    # 8. CHAINED REFINEMENTS CONTRACT
    # -------------------------------------------------------------------------
    def test_chained_refinements_remain_valid(self):
        """Chaining multiple verbs (bolder -> delight -> quieter) must preserve zero errors and zero warnings."""
        step1 = bolder(STATIC_SVG_TEMPLATE)
        step2 = delight(step1)
        step3 = quieter(step2)

        out_path = os.path.join(self.temp_dir, "chained_out.svg")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(step3)

        res = validate_svg_file(out_path)
        self.assertTrue(res.is_valid, f"Chained refinements failed validation: {res.errors}")
        self.assertEqual(len(res.errors), 0)
        self.assertEqual(len(res.warnings), 0)

    # -------------------------------------------------------------------------
    # 9. CLI INTERFACE
    # -------------------------------------------------------------------------
    def test_cli_interface_all_verbs(self):
        """Test full CLI interface for all verbs and critique flags."""
        verbs = ['bolder', 'quieter', 'distill', 'delight', 'animate']

        for verb in verbs:
            out_file = os.path.join(self.temp_dir, f"cli_{verb}.svg")
            cmd = [
                sys.executable,
                os.path.join(SCRIPTS_DIR, "refinement_verbs.py"),
                verb,
                "--input", self.static_svg_path,
                "--output", out_file
            ]
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
            self.assertEqual(proc.returncode, 0, f"CLI {verb} failed: {proc.stderr}")
            self.assertTrue(os.path.exists(out_file))

            # Validate generated file
            res = validate_svg_file(out_file)
            self.assertTrue(res.is_valid, f"CLI {verb} generated invalid SVG: {res.errors}")
            self.assertEqual(len(res.errors), 0)
            self.assertEqual(len(res.warnings), 0)

        # Test CLI critique --json
        cmd_critique_json = [
            sys.executable,
            os.path.join(SCRIPTS_DIR, "refinement_verbs.py"),
            "critique",
            "--input", self.static_svg_path,
            "--json"
        ]
        proc = subprocess.run(cmd_critique_json, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 0, f"CLI critique --json failed: {proc.stderr}")
        critique_data = json.loads(proc.stdout)
        self.assertIn("composite_score", critique_data)
        self.assertIn("technical_standards", critique_data)

        # Test CLI critique human-readable report
        cmd_critique_txt = [
            sys.executable,
            os.path.join(SCRIPTS_DIR, "refinement_verbs.py"),
            "critique",
            "--input", self.static_svg_path
        ]
        proc = subprocess.run(cmd_critique_txt, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 0, f"CLI critique failed: {proc.stderr}")
        self.assertIn("SVG Maestro Design Critique", proc.stdout)

    def test_non_destructive_derived_output_default(self):
        """CLI without --output or --in-place must create <stem>_<verb>.svg and leave input unchanged."""
        test_file = os.path.join(self.temp_dir, "original_card.svg")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(STATIC_SVG_TEMPLATE)

        cmd = [
            sys.executable,
            os.path.join(SCRIPTS_DIR, "refinement_verbs.py"),
            "bolder",
            "--input", test_file
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 0, f"Command failed: {proc.stderr}")

        derived_file = os.path.join(self.temp_dir, "original_card_bolder.svg")
        self.assertTrue(os.path.exists(derived_file), "Derived file was not created")

        # Original file must remain unchanged
        with open(test_file, "r", encoding="utf-8") as f:
            original_content = f.read()
        self.assertEqual(original_content, STATIC_SVG_TEMPLATE, "Original file was modified unexpectedly")

    def test_in_place_overwrite_when_explicit(self):
        """CLI with --in-place must explicitly overwrite the input file."""
        test_file = os.path.join(self.temp_dir, "inplace_card.svg")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(STATIC_SVG_TEMPLATE)

        cmd = [
            sys.executable,
            os.path.join(SCRIPTS_DIR, "refinement_verbs.py"),
            "bolder",
            "--input", test_file,
            "--in-place"
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 0, f"Command failed: {proc.stderr}")

        with open(test_file, "r", encoding="utf-8") as f:
            modified_content = f.read()
        self.assertNotEqual(modified_content, STATIC_SVG_TEMPLATE, "File was not modified in-place")

    def test_in_place_and_output_are_mutually_exclusive(self):
        """Passing both --output and --in-place must be rejected by argparse."""
        test_file = os.path.join(self.temp_dir, "conflict_card.svg")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(STATIC_SVG_TEMPLATE)

        cmd = [
            sys.executable,
            os.path.join(SCRIPTS_DIR, "refinement_verbs.py"),
            "bolder",
            "--input", test_file,
            "--output", os.path.join(self.temp_dir, "custom.svg"),
            "--in-place"
        ]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        self.assertNotEqual(proc.returncode, 0, "CLI should reject simultaneous --output and --in-place")
        self.assertIn("not allowed with argument", proc.stderr)

    def test_apply_verb_file_python_api(self):
        """apply_verb_file Python API must return a tuple (content, dest_path)."""
        test_file = os.path.join(self.temp_dir, "py_api_card.svg")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(STATIC_SVG_TEMPLATE)

        content, dest_path = apply_verb_file("bolder", test_file)
        self.assertTrue(os.path.exists(dest_path))
        self.assertIn("py_api_card_bolder.svg", dest_path)
        self.assertIn("<svg", content)


if __name__ == "__main__":
    unittest.main()
