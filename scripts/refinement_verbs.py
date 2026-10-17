#!/usr/bin/env python3
"""
SVG Maestro - Art Direction Refinement Verbs Engine
Provides expressive creative direction commands for iterative vector refinement:
- bolder: Amplifies stroke weights, enhances gradient contrasts, increases filter glow intensity.
- quieter: Reduces saturation, softens lighting/glows, reduces stroke weights.
- distill: Strips secondary decorative shapes while preserving core geometric hierarchy and metrics.
- delight: Injects subtle micro-motion accents using the Wrapper Pattern and CSS transform contracts.
- animate: Transforms a static SVG into a motion asset with Wrapper Pattern groups and keyframes.
- critique: Emits structured two-axis review scoring Technical Standards and Aesthetic Craft.

Guaranteed Contract: All refined SVG outputs MUST pass validate_svg.py with 0 errors and 0 warnings.
Zero external dependencies (Python standard library only).
"""

import os
import sys
import re
import json
import math
import colorsys
import argparse
import tempfile
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional, Tuple

# Ensure scripts directory is in sys.path
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from validate_svg import validate_svg_file, NAMESPACES

# Standard XML Namespaces for SVG Maestro
INKSCAPE_NS = "http://www.inkscape.org/namespaces/inkscape"
SODIPODI_NS = "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
XLINK_NS = "http://www.w3.org/1999/xlink"
SVG_NS = "http://www.w3.org/2000/svg"

REGISTERED_NAMESPACES = {
    "": SVG_NS,
    "inkscape": INKSCAPE_NS,
    "sodipodi": SODIPODI_NS,
    "xlink": XLINK_NS
}


# =============================================================================
# XML & SERIALIZATION HELPERS
# =============================================================================

def get_clean_tag(elem: ET.Element) -> str:
    """Return local tag name without namespace, safely handling comment nodes."""
    if not isinstance(elem.tag, str):
        return ""
    return elem.tag.split("}")[-1]


def ensure_namespaces_and_viewbox(root: ET.Element):
    """Ensure root <svg> has viewBox attribute, normalizing commas or deducing from width/height."""
    viewbox = root.attrib.get("viewBox")
    if not viewbox:
        w_str = root.attrib.get("width", "800")
        h_str = root.attrib.get("height", "600")
        w_match = re.search(r"([0-9.]+)", w_str)
        h_match = re.search(r"([0-9.]+)", h_str)
        w = float(w_match.group(1)) if w_match else 800.0
        h = float(h_match.group(1)) if h_match else 600.0
        if w <= 0 or "%" in w_str:
            w = 800.0
        if h <= 0 or "%" in h_str:
            h = 600.0
        root.attrib["viewBox"] = f"0 0 {int(w)} {int(h)}"
    else:
        parts = [p for p in re.split(r"[\s,]+", viewbox.strip()) if p]
        if len(parts) == 4:
            root.attrib["viewBox"] = " ".join(parts)


def ensure_defs_hygiene(root: ET.Element):
    """Sanitize generic or missing IDs in definition elements (<linearGradient>, <filter>, etc.)."""
    id_map = {}
    gen_counter = 1
    for elem in root.iter():
        tag = get_clean_tag(elem)
        if tag in ("linearGradient", "radialGradient", "filter", "pattern", "clipPath"):
            elem_id = elem.attrib.get("id", "")
            if not elem_id:
                new_id = f"def-{tag}-{gen_counter}"
                gen_counter += 1
                elem.attrib["id"] = new_id
            elif re.match(r"^(linearGradient|radialGradient|filter)\d+$", elem_id):
                prefix = "grad" if "Gradient" in tag else tag
                new_id = f"{prefix}-legacy-{elem_id}"
                id_map[elem_id] = new_id
                elem.attrib["id"] = new_id

    if id_map:
        for elem in root.iter():
            tag = get_clean_tag(elem)
            if tag == "style" and elem.text:
                for old_id, new_id in id_map.items():
                    elem.text = elem.text.replace(f"#{old_id}", f"#{new_id}")
            for attr_name, attr_val in list(elem.attrib.items()):
                for old_id, new_id in id_map.items():
                    if f"#{old_id}" in attr_val:
                        elem.attrib[attr_name] = attr_val.replace(f"#{old_id}", f"#{new_id}")
                    if f"url(#{old_id})" in attr_val:
                        elem.attrib[attr_name] = attr_val.replace(f"url(#{old_id})", f"url(#{new_id})")


def ensure_semantic_layers(root: ET.Element):
    """Ensure all visual content is grouped into labeled semantic Inkscape layers."""
    inkscape_groupmode_key = f"{{{INKSCAPE_NS}}}groupmode"
    inkscape_label_key = f"{{{INKSCAPE_NS}}}label"

    # Find existing layer groups
    existing_layers = []
    for child in list(root):
        if get_clean_tag(child) == "g":
            groupmode = child.attrib.get(inkscape_groupmode_key) or child.attrib.get("inkscape:groupmode")
            if groupmode == "layer":
                existing_layers.append(child)

    if existing_layers:
        # Layers exist: ensure every layer has an inkscape:label
        for g in existing_layers:
            label = g.attrib.get(inkscape_label_key) or g.attrib.get("inkscape:label")
            if not label:
                gid = g.attrib.get("id", "Layer")
                label = gid.replace("-", " ").replace("_", " ").title()
            g.attrib[inkscape_label_key] = label
            g.attrib.pop("inkscape:label", None)
            g.attrib[inkscape_groupmode_key] = "layer"
            g.attrib.pop("inkscape:groupmode", None)

        # Check if there are loose visual elements outside of any layers at the root level
        HEADER_TAGS = {"defs", "style", "metadata", "title", "desc", "sodipodi:namedview", "namedview"}
        loose_elements = []
        for child in list(root):
            ctag = get_clean_tag(child)
            if ctag in HEADER_TAGS:
                continue
            groupmode = child.attrib.get(inkscape_groupmode_key) or child.attrib.get("inkscape:groupmode")
            if groupmode != "layer":
                loose_elements.append(child)

        if loose_elements:
            target_layer = None
            for layer in existing_layers:
                lid = (layer.attrib.get("id") or "").lower()
                llabel = (layer.attrib.get(inkscape_label_key) or layer.attrib.get("inkscape:label") or "").lower()
                if "geom" in lid or "geom" in llabel or "structure" in llabel or "content" in lid:
                    target_layer = layer
                    break
            if target_layer is None and existing_layers:
                target_layer = existing_layers[-1]

            for elem in loose_elements:
                root.remove(elem)
                if target_layer is not None:
                    target_layer.append(elem)
        return

    # No semantic layers found! Inspect top-level elements
    HEADER_TAGS = {"defs", "style", "metadata", "title", "desc", "sodipodi:namedview", "namedview"}
    top_groups = []
    loose_elements = []

    for child in list(root):
        ctag = get_clean_tag(child)
        if ctag in HEADER_TAGS:
            continue
        if ctag == "g":
            top_groups.append(child)
        else:
            loose_elements.append(child)

    if top_groups and not loose_elements:
        # All top-level visual elements are already <g> groups: upgrade them into layers!
        for g in top_groups:
            g.attrib[inkscape_groupmode_key] = "layer"
            g.attrib.pop("inkscape:groupmode", None)
            label = g.attrib.get(inkscape_label_key) or g.attrib.get("inkscape:label")
            if not label:
                gid = g.attrib.get("id", "Layer")
                label = gid.replace("-", " ").replace("_", " ").title()
            g.attrib[inkscape_label_key] = label
            g.attrib.pop("inkscape:label", None)
        return

    # Otherwise, we have loose shapes/elements (or mixed groups and shapes)
    all_visual = []
    for child in list(root):
        ctag = get_clean_tag(child)
        if ctag not in HEADER_TAGS:
            root.remove(child)
            all_visual.append(child)

    if not all_visual:
        dummy = ET.SubElement(root, f"{{{SVG_NS}}}g")
        dummy.attrib["id"] = "layer-geometry"
        dummy.attrib[inkscape_groupmode_key] = "layer"
        dummy.attrib[inkscape_label_key] = "Geometric Structure"
        return

    bg_elements = []
    typo_elements = []
    geom_elements = []

    for elem in all_visual:
        ctag = get_clean_tag(elem)
        eid = (elem.attrib.get("id") or "").lower()
        eclass = (elem.attrib.get("class") or "").lower()

        if ctag in ("text", "switch"):
            typo_elements.append(elem)
        elif "bg" in eid or "background" in eid or "chassis" in eid or "bg" in eclass:
            bg_elements.append(elem)
        elif not bg_elements and ctag == "rect" and (
            elem.attrib.get("width") in ("100%", "800", "1920", "1200", "600", "500") or
            elem.attrib.get("height") in ("100%", "600", "1080", "500", "480", "400")
        ):
            bg_elements.append(elem)
        else:
            geom_elements.append(elem)

    if not geom_elements and not typo_elements and bg_elements:
        geom_elements = bg_elements
        bg_elements = []

    if bg_elements:
        bg_layer = ET.SubElement(root, f"{{{SVG_NS}}}g")
        bg_layer.attrib["id"] = "layer-background"
        bg_layer.attrib[inkscape_groupmode_key] = "layer"
        bg_layer.attrib[inkscape_label_key] = "Background"
        for elem in bg_elements:
            bg_layer.append(elem)

    if geom_elements or (not bg_elements and not typo_elements):
        geom_layer = ET.SubElement(root, f"{{{SVG_NS}}}g")
        geom_layer.attrib["id"] = "layer-geometry"
        geom_layer.attrib[inkscape_groupmode_key] = "layer"
        geom_layer.attrib[inkscape_label_key] = "Geometric Structure"
        for elem in geom_elements:
            geom_layer.append(elem)

    if typo_elements:
        typo_layer = ET.SubElement(root, f"{{{SVG_NS}}}g")
        typo_layer.attrib["id"] = "layer-typography"
        typo_layer.attrib[inkscape_groupmode_key] = "layer"
        typo_layer.attrib[inkscape_label_key] = "Typography & Labels"
        for elem in typo_elements:
            typo_layer.append(elem)


