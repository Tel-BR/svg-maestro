#!/usr/bin/env python3
"""
SVG Maestro - OBS Streaming Overlays Test Suite
Validates that generated OBS streaming overlays (16:9 webcam frame and alert banner)
adhere to the Experience mode requirements:
- 16:9 aspect ratio and transparent center for camera feed
- Continuous line tracing motion and cyber neon illumination
- Zero linter errors and zero warnings under strict validation
- Strict Wrapper Pattern compliance (zero WRAPPER_PATTERN_COLLISION warnings)
- Inkscape semantic layers across all themes and custom configurations
"""

import os
import sys
import re
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
EXAMPLES_OBS_DIR = os.path.join(REPO_ROOT, "examples", "obs")

if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from validate_svg import validate_svg_file
from obs_pipeline import (
    generate_webcam_frame,
    generate_alert_banner,
    export_obs_overlays,
    THEMES
)


class TestOBSStreamingOverlays(unittest.TestCase):
    """Test suite for OBS Streaming Overlays in examples/obs/."""

    def setUp(self):
        self.webcam_path = os.path.join(EXAMPLES_OBS_DIR, "webcam_frame_16_9.svg")
        self.alert_path = os.path.join(EXAMPLES_OBS_DIR, "alert_banner.svg")

        # Ensure assets exist before tests run
        if not os.path.exists(self.webcam_path) or not os.path.exists(self.alert_path):
            export_obs_overlays(output_dir=EXAMPLES_OBS_DIR, theme_name="cyan_magenta", validate=False)

    def test_webcam_passes_strict_linter_validation(self):
        """Webcam frame must pass validate_svg_file with 0 errors and 0 warnings."""
        result = validate_svg_file(self.webcam_path)
        self.assertTrue(result.is_valid, f"Webcam frame failed validation: {result.errors}")
        self.assertEqual(len(result.errors), 0, f"Expected 0 errors, got: {result.errors}")
        self.assertEqual(len(result.warnings), 0, f"Expected 0 warnings, got: {result.warnings}")

    def test_alert_banner_passes_strict_linter_validation(self):
        """Alert banner must pass validate_svg_file with 0 errors and 0 warnings."""
        result = validate_svg_file(self.alert_path)
        self.assertTrue(result.is_valid, f"Alert banner failed validation: {result.errors}")
        self.assertEqual(len(result.errors), 0, f"Expected 0 errors, got: {result.errors}")
        self.assertEqual(len(result.warnings), 0, f"Expected 0 warnings, got: {result.warnings}")

    def test_webcam_frame_16_9_aspect_ratio(self):
        """Webcam frame must have exact 16:9 viewBox (1920x1080)."""
        tree = ET.parse(self.webcam_path)
        root = tree.getroot()
        viewbox = root.attrib.get("viewBox", "")
        parts = [float(p) for p in viewbox.split()]
        self.assertEqual(len(parts), 4, f"viewBox should have 4 values: {viewbox}")
        min_x, min_y, width, height = parts
        self.assertEqual(min_x, 0.0)
        self.assertEqual(min_y, 0.0)
        self.assertEqual(width, 1920.0)
        self.assertEqual(height, 1080.0)
        # Check 16:9 aspect ratio mathematically
        self.assertAlmostEqual(width / height, 16.0 / 9.0, places=4)

    def test_webcam_transparent_center_camera_aperture(self):
        """Camera aperture center (e.g. 960, 540) must be transparent with no opaque rect/path."""
        tree = ET.parse(self.webcam_path)
        root = tree.getroot()

        # Check all rect elements: none should cover the center (960, 540)
        for rect in root.iter("{http://www.w3.org/2000/svg}rect"):
            x = float(rect.attrib.get("x", 0))
            y = float(rect.attrib.get("y", 0))
            w = float(rect.attrib.get("width", 0))
            h = float(rect.attrib.get("height", 0))
            # Verify the rect does not encompass the center coordinate
            center_covered = (x <= 960 <= x + w) and (y <= 540 <= y + h)
            self.assertFalse(center_covered, f"Found rect covering camera center: x={x}, y={y}, w={w}, h={h}")

        # Check background layer: all shapes must be exterior framing plates
        ns = {"inkscape": "http://www.inkscape.org/namespaces/inkscape", "svg": "http://www.w3.org/2000/svg"}
        bg_layer = None
        for g in root.findall(".//{http://www.w3.org/2000/svg}g"):
            if g.attrib.get("id") == "layer-background":
                bg_layer = g
                break

        self.assertIsNotNone(bg_layer, "layer-background not found")

        # Ensure no full-canvas background rect exists in background layer
        rects_in_bg = bg_layer.findall(".//{http://www.w3.org/2000/svg}rect")
        self.assertEqual(len(rects_in_bg), 0, "Background framing layer should not contain full rect fills")

    def test_webcam_semantic_layers_hierarchy(self):
        """Webcam frame must declare all 4 required Inkscape semantic layers with labels."""
        tree = ET.parse(self.webcam_path)
        root = tree.getroot()

        expected_layers = {
            "layer-background": "Background Framing",
            "layer-frame": "Frame Chassis",
            "layer-accents": "Accents and Lighting",
            "layer-typography": "Typography and Labels"
        }

        found_layers = {}
        for g in root.findall("{http://www.w3.org/2000/svg}g"):
            gid = g.attrib.get("id")
            groupmode = g.attrib.get("{http://www.inkscape.org/namespaces/inkscape}groupmode") or g.attrib.get("inkscape:groupmode")
            label = g.attrib.get("{http://www.inkscape.org/namespaces/inkscape}label") or g.attrib.get("inkscape:label")
            if groupmode == "layer" and gid in expected_layers:
                found_layers[gid] = label

        for exp_id, exp_label in expected_layers.items():
            self.assertIn(exp_id, found_layers, f"Missing semantic layer: {exp_id}")
            self.assertEqual(found_layers[exp_id], exp_label)

    def test_webcam_wrapper_pattern_and_css_contract(self):
        """Webcam frame must honor the Wrapper Pattern with zero collisions and valid transform contracts."""
        with open(self.webcam_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Contract checks
        self.assertIn("transform-box: fill-box;", content)
        self.assertIn("transform-origin: center;", content)
        self.assertIn("@keyframes pulse-corner-kf", content)
        self.assertIn("@keyframes blink-rec-kf", content)

        # Verify that animated wrappers are strictly <g> nodes
        tree = ET.parse(self.webcam_path)
        root = tree.getroot()
        for elem in root.findall(".//*[@class]"):
            cls_name = elem.attrib.get("class", "")
            if "anim-" in cls_name:
                tag = elem.tag.split("}")[-1]
                self.assertEqual(tag, "g", f"Animated element with class '{cls_name}' must be <g>, got <{tag}>")

    def test_alert_banner_line_tracing_keyframes(self):
        """Alert banner must feature continuous line tracing motion with stroke-dasharray and stroke-dashoffset."""
        with open(self.alert_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("stroke-dasharray", content)
        self.assertIn("stroke-dashoffset", content)
        self.assertIn("@keyframes trace-perimeter-kf", content)
        self.assertIn("animation: trace-perimeter-kf", content)
        self.assertIn("infinite", content)

        # Verify animated tracing elements exist in DOM
        tree = ET.parse(self.alert_path)
        root = tree.getroot()
        tracing_paths = root.findall(".//{http://www.w3.org/2000/svg}path[@class='anim-line-trace']")
        self.assertGreaterEqual(len(tracing_paths), 1, "Expected at least 1 anim-line-trace path in alert banner")

    def test_alert_banner_semantic_layers_and_transparent_canvas(self):
        """Alert banner must have semantic layers and transparent surrounding canvas."""
        tree = ET.parse(self.alert_path)
        root = tree.getroot()

        # ViewBox check (1200x300 modular viewport)
        viewbox = root.attrib.get("viewBox", "")
        self.assertEqual(viewbox, "0 0 1200 300")

        # Layer check
        expected_layers = ["layer-background", "layer-frame", "layer-accents", "layer-typography"]
        found_layer_ids = []
        for g in root.findall("{http://www.w3.org/2000/svg}g"):
            groupmode = g.attrib.get("{http://www.inkscape.org/namespaces/inkscape}groupmode") or g.attrib.get("inkscape:groupmode")
            if groupmode == "layer":
                found_layer_ids.append(g.attrib.get("id"))

        for exp_id in expected_layers:
            self.assertIn(exp_id, found_layer_ids, f"Alert banner missing layer: {exp_id}")

        # Transparent Canvas: Canvas corners (0,0) and (1200,300) must not have full opaque rect
        rects = root.findall(".//{http://www.w3.org/2000/svg}rect")
        for r in rects:
            w = float(r.attrib.get("width", 0))
            h = float(r.attrib.get("height", 0))
            self.assertFalse(w >= 1200 and h >= 300, "Alert banner must not have a full-canvas opaque rect")


class TestOBSPipelineProgrammaticAPI(unittest.TestCase):
    """Test suite for scripts/obs_pipeline.py Python functions."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_all_themes_generate_strictly_valid_webcam_svg(self):
        """Every defined theme must produce 100% valid webcam SVG with zero errors and zero warnings."""
        for theme_name in THEMES.keys():
            svg_code = generate_webcam_frame(theme_name=theme_name)
            filepath = os.path.join(self.temp_dir, f"webcam_{theme_name}.svg")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(svg_code)

            result = validate_svg_file(filepath)
            self.assertTrue(result.is_valid, f"Theme '{theme_name}' generated invalid webcam: {result.errors}")
            self.assertEqual(len(result.errors), 0)
            self.assertEqual(len(result.warnings), 0, f"Theme '{theme_name}' generated warnings: {result.warnings}")

    def test_all_themes_generate_strictly_valid_alert_svg(self):
        """Every defined theme must produce 100% valid alert SVG with zero errors and zero warnings."""
        for theme_name in THEMES.keys():
            svg_code = generate_alert_banner(theme_name=theme_name)
            filepath = os.path.join(self.temp_dir, f"alert_{theme_name}.svg")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(svg_code)

            result = validate_svg_file(filepath)
            self.assertTrue(result.is_valid, f"Theme '{theme_name}' generated invalid alert: {result.errors}")
            self.assertEqual(len(result.errors), 0)
            self.assertEqual(len(result.warnings), 0, f"Theme '{theme_name}' generated warnings: {result.warnings}")

    def test_custom_text_generation(self):
        """Overlays should embed custom labels accurately in decoupled text tags."""
        cam_svg = generate_webcam_frame(
            cam_label="CUSTOM_CAM_A",
            status_label="RECORDING_LIVE",
            audio_label="CH1_STEREO",
            telemetry_label="LATENCY_5MS"
        )
        self.assertIn("CUSTOM_CAM_A", cam_svg)
        self.assertIn("RECORDING_LIVE", cam_svg)
        self.assertIn("CH1_STEREO", cam_svg)
        self.assertIn("LATENCY_5MS", cam_svg)

        alert_svg = generate_alert_banner(
            alert_type="NEW RAID",
            username="STREAM_CAPTAIN",
            detail_text="500 VIEWERS INCOMING"
        )
        self.assertIn("NEW RAID", alert_svg)
        self.assertIn("STREAM_CAPTAIN", alert_svg)
        self.assertIn("500 VIEWERS INCOMING", alert_svg)

    def test_export_obs_overlays_function(self):
        """export_obs_overlays must write both files and validate them successfully."""
        res = export_obs_overlays(output_dir=self.temp_dir, theme_name="matrix_green", validate=True)
        self.assertEqual(res["theme"], "matrix_green")
        self.assertTrue(res["files"]["webcam"]["valid"])
        self.assertTrue(res["files"]["alert"]["valid"])
        self.assertEqual(len(res["files"]["webcam"]["errors"]), 0)
        self.assertEqual(len(res["files"]["alert"]["errors"]), 0)
        self.assertEqual(len(res["files"]["webcam"]["warnings"]), 0)
        self.assertEqual(len(res["files"]["alert"]["warnings"]), 0)


class TestOBSPipelineCLI(unittest.TestCase):
    """Test suite for CLI execution of scripts/obs_pipeline.py."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.cli_path = os.path.join(SCRIPTS_DIR, "obs_pipeline.py")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_cli_generate_all_exits_zero(self):
        """CLI generate-all command must exit with code 0."""
        cmd = [sys.executable, self.cli_path, "generate-all", "--output-dir", self.temp_dir, "--theme", "crimson_hazard"]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(proc.returncode, 0, f"STDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
        self.assertIn("[PASS] VALID", proc.stdout)

        webcam_file = os.path.join(self.temp_dir, "webcam_frame_16_9.svg")
        alert_file = os.path.join(self.temp_dir, "alert_banner.svg")
        self.assertTrue(os.path.exists(webcam_file))
        self.assertTrue(os.path.exists(alert_file))

    def test_cli_webcam_command(self):
        """CLI webcam command generates custom webcam frame."""
        out_file = os.path.join(self.temp_dir, "my_webcam.svg")
        cmd = [sys.executable, self.cli_path, "webcam", "--output", out_file, "--cam-label", "DEV_STREAM"]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertTrue(os.path.exists(out_file))
        res = validate_svg_file(out_file)
        self.assertTrue(res.is_valid)

    def test_cli_alert_command(self):
        """CLI alert command generates custom alert banner."""
        out_file = os.path.join(self.temp_dir, "my_alert.svg")
        cmd = [sys.executable, self.cli_path, "alert", "--output", out_file, "--user", "PILOT_ZERO"]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertTrue(os.path.exists(out_file))
        res = validate_svg_file(out_file)
        self.assertTrue(res.is_valid)


if __name__ == "__main__":
    unittest.main()