def ensure_animation_wrapper_pattern(root: ET.Element):
    """Ensure transform animations adhere to the Wrapper Pattern and have transform-box contracts."""
    style_nodes = []
    for elem in root.iter():
        if get_clean_tag(elem) == "style":
            style_nodes.append(elem)

    full_css = "".join(s.text or "" for s in style_nodes)
    has_animation = "@keyframes" in full_css or "animation" in full_css

    for elem in root.iter():
        elem_style = elem.attrib.get("style", "")
        if "animation" in elem_style or "@keyframes" in elem_style:
            has_animation = True
            break

    if not has_animation:
        return

    # Extract keyframes that animate transforms
    transform_keyframes = set()
    for kf_match in re.finditer(r'@(?:-webkit-)?keyframes\s+([a-zA-Z0-9_-]+)\s*\{([\s\S]*?)\}(?=\s*(@(?:-webkit-)?keyframes|\s*$|[^{]*\{))', full_css):
        kf_name = kf_match.group(1)
        kf_body = kf_match.group(2)
        if any(term in kf_body for term in ("transform", "rotate", "scale", "translate", "matrix")):
            transform_keyframes.add(kf_name)

    # Find classes that animate transforms
    anim_classes = {}
    for cls_name, cls_body in re.findall(r'\.([a-zA-Z0-9_-]+)\s*\{([^}]*)\}', full_css):
        anim_match = re.search(r'animation\s*:\s*([a-zA-Z0-9_-]+)', cls_body)
        if anim_match:
            anim_name = anim_match.group(1)
            if anim_name in transform_keyframes or any(term in cls_body for term in ("transform", "rotate", "scale")):
                anim_classes[cls_name] = anim_name

    # Check for direct shape collisions: elements not <g> that have an animated transform class
    parent_map = {c: p for p in root.iter() for c in p}
    wrapper_counter = 1

    for elem in list(root.iter()):
        tag = get_clean_tag(elem)
        if tag in ("g", "svg", "style", "defs"):
            continue

        cls_attr = elem.attrib.get("class", "")
        elem_style = elem.attrib.get("style", "")
        elem_classes = cls_attr.split()
        colliding_classes = [c for c in elem_classes if c in anim_classes]

        has_inline_anim = "animation" in elem_style and any(term in elem_style for term in ("rotate", "scale", "transform"))

        if colliding_classes or has_inline_anim:
            parent = parent_map.get(elem)
            if parent is None:
                continue

            wrapper = ET.Element(f"{{{SVG_NS}}}g")
            wrapper_cls = []
            for c in colliding_classes:
                wrapper_cls.append(f"anim-wrapper-{c}")
                wrapper_cls.append(c)
            if has_inline_anim:
                wrapper_cls.append("anim-wrapper-inline")

            wrapper.attrib["class"] = " ".join(wrapper_cls) if wrapper_cls else "anim-wrapper-legacy"
            elem_id = elem.attrib.get("id", f"target-{wrapper_counter}")
            wrapper.attrib["id"] = f"wrapper-anim-{elem_id}"
            wrapper_counter += 1

            remaining_classes = [c for c in elem_classes if c not in colliding_classes]
            if remaining_classes:
                elem.attrib["class"] = " ".join(remaining_classes)
            elif "class" in elem.attrib:
                del elem.attrib["class"]

            if has_inline_anim:
                wrapper.attrib["style"] = elem_style
                del elem.attrib["style"]

            idx = list(parent).index(elem)
            parent.remove(elem)
            wrapper.append(elem)
            parent.insert(idx, wrapper)
            parent_map[elem] = wrapper
            parent_map[wrapper] = parent

    # Ensure CSS contains transform-box: fill-box; and transform-origin: center;
    needs_tbox = "transform-box" not in full_css or "fill-box" not in full_css
    needs_torig = "transform-origin" not in full_css

    if needs_tbox or needs_torig:
        contract_css = """
/* SVG Maestro Universal Transform Contracts */
[class*="anim-"], [class*="wrapper-anim"], [class*="radar"], [class*="needle"], [class*="spinner"] {
  transform-box: fill-box;
  transform-origin: center;
}
"""
        if style_nodes:
            style_nodes[0].text = (style_nodes[0].text or "") + "\n" + contract_css
        else:
            new_style = ET.Element(f"{{{SVG_NS}}}style")
            new_style.text = contract_css
            root.insert(0, new_style)


def upgrade_legacy_svg_element(root: ET.Element) -> ET.Element:
    """
    In-memory normalization and auto-upgrade of legacy SVGs:
    - Normalizes namespaces and viewBox
    - Upgrades defs hygiene and fixes generic IDs
    - Groups unorganized visual elements into labeled semantic Inkscape layers
    - Enforces the Animation Wrapper Pattern and universal CSS transform contracts
    """
    ensure_namespaces_and_viewbox(root)
    ensure_defs_hygiene(root)
    ensure_semantic_layers(root)
    ensure_animation_wrapper_pattern(root)
    return root


def upgrade_legacy_svg(svg_content: str, **kwargs) -> str:
    """
    Programmatic entrypoint to auto-upgrade a legacy SVG string in-memory
    to modern SVG Maestro standards without modifying creative visual intent.
    Guaranteed to produce an SVG passing validate_svg.py with 0 errors and 0 warnings.
    """
    root = parse_svg(svg_content, upgrade_legacy=True)
    return serialize_svg(root)


def normalize_svg_string(svg_content: str) -> str:
    """Ensure standard namespace declarations exist in raw string before XML parsing."""
    raw = svg_content
    if "xmlns:inkscape=" not in raw:
        raw = re.sub(r'<svg\b', f'<svg xmlns:inkscape="{INKSCAPE_NS}"', raw, count=1)
    if "xmlns:sodipodi=" not in raw and "sodipodi:" in raw:
        raw = re.sub(r'<svg\b', f'<svg xmlns:sodipodi="{SODIPODI_NS}"', raw, count=1)
    if "xmlns:xlink=" not in raw and "xlink:" in raw:
        raw = re.sub(r'<svg\b', f'<svg xmlns:xlink="{XLINK_NS}"', raw, count=1)
    return raw


def parse_svg(svg_content: str, upgrade_legacy: bool = True) -> ET.Element:
    """Parse SVG string into an ElementTree root element preserving comments.
    If upgrade_legacy is True, automatically normalizes and upgrades legacy SVGs in-memory.
    """
    for prefix, uri in REGISTERED_NAMESPACES.items():
        ET.register_namespace(prefix, uri)

    clean_content = normalize_svg_string(svg_content)
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    root = ET.fromstring(clean_content, parser=parser)
    if upgrade_legacy:
        upgrade_legacy_svg_element(root)
    return root


def serialize_svg(root: ET.Element) -> str:
    """Serialize ElementTree root element into clean, formatted SVG markup."""
    for prefix, uri in REGISTERED_NAMESPACES.items():
        ET.register_namespace(prefix, uri)

    if hasattr(ET, "indent"):
        ET.indent(root, space="  ")
    raw = ET.tostring(root, encoding="utf-8").decode("utf-8")

    # Ensure root <svg> has exact required namespace declarations for Inkscape and validator
    if 'xmlns:inkscape=' not in raw:
        raw = re.sub(r'<svg\b', f'<svg xmlns:inkscape="{INKSCAPE_NS}"', raw, count=1)
    if 'xmlns:sodipodi=' not in raw:
        raw = re.sub(r'<svg\b', f'<svg xmlns:sodipodi="{SODIPODI_NS}"', raw, count=1)
    if 'xmlns:xlink=' not in raw:
        raw = re.sub(r'<svg\b', f'<svg xmlns:xlink="{XLINK_NS}"', raw, count=1)

    return raw


def validate_content(svg_content: str) -> Tuple[bool, List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Validate in-memory SVG content using validate_svg_file via a temporary file."""
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False, encoding="utf-8") as f:
        f.write(svg_content)
        temp_path = f.name
    try:
        res = validate_svg_file(temp_path)
        return res.is_valid and len(res.warnings) == 0, res.errors, res.warnings
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


# =============================================================================
# COLOR & FORMATTING UTILITIES
# =============================================================================

def hex_to_rgb(hex_str: str) -> Optional[Tuple[float, float, float]]:
    """Convert hex string (#rgb or #rrggbb) to normalized RGB floats in [0, 1]."""
    clean_hex = hex_str.strip().lstrip("#")
    if len(clean_hex) == 3:
        clean_hex = "".join(c * 2 for c in clean_hex)
    if len(clean_hex) != 6:
        return None
    try:
        r = int(clean_hex[0:2], 16) / 255.0
        g = int(clean_hex[2:4], 16) / 255.0
        b = int(clean_hex[4:6], 16) / 255.0
        return (r, g, b)
    except ValueError:
        return None


def rgb_to_hex(r: float, g: float, b: float) -> str:
    """Convert normalized RGB floats to #rrggbb hex string."""
    r_int = max(0, min(255, int(round(r * 255.0))))
    g_int = max(0, min(255, int(round(g * 255.0))))
    b_int = max(0, min(255, int(round(b * 255.0))))
    return f"#{r_int:02x}{g_int:02x}{b_int:02x}"


def format_number(val: float) -> str:
    """Neatly format a numeric value for SVG attributes."""
    val_rounded = round(val, 2)
    if abs(val_rounded - round(val_rounded, 1)) < 1e-5:
        return f"{val_rounded:.1f}"
    return f"{val_rounded:.2f}"


def scale_stroke_string(val_str: str, factor: float, min_val: float = 0.2) -> str:
    """Scale a stroke-width string (e.g. '2.0', '1.5px') by factor."""
    m = re.match(r"^([0-9.]+)(.*)$", val_str.strip())
    if not m:
        return val_str
    num_str, unit = m.group(1), m.group(2)
    try:
        num = float(num_str)
        new_num = max(min_val, num * factor)
        return f"{format_number(new_num)}{unit}"
    except ValueError:
        return val_str


# =============================================================================
# VERB 1: BOLDER
# =============================================================================

def bolder(svg_content: str, factor: float = 1.6) -> str:
    """
    Amplifies stroke weights (1.4x-1.8x, default 1.6x), enhances gradient contrasts,
    and increases filter glow intensity (feGaussianBlur stdDeviation).
    """
    root = parse_svg(svg_content)

    # 1. Amplify stroke weights in element attributes and styles
    for elem in root.iter():
        if "stroke-width" in elem.attrib:
            elem.attrib["stroke-width"] = scale_stroke_string(elem.attrib["stroke-width"], factor)

        if "style" in elem.attrib:
            def repl_stroke(m):
                scaled = scale_stroke_string(m.group(1), factor)
                return f"stroke-width: {scaled}{m.group(2)}"
            elem.attrib["style"] = re.sub(r"stroke-width\s*:\s*([0-9.]+)(px)?", repl_stroke, elem.attrib["style"])

    # 2. Amplify stroke-widths inside <style> blocks
    for style_elem in root.iter():
        tag = get_clean_tag(style_elem)
        if tag == "style" and style_elem.text:
            def repl_style_stroke(m):
                scaled = scale_stroke_string(m.group(1), factor)
                return f"stroke-width: {scaled}{m.group(2)}"
            style_elem.text = re.sub(r"stroke-width\s*:\s*([0-9.]+)(px)?", repl_style_stroke, style_elem.text)

    # 3. Increase filter glow intensity (feGaussianBlur stdDeviation)
    for elem in root.iter():
        tag = get_clean_tag(elem)
        if tag == "feGaussianBlur" and "stdDeviation" in elem.attrib:
            parts = elem.attrib["stdDeviation"].strip().split()
            new_parts = []
            for p in parts:
                try:
                    val = float(p) * factor
                    new_parts.append(format_number(val))
                except ValueError:
                    new_parts.append(p)
            elem.attrib["stdDeviation"] = " ".join(new_parts)

    # 4. Enhance gradient contrasts and opacities
    for elem in root.iter():
        tag = get_clean_tag(elem)
        if tag == "stop":
            # Boost stop-opacity slightly if below 1.0
            if "stop-opacity" in elem.attrib:
                try:
                    op = float(elem.attrib["stop-opacity"])
                    elem.attrib["stop-opacity"] = format_number(min(1.0, op * 1.25))
                except ValueError:
                    pass

            # Boost saturation of vibrant stop colors and deepen dark background stops
            if "stop-color" in elem.attrib:
                rgb = hex_to_rgb(elem.attrib["stop-color"])
                if rgb:
                    h, l, s = colorsys.rgb_to_hls(*rgb)
                    if s > 0.2:  # Accent color
                        s_new = min(1.0, s * 1.2)
                        l_new = min(1.0, l * 1.05) if l > 0.4 else l
                        elem.attrib["stop-color"] = rgb_to_hex(*colorsys.hls_to_rgb(h, l_new, s_new))
                    elif l < 0.25:  # Dark chassis stop
                        l_new = max(0.02, l * 0.85)
                        elem.attrib["stop-color"] = rgb_to_hex(*colorsys.hls_to_rgb(h, l_new, s))

    output = serialize_svg(root)
    return output


# =============================================================================
# VERB 2: QUIETER
# =============================================================================

def quieter(svg_content: str, factor: float = 0.7) -> str:
    """
    Reduces saturation, softens lighting/glows, and reduces stroke weights (0.6x-0.75x, default 0.7x)
    for an understated, elegant look.
    """
    root = parse_svg(svg_content)

    # 1. Reduce stroke weights
    for elem in root.iter():
        if "stroke-width" in elem.attrib:
            elem.attrib["stroke-width"] = scale_stroke_string(elem.attrib["stroke-width"], factor, min_val=0.4)

        if "style" in elem.attrib:
            def repl_stroke(m):
                scaled = scale_stroke_string(m.group(1), factor, min_val=0.4)
                return f"stroke-width: {scaled}{m.group(2)}"
            elem.attrib["style"] = re.sub(r"stroke-width\s*:\s*([0-9.]+)(px)?", repl_stroke, elem.attrib["style"])

    # 2. Soften filter glow (feGaussianBlur stdDeviation)
    blur_factor = 0.6
    for elem in root.iter():
        tag = get_clean_tag(elem)
        if tag == "feGaussianBlur" and "stdDeviation" in elem.attrib:
            parts = elem.attrib["stdDeviation"].strip().split()
            new_parts = []
            for p in parts:
                try:
                    val = max(0.5, float(p) * blur_factor)
                    new_parts.append(format_number(val))
                except ValueError:
                    new_parts.append(p)
            elem.attrib["stdDeviation"] = " ".join(new_parts)

    # 3. Desaturate colors across fills, strokes, and stops
    def desaturate_hex(hex_val: str) -> str:
        rgb = hex_to_rgb(hex_val)
        if not rgb:
            return hex_val
        h, l, s = colorsys.rgb_to_hls(*rgb)
        s_new = max(0.0, s * 0.65)
        # Tone down overly glaring whites/bright neons slightly
        l_new = l * 0.95 if l > 0.85 else l
        return rgb_to_hex(*colorsys.hls_to_rgb(h, l_new, s_new))

    for elem in root.iter():
        for attr in ("stroke", "fill", "stop-color"):
            if attr in elem.attrib and elem.attrib[attr].startswith("#"):
                elem.attrib[attr] = desaturate_hex(elem.attrib[attr])

        # Soften stop opacities
        if "stop-opacity" in elem.attrib:
            try:
                op = float(elem.attrib["stop-opacity"])
                elem.attrib["stop-opacity"] = format_number(max(0.05, op * 0.8))
            except ValueError:
                pass

    output = serialize_svg(root)
    return output


# =============================================================================
# VERB 3: DISTILL
# =============================================================================

def distill(svg_content: str) -> str:
    """
    Strips secondary decorative shapes (micro grid tics, secondary accent embellishments,
    decorative noise) while preserving core geometric hierarchy, metrics, and labels.
    """
    root = parse_svg(svg_content)
    parent_map = {c: p for p in root.iter() for c in p}

    # Keywords identifying secondary decorative elements
    DECORATIVE_PATTERNS = [
        r"\btic\b", r"\btick\b", r"grid-tic", r"grid-sub", r"sub-grid",
        r"noise", r"dust", r"embellish", r"ornament", r"decorative",
        r"accent-dot", r"bracket-sub", r"hairline-sub", r"micro-accent",
        r"secondary-tic", r"tic-mark", r"sub-line"
    ]
    regex_deco = re.compile("|".join(DECORATIVE_PATTERNS), re.IGNORECASE)

    # Collect elements to remove
    to_remove = set()

    for elem in root.iter():
        tag = get_clean_tag(elem)

        # NEVER remove root or semantic layers
        if tag == "svg":
            continue
        groupmode = elem.attrib.get(f"{{{INKSCAPE_NS}}}groupmode") or elem.attrib.get("inkscape:groupmode")
        if groupmode == "layer":
            continue

        # NEVER remove typography elements or text
        if tag in ("text", "tspan", "switch"):
            continue

        # Check if element is inside layer-typography
        p = elem
        in_typography = False
        while p in parent_map:
            p = parent_map[p]
            p_id = p.attrib.get("id", "")
            p_label = p.attrib.get(f"{{{INKSCAPE_NS}}}label") or p.attrib.get("inkscape:label") or ""
            if "typography" in p_id.lower() or "typography" in p_label.lower():
                in_typography = True
                break
        if in_typography:
            continue

        # NEVER remove background or chassis rects
        elem_id = elem.attrib.get("id", "")
        elem_label = elem.attrib.get(f"{{{INKSCAPE_NS}}}label") or elem.attrib.get("inkscape:label") or ""
        elem_class = elem.attrib.get("class", "")

        if "background" in elem_id.lower() or "chassis" in elem_id.lower() or "background" in elem_label.lower():
            continue

        # Criteria 1: Matches decorative keywords in id, class, or label
        identifier = f"{elem_id} {elem_class} {elem_label}"
        if regex_deco.search(identifier):
            to_remove.add(elem)
            continue

        # Criteria 2: Micro-dots (circle with r <= 1.5 in grid/accent layers)
        if tag == "circle":
            try:
                r = float(elem.attrib.get("r", "99"))
                if r <= 1.5:
                    to_remove.add(elem)
                    continue
            except ValueError:
                pass

        # Criteria 3: Hairline lines with stroke-width <= 0.6 and short length
        if tag == "line":
            try:
                sw_str = elem.attrib.get("stroke-width", "1.0")
                sw = float(re.match(r"^([0-9.]+)", sw_str).group(1))
                if sw <= 0.6:
                    x1 = float(elem.attrib.get("x1", "0"))
                    y1 = float(elem.attrib.get("y1", "0"))
                    x2 = float(elem.attrib.get("x2", "0"))
                    y2 = float(elem.attrib.get("y2", "0"))
                    length = math.hypot(x2 - x1, y2 - y1)
                    if length <= 25.0:
                        to_remove.add(elem)
                        continue
            except (ValueError, AttributeError):
                pass

    # Remove collected elements from their parents
    for elem in to_remove:
        parent = parent_map.get(elem)
        if parent is not None and elem in parent:
            parent.remove(elem)

    output = serialize_svg(root)
    return output


# =============================================================================
# VERB 4: DELIGHT
# =============================================================================

def delight(svg_content: str, motion_type: str = "orbit") -> str:
    """
    Injects subtle micro-motion accents (orbital radar rings or breathing pulses),
    strictly encapsulated using the Wrapper Pattern with transform-box: fill-box;
    transform-origin: center;.
    """
    root = parse_svg(svg_content)

    # 1. Extract viewBox dimensions
    viewbox = root.attrib.get("viewBox", "0 0 800 600")
    parts = [float(p) for p in viewbox.strip().split()]
    min_x, min_y, width, height = (parts[0], parts[1], parts[2], parts[3]) if len(parts) == 4 else (0, 0, 800, 600)

    # Determine focal center point for delight accent (top-right telemetry quadrant or geometric center)
    cx = round(min_x + width * 0.86, 1)
    cy = round(min_y + height * 0.18, 1)
    r = round(max(14.0, min(width, height) * 0.055), 1)

    # Check if delight accent already exists to avoid duplicate injection
    has_delight = False
    for elem in root.iter():
        if "delight" in elem.attrib.get("class", "") or "delight" in elem.attrib.get("id", ""):
            has_delight = True
            break

    if not has_delight:
        # 2. Create the Motion Wrapper Group adhering to the Wrapper Pattern
        wrapper = ET.Element(f"{{{SVG_NS}}}g")
        wrapper.attrib["class"] = "anim-delight-orbit"
        wrapper.attrib["id"] = "wrapper-delight-orbit"

        # Inner geometry node for Inkscape isolation
        geom_group = ET.SubElement(wrapper, f"{{{SVG_NS}}}g")
        geom_group.attrib["id"] = "geom-delight-orbit"
        geom_group.attrib[f"{{{INKSCAPE_NS}}}label"] = "Delight Orbit Accent"

        # Orbit dashed ring
        circle_ring = ET.SubElement(geom_group, f"{{{SVG_NS}}}circle")
        circle_ring.attrib["cx"] = str(cx)
        circle_ring.attrib["cy"] = str(cy)
        circle_ring.attrib["r"] = str(r)
        circle_ring.attrib["fill"] = "none"
        circle_ring.attrib["stroke"] = "#00f0ff"
        circle_ring.attrib["stroke-width"] = "1.2"
        circle_ring.attrib["stroke-dasharray"] = "3 6"
        circle_ring.attrib["opacity"] = "0.65"

        # Satellite blip on orbit
        blip = ET.SubElement(geom_group, f"{{{SVG_NS}}}circle")
        blip.attrib["cx"] = str(round(cx + r, 1))
        blip.attrib["cy"] = str(cy)
        blip.attrib["r"] = "2.5"
        blip.attrib["fill"] = "#00f0ff"

        # Center pulse node
        center_pulse_wrapper = ET.Element(f"{{{SVG_NS}}}g")
        center_pulse_wrapper.attrib["class"] = "anim-delight-pulse"
        center_pulse_wrapper.attrib["id"] = "wrapper-delight-pulse"

        pulse_geom = ET.SubElement(center_pulse_wrapper, f"{{{SVG_NS}}}g")
        pulse_geom.attrib["id"] = "geom-delight-pulse"
        pulse_geom.attrib[f"{{{INKSCAPE_NS}}}label"] = "Delight Pulse Node"

        pulse_dot = ET.SubElement(pulse_geom, f"{{{SVG_NS}}}circle")
        pulse_dot.attrib["cx"] = str(cx)
        pulse_dot.attrib["cy"] = str(cy)
        pulse_dot.attrib["r"] = "3.0"
        pulse_dot.attrib["fill"] = "#00f0ff"
        pulse_dot.attrib["opacity"] = "0.75"

        # Find target layer to attach (accents, motion, geometry, or first non-background layer)
        target_layer = None
        fallback_layer = None
        for g in root.findall(f"{{{SVG_NS}}}g"):
            groupmode = g.attrib.get(f"{{{INKSCAPE_NS}}}groupmode") or g.attrib.get("inkscape:groupmode")
            if groupmode == "layer":
                g_id = g.attrib.get("id", "").lower()
                g_label = (g.attrib.get(f"{{{INKSCAPE_NS}}}label") or g.attrib.get("inkscape:label") or "").lower()
                if any(k in g_id or k in g_label for k in ("accent", "motion", "telemetry", "grid", "geom")):
                    target_layer = g
                    break
                elif "background" not in g_id and "background" not in g_label and "typography" not in g_id:
                    fallback_layer = g

        layer_to_use = target_layer or fallback_layer
        if layer_to_use is not None:
            layer_to_use.append(wrapper)
            layer_to_use.append(center_pulse_wrapper)
        else:
            # Fallback: create layer-accents
            new_layer = ET.SubElement(root, f"{{{SVG_NS}}}g")
            new_layer.attrib["id"] = "layer-accents"
            new_layer.attrib[f"{{{INKSCAPE_NS}}}groupmode"] = "layer"
            new_layer.attrib[f"{{{INKSCAPE_NS}}}label"] = "Accents & Delight"
            new_layer.append(wrapper)
            new_layer.append(center_pulse_wrapper)

    # 3. Inject CSS Keyframes with Universal Transform Contracts into <style>
    delight_css = """
    /* SVG Maestro Delight Micro-Motion Contracts */
    .anim-delight-orbit {
      transform-box: fill-box;
      transform-origin: center;
      animation: delight-orbit 7s linear infinite;
    }
    @keyframes delight-orbit {
      0% {
        transform: rotate(0deg);
      }
      100% {
        transform: rotate(360deg);
      }
    }
    .anim-delight-pulse {
      transform-box: fill-box;
      transform-origin: center;
      animation: delight-pulse 2.2s ease-in-out infinite alternate;
    }
    @keyframes delight-pulse {
      0% {
        transform: scale(0.90);
        opacity: 0.35;
      }
      100% {
        transform: scale(1.10);
        opacity: 0.95;
      }
    }
"""
    style_elem = None
    for elem in root.iter():
        if get_clean_tag(elem) == "style":
            style_elem = elem
            break

    if style_elem is not None:
        if "anim-delight-orbit" not in (style_elem.text or ""):
            style_elem.text = (style_elem.text or "") + delight_css
    else:
        new_style = ET.Element(f"{{{SVG_NS}}}style")
        new_style.text = delight_css
        root.insert(1 if len(root) > 0 and get_clean_tag(root[0]) == "defs" else 0, new_style)

    output = serialize_svg(root)
    return output


# =============================================================================
# VERB 5: ANIMATE
# =============================================================================

def animate(svg_content: str, motion_type: str = "pulse_spin") -> str:
    """
    Transforms a static SVG into a motion asset by identifying central geometry or accents,
    wrapping target elements in <g class="anim-wrapper-...">, and injecting CSS keyframes
    with transform-box: fill-box; transform-origin: center;.
    """
    root = parse_svg(svg_content)
    parent_map = {c: p for p in root.iter() for c in p}

    # Identify candidate elements to animate within non-background, non-typography layers
    candidates: List[Tuple[ET.Element, str]] = []  # (element, animation_style)

    for elem in root.iter():
        tag = get_clean_tag(elem)
        if tag == "svg":
            continue

        # Skip layers themselves
        groupmode = elem.attrib.get(f"{{{INKSCAPE_NS}}}groupmode") or elem.attrib.get("inkscape:groupmode")
        if groupmode == "layer":
            continue

        # Skip elements inside typography or background layers
        p = elem
        skip = False
        while p in parent_map:
            p = parent_map[p]
            p_id = p.attrib.get("id", "").lower()
            p_label = (p.attrib.get(f"{{{INKSCAPE_NS}}}label") or p.attrib.get("inkscape:label") or "").lower()
            if "typography" in p_id or "typography" in p_label or "background" in p_id or "background" in p_label:
                skip = True
                break
        if skip or tag in ("text", "tspan", "switch", "defs", "style", "filter", "linearGradient", "radialGradient", "rect"):
            continue

        elem_id = elem.attrib.get("id", "").lower()

        # Prioritize prominent focal geometry
        if any(k in elem_id for k in ("gauge", "ring", "reticle", "radar", "needle", "spinner")):
            candidates.append((elem, "spin"))
        elif any(k in elem_id for k in ("diamond", "core", "beacon", "center", "symbol", "status")):
            candidates.append((elem, "pulse"))

    # Fallback if no specific ID matched: grab first significant geometric shape/group in geometry layer
    if not candidates:
        for elem in root.iter():
            tag = get_clean_tag(elem)
            if tag in ("circle", "polygon", "path", "g"):
                elem_id = elem.attrib.get("id", "").lower()
                if "bg" not in elem_id and "axis" not in elem_id and "grid" not in elem_id:
                    candidates.append((elem, "spin"))
                    break

    # Wrap target elements in dedicated <g class="anim-wrapper-..."> nodes
    wrapped_count = 0
    for target_elem, anim_kind in candidates[:2]:  # Wrap up to 2 distinct focal points
        parent = parent_map.get(target_elem)
        if parent is None:
            continue

        # Check if already wrapped
        parent_class = parent.attrib.get("class", "")
        if "anim-wrapper" in parent_class:
            continue

        cls_name = f"anim-wrapper-{anim_kind}"
        wrapper_id = f"wrapper-anim-{anim_kind}-{wrapped_count}"

        wrapper = ET.Element(f"{{{SVG_NS}}}g")
        wrapper.attrib["class"] = cls_name
        wrapper.attrib["id"] = wrapper_id

        # Replace target element in parent with wrapper
        target_idx = list(parent).index(target_elem)
        parent.remove(target_elem)
        wrapper.append(target_elem)
        parent.insert(target_idx, wrapper)
        wrapped_count += 1

    # Inject CSS Keyframes with Universal Transform Contract
    animate_css = """
    /* SVG Maestro Motion Transformation Contracts */
    .anim-wrapper-spin {
      transform-box: fill-box;
      transform-origin: center;
      animation: anim-spin 12s linear infinite;
    }
    @keyframes anim-spin {
      0% {
        transform: rotate(0deg);
      }
      100% {
        transform: rotate(360deg);
      }
    }
    .anim-wrapper-pulse {
      transform-box: fill-box;
      transform-origin: center;
      animation: anim-pulse 3.2s ease-in-out infinite alternate;
    }
    @keyframes anim-pulse {
      0% {
        transform: scale(0.96);
        opacity: 0.75;
      }
      100% {
        transform: scale(1.04);
        opacity: 1.0;
      }
    }
"""
    style_elem = None
    for elem in root.iter():
        if get_clean_tag(elem) == "style":
            style_elem = elem
            break

    if style_elem is not None:
        if "anim-wrapper-spin" not in (style_elem.text or ""):
            style_elem.text = (style_elem.text or "") + animate_css
    else:
        new_style = ET.Element(f"{{{SVG_NS}}}style")
        new_style.text = animate_css
        root.insert(1 if len(root) > 0 and get_clean_tag(root[0]) == "defs" else 0, new_style)

    output = serialize_svg(root)
    return output


# =============================================================================
# VERB 6: CRITIQUE
# =============================================================================

def calculate_grade(score: float) -> str:
    """Calculate letter grade from 0-100 score."""
    if score >= 95.0:
        return "A+"
    elif score >= 90.0:
        return "A"
    elif score >= 80.0:
        return "B"
    elif score >= 70.0:
        return "C"
    elif score >= 60.0:
        return "D"
    return "F"


def critique(svg_content: str) -> Dict[str, Any]:
    """
    Emits a structured two-axis review scoring:
    (1) Technical Standards (linter compliance, Inkscape layers, defs hygiene, Wrapper Pattern)
    (2) Aesthetic Craft (proportions, color harmony, typography decoupling, Craft Floor bans)
    Returns detailed scores, grades, highlights, recommendations, and suggested verbs.
    """
    # -------------------------------------------------------------------------
    # Axis 1: Technical Standards (0 - 100)
    # -------------------------------------------------------------------------
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False, encoding="utf-8") as f:
        f.write(svg_content)
        temp_path = f.name

    try:
        val_res = validate_svg_file(temp_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    tech_breakdown = {
        "xml_well_formedness": {"score": 20, "max": 20, "notes": "Valid XML markup syntax"},
        "namespaces_and_viewbox": {"score": 20, "max": 20, "notes": "Root <svg> namespace and viewBox verified"},
        "semantic_layers": {"score": 20, "max": 20, "notes": "Inkscape semantic layers present and labeled"},
        "defs_hygiene": {"score": 20, "max": 20, "notes": "Definitions cleanly encapsulated with descriptive IDs"},
        "wrapper_pattern_and_motion": {"score": 20, "max": 20, "notes": "Universal CSS transform contracts verified"}
    }

    # Evaluate errors and warnings from linter
    for err in val_res.errors:
        code = err["code"]
        if code in ("XML_PARSE_ERROR", "ROOT_NOT_SVG"):
            tech_breakdown["xml_well_formedness"]["score"] = 0
            tech_breakdown["xml_well_formedness"]["notes"] = err["message"]
        elif code in ("MISSING_INKSCAPE_NS", "MISSING_VIEWBOX", "INVALID_VIEWBOX"):
            tech_breakdown["namespaces_and_viewbox"]["score"] = max(0, tech_breakdown["namespaces_and_viewbox"]["score"] - 10)
            tech_breakdown["namespaces_and_viewbox"]["notes"] = err["message"]
        elif code == "NO_INKSCAPE_LAYERS":
            tech_breakdown["semantic_layers"]["score"] = 0
            tech_breakdown["semantic_layers"]["notes"] = "Zero semantic Inkscape layers detected"
        elif code == "MISSING_TRANSFORM_BOX":
            tech_breakdown["wrapper_pattern_and_motion"]["score"] = max(0, tech_breakdown["wrapper_pattern_and_motion"]["score"] - 12)
            tech_breakdown["wrapper_pattern_and_motion"]["notes"] = err["message"]

    for warn in val_res.warnings:
        code = warn["code"]
        if code == "UNLABELED_LAYER":
            tech_breakdown["semantic_layers"]["score"] = max(0, tech_breakdown["semantic_layers"]["score"] - 4)
        elif code in ("MISSING_DEF_ID", "GENERIC_DEF_ID"):
            tech_breakdown["defs_hygiene"]["score"] = max(0, tech_breakdown["defs_hygiene"]["score"] - 5)
            tech_breakdown["defs_hygiene"]["notes"] = "Generic or missing IDs found in <defs>"
        elif code == "MISSING_TRANSFORM_ORIGIN":
            tech_breakdown["wrapper_pattern_and_motion"]["score"] = max(0, tech_breakdown["wrapper_pattern_and_motion"]["score"] - 4)
        elif code == "WRAPPER_PATTERN_COLLISION":
            tech_breakdown["wrapper_pattern_and_motion"]["score"] = max(0, tech_breakdown["wrapper_pattern_and_motion"]["score"] - 10)
            tech_breakdown["wrapper_pattern_and_motion"]["notes"] = "Transform animation attached directly to shape instead of wrapper <g>"

    tech_score = sum(item["score"] for item in tech_breakdown.values())
    if val_res.errors:
        # Hard failure on linter validation errors
        tech_score = min(tech_score, 50)
        tech_grade = "F"
    else:
        tech_score = max(0, min(100, tech_score))
        tech_grade = calculate_grade(tech_score)

    # -------------------------------------------------------------------------
    # Axis 2: Aesthetic Craft (0 - 100)
    # -------------------------------------------------------------------------
    aesthetic_breakdown = {
        "proportions_and_geometry": {"score": 25, "max": 25, "notes": "Geometric scale and aspect ratio analysis"},
        "color_harmony_and_contrast": {"score": 25, "max": 25, "notes": "Palette contrast, luminances, and gradients"},
        "typography_decoupling": {"score": 25, "max": 25, "notes": "Semantic typography hierarchy in layer-typography"},
        "craft_floor_bans": {"score": 25, "max": 25, "notes": "Non-negotiable bans: zero AI clipart, zero muddy ramps"}
    }

    try:
        root = parse_svg(svg_content, upgrade_legacy=False)
    except Exception:
        root = None

    highlights = []
    recommendations = []
    suggested_verbs = []

    if root is not None:
        # 1. Proportions & Geometry Analysis
        viewbox = root.attrib.get("viewBox", "")
        if viewbox:
            v_parts = [float(p) for p in re.findall(r"[-+]?(?:\d*\.\d+|\d+)", viewbox)]
            if len(v_parts) == 4 and v_parts[3] > 0:
                aspect_ratio = v_parts[2] / v_parts[3]
                # Compare to Golden Ratio (1.618), 16:9 (1.778), 4:3 (1.333), 1:1 (1.0), 2.333
                if abs(aspect_ratio - 1.618) < 0.05:
                    aesthetic_breakdown["proportions_and_geometry"]["notes"] = f"Golden ratio viewport ({v_parts[2]}x{v_parts[3]}) aligns with Fibonacci proportions"
                    highlights.append("Exceptional Golden Ratio proportioning (~1.618)")
                elif abs(aspect_ratio - (16 / 9)) < 0.05:
                    aesthetic_breakdown["proportions_and_geometry"]["notes"] = f"Standard broadcast 16:9 viewport ({v_parts[2]}x{v_parts[3]})"
                    highlights.append("Standard broadcast 16:9 viewport ratio for streaming overlay")
                elif abs(aspect_ratio - 1.6) < 0.05:
                    aesthetic_breakdown["proportions_and_geometry"]["notes"] = f"Intentional modular 8:5 ratio ({v_parts[2]}x{v_parts[3]})"
                    highlights.append("Clean 8:5 modular grid ratio")
                else:
                    aesthetic_breakdown["proportions_and_geometry"]["score"] = 22
                    aesthetic_breakdown["proportions_and_geometry"]["notes"] = f"Custom aspect ratio ({aspect_ratio:.2f})"

        # 2. Color Harmony & Palette Contrast Analysis
        hex_colors = set(re.findall(r"#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}", svg_content))
        has_gradients = len(root.findall(".//{http://www.w3.org/2000/svg}linearGradient") + root.findall(".//linearGradient")) > 0

        dark_shades = 0
        luminous_accents = 0
        for c in hex_colors:
            rgb = hex_to_rgb(c)
            if rgb:
                _, l, s = colorsys.rgb_to_hls(*rgb)
                if l < 0.2:
                    dark_shades += 1
                elif s > 0.4 and l > 0.35:
                    luminous_accents += 1

        if dark_shades > 0 and luminous_accents > 0:
            highlights.append("High visual contrast heuristic between chassis and luminous accents")
            if has_gradients:
                aesthetic_breakdown["color_harmony_and_contrast"]["notes"] = "Harmonious palette with deep darks, luminous accents, and smooth gradient ramps"
            else:
                aesthetic_breakdown["color_harmony_and_contrast"]["score"] = 23
                aesthetic_breakdown["color_harmony_and_contrast"]["notes"] = "Good contrast, but could benefit from gradient luminescence"
                suggested_verbs.append("bolder")
        else:
            aesthetic_breakdown["color_harmony_and_contrast"]["score"] = 19
            aesthetic_breakdown["color_harmony_and_contrast"]["notes"] = "Limited tonal contrast detected"
            recommendations.append("Consider running `bolder` to increase luminescence contrast between base and accents")
            suggested_verbs.append("bolder")

        # 3. Typography Decoupling Analysis
        text_nodes = root.findall(".//{http://www.w3.org/2000/svg}text") + root.findall(".//text")
        if text_nodes:
            # Check if text is placed in a dedicated typography layer
            in_typo_layer = False
            for g in root.findall(".//{http://www.w3.org/2000/svg}g") + root.findall(".//g"):
                g_id = g.attrib.get("id", "").lower()
                g_label = (g.attrib.get(f"{{{INKSCAPE_NS}}}label") or g.attrib.get("inkscape:label") or "").lower()
                if "typography" in g_id or "typography" in g_label or "text" in g_label:
                    if len(g.findall(".//{http://www.w3.org/2000/svg}text") + g.findall(".//text")) > 0:
                        in_typo_layer = True
                        break

            if in_typo_layer:
                highlights.append("Typography decoupled cleanly in dedicated Inkscape layer (layer-typography)")
                aesthetic_breakdown["typography_decoupling"]["notes"] = "Semantic <text> elements isolated in dedicated typography layer"
            else:
                aesthetic_breakdown["typography_decoupling"]["score"] = 21
                aesthetic_breakdown["typography_decoupling"]["notes"] = "Text elements present but scattered across non-typography layers"
                recommendations.append("Isolate all <text> elements in layer-typography for effortless translation and i18n")
        else:
            # Standalone geometric vector without text
            aesthetic_breakdown["typography_decoupling"]["notes"] = "Clean non-typographic vector graphic"

        # 4. Craft Floor Bans Analysis
        raw_lower = svg_content.lower()
        if any(banned in raw_lower for banned in ("clipart", "lightbulb", "gear-cartoon", "floating gear", "cartoon mascot")):
            aesthetic_breakdown["craft_floor_bans"]["score"] = 0
            aesthetic_breakdown["craft_floor_bans"]["notes"] = "VIOLATION: Generic AI clipart keyword detected"
            recommendations.append("Remove generic clipart and replace with mathematical Euclidean geometry")
        else:
            aesthetic_breakdown["craft_floor_bans"]["notes"] = "Zero AI clipart; pure Euclidean vector craft confirmed"
            highlights.append("Adheres strictly to the Craft Floor (zero generic clipart)")

    aesthetic_score = sum(item["score"] for item in aesthetic_breakdown.values())
    aesthetic_score = max(0, min(100, aesthetic_score))
    aesthetic_grade = calculate_grade(aesthetic_score)

    # -------------------------------------------------------------------------
    # Composite Score & Synthesis
    # -------------------------------------------------------------------------
    composite_score = round(0.5 * tech_score + 0.5 * aesthetic_score, 1)
    composite_grade = calculate_grade(composite_score)

    # Motion suggestions
    if val_res.stats.get("animated_elements_count", 0) == 0:
        recommendations.append("SVG is static. Run `animate` or `delight` to add subtle ambient motion")
        if "animate" not in suggested_verbs:
            suggested_verbs.append("animate")
        if "delight" not in suggested_verbs:
            suggested_verbs.append("delight")
    else:
        highlights.append(f"Contains {val_res.stats.get('animated_elements_count')} motion elements adhering to Wrapper Pattern")

    # Legacy asset upgrade suggestions
    if val_res.errors or val_res.warnings:
        recommendations.append("Legacy or non-compliant SVG detected. Run any SVG Maestro refinement verb (`bolder`, `quieter`, `animate`, `delight`) to auto-upgrade to modern standards.")
        if hasattr(val_res, "hints") and val_res.hints:
            for h in val_res.hints:
                recommendations.append(f"Upgrade Suggestion: {h['message']}")
        if "bolder" not in suggested_verbs:
            suggested_verbs.append("bolder")

    if not suggested_verbs:
        suggested_verbs = ["delight", "bolder"]

    return {
        "valid": val_res.is_valid and len(val_res.warnings) == 0,
        "composite_score": composite_score,
        "composite_grade": composite_grade,
        "technical_standards": {
            "score": tech_score,
            "grade": tech_grade,
            "breakdown": tech_breakdown,
            "errors": val_res.errors,
            "warnings": val_res.warnings
        },
        "aesthetic_craft": {
            "score": aesthetic_score,
            "grade": aesthetic_grade,
            "breakdown": aesthetic_breakdown,
            "critique": [v["notes"] for v in aesthetic_breakdown.values()]
        },
        "highlights": highlights,
        "recommendations": recommendations,
        "suggested_verbs": suggested_verbs
    }


def critique_file(filepath: str) -> Dict[str, Any]:
    """Load an SVG file and generate a structured critique report."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return critique(content)


def format_critique_markdown(report: Dict[str, Any], target_name: str = "Target SVG") -> str:
    """Format structured critique report into a beautiful Markdown presentation."""
    tech = report["technical_standards"]
    aest = report["aesthetic_craft"]

    md = []
    md.append(f"# SVG Maestro Design Critique Report")
    md.append(f"")
    md.append(f"**Target**: `{target_name}`  ")
    md.append(f"**Composite Score**: **{report['composite_score']} / 100** — **Grade**: `[{report['composite_grade']}]`  ")
    md.append(f"**Contract Status**: {'[PASS] VALID (0 Errors, 0 Warnings)' if report['valid'] else '[WARN] Linter findings detected'}")
    md.append(f"")
    md.append(f"---")
    md.append(f"")
    md.append(f"## Axis 1: Technical Standards — {tech['score']}/100 `[{tech['grade']}]`")
    for key, data in tech["breakdown"].items():
        title = key.replace("_", " ").title()
        md.append(f"- **{title}**: `{data['score']}/{data['max']}` — {data['notes']}")
    md.append(f"")

    md.append(f"## Axis 2: Aesthetic Craft — {aest['score']}/100 `[{aest['grade']}]`")
    for key, data in aest["breakdown"].items():
        title = key.replace("_", " ").title()
        md.append(f"- **{title}**: `{data['score']}/{data['max']}` — {data['notes']}")
    md.append(f"")

    if report["highlights"]:
        md.append(f"### Highlights")
        for h in report["highlights"]:
            md.append(f"- {h}")
        md.append(f"")

    if report["recommendations"]:
        md.append(f"### Recommendations")
        for r in report["recommendations"]:
            md.append(f"- {r}")
        md.append(f"")

    if report["suggested_verbs"]:
        md.append(f"### Suggested Refinement Verbs")
        for v in report["suggested_verbs"]:
            md.append(f"- `/svg-maestro {v}`")
        md.append(f"")

    return "\n".join(md)


# =============================================================================
# UNIFIED DISPATCH & FILE API
# =============================================================================

VERB_MAP = {
    "bolder": bolder,
    "quieter": quieter,
    "distill": distill,
    "delight": delight,
    "animate": animate,
    "upgrade": upgrade_legacy_svg,
}


def apply_verb(verb: str, svg_content: str, **kwargs) -> str:
    """Apply a refinement verb to an SVG string and guarantee validator compliance."""
    v_clean = verb.strip().lower()
    if v_clean not in VERB_MAP:
        raise ValueError(f"Unknown refinement verb: '{verb}'. Available: {list(VERB_MAP.keys())} or 'critique'")

    transform_fn = VERB_MAP[v_clean]
    refined_svg = transform_fn(svg_content, **kwargs)

    # Autonomous self-validation contract
    is_valid, errors, warnings = validate_content(refined_svg)
    if not is_valid:
        raise RuntimeError(f"Refinement verb '{verb}' produced non-compliant SVG: Errors: {errors}, Warnings: {warnings}")

    return refined_svg


def resolve_destination_path(
    input_path: str,
    verb: str,
    output_path: Optional[str] = None,
    in_place: bool = False
) -> str:
    """Resolve destination path for a refinement verb output.

    Safety contract:
    - If output_path is provided, use output_path.
    - If in_place is True, overwrite input_path.
    - Otherwise, default to safe derived path: <input_stem>_<verb>.svg.
    """
    if output_path:
        return output_path
    if in_place:
        return input_path
    base, ext = os.path.splitext(input_path)
    return f"{base}_{verb}{ext}"


def apply_verb_file(
    verb: str,
    input_path: str,
    output_path: Optional[str] = None,
    in_place: bool = False,
    **kwargs
) -> Tuple[str, str]:
    """Apply a refinement verb to an SVG file and write the result.

    Returns:
        Tuple[str, str]: (refined_svg_content, destination_path)
    """
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    refined = apply_verb(verb, content, **kwargs)
    dest_path = resolve_destination_path(input_path, verb, output_path=output_path, in_place=in_place)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(refined)

    return refined, dest_path


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        description="SVG Maestro - Art Direction Refinement Verbs CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/refinement_verbs.py bolder --input card.svg --output card_bolder.svg
  python scripts/refinement_verbs.py quieter --input card.svg  # writes to card_quieter.svg
  python scripts/refinement_verbs.py distill --input widget.svg --in-place  # overwrites widget.svg
  python scripts/refinement_verbs.py delight --input overlay.svg
  python scripts/refinement_verbs.py animate --input static_card.svg
  python scripts/refinement_verbs.py critique --input card.svg
  python scripts/refinement_verbs.py critique --input card.svg --json
"""
    )

    parser.add_argument("verb", nargs="?", choices=["bolder", "quieter", "distill", "delight", "animate", "critique", "upgrade"],
                        help="Creative refinement verb to execute")
    parser.add_argument("-i", "--input", required=False, help="Input SVG file path")

    dest_group = parser.add_mutually_exclusive_group()
    dest_group.add_argument("-o", "--output", help="Output SVG file path (default: <input>_<verb>.svg)")
    dest_group.add_argument("--in-place", action="store_true", help="Overwrite the input SVG file directly instead of creating a derived file")

    parser.add_argument("--check-update", action="store_true", help="Check for SVG Maestro updates")
    parser.add_argument("--json", action="store_true", help="Output critique results as JSON")
    parser.add_argument("--factor", type=float, help="Scale factor for bolder or quieter verbs")

    args = parser.parse_args()

    if args.check_update:
        try:
            from update_notifier import check_for_updates, print_update_banner
            up_res = check_for_updates()
            if up_res and up_res.get("update_available"):
                print_update_banner(up_res, stream=sys.stderr)
            elif not args.input and not args.verb:
                print(f"[OK] SVG Maestro is up to date (v{up_res.get('current_version', '') if up_res else ''}).")
        except Exception:
            pass
        if not args.input or not args.verb:
            sys.exit(0)

    if not args.verb or not args.input:
        parser.print_help(sys.stderr)
        sys.exit(2)

    if not os.path.exists(args.input):
        print(f"Error: Input file does not exist: {args.input}", file=sys.stderr)
        sys.exit(1)

    if args.verb == "critique":
        report = critique_file(args.input)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(format_critique_markdown(report, target_name=args.input))
        sys.exit(0)

    # Modification verbs
    kwargs = {}
    if args.factor is not None:
        kwargs["factor"] = args.factor

    try:
        _, dest_path = apply_verb_file(
            args.verb,
            args.input,
            output_path=args.output,
            in_place=args.in_place,
            **kwargs
        )
        print(f"[OK] Refinement verb '{args.verb}' successfully applied.")
        print(f"     Output saved to: {dest_path}")
        sys.exit(0)
    except Exception as e:
        print(f"Error executing '{args.verb}': {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
