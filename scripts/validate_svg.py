#!/usr/bin/env python3
"""
SVG Maestro - Autonomous SVG Linter & Validation Engine
Zero-dependency validator for Inkscape compatibility, mutation-proof animation wrappers,
viewBox accuracy, defs hygiene, and CSS keyframe contracts.
"""

import sys
import os
import re
import json
import argparse
import xml.etree.ElementTree as ET

# Inkscape & XML Namespaces
NAMESPACES = {
    'svg': 'http://www.w3.org/2000/svg',
    'inkscape': 'http://www.inkscape.org/namespaces/inkscape',
    'sodipodi': 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
    'xlink': 'http://www.w3.org/1999/xlink'
}

def get_tag(elem):
    """Safely return tag name without namespace, handling comments or non-string tags."""
    if not hasattr(elem, 'tag') or not isinstance(elem.tag, str):
        return ''
    return elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag

class ValidationResult:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.hints = []
        self.stats = {
            'layers_count': 0,
            'animated_elements_count': 0,
            'defs_count': 0,
            'has_viewbox': False,
            'has_inkscape_ns': False,
            'text_nodes_count': 0,
            'switch_nodes_count': 0
        }

    def error(self, code, message, element=None, hint=None):
        entry = {'code': code, 'message': message}
        if element is not None:
            entry['tag'] = get_tag(element)
            entry['id'] = element.attrib.get('id', 'unnamed') if hasattr(element, 'attrib') else 'unnamed'
        if hint is not None:
            entry['hint'] = hint
            self.hint(f"UPGRADE_{code}", hint, element)
        self.errors.append(entry)

    def warning(self, code, message, element=None, hint=None):
        entry = {'code': code, 'message': message}
        if element is not None:
            tag = get_tag(element)
            if tag:
                entry['tag'] = tag
            if hasattr(element, 'attrib'):
                entry['id'] = element.attrib.get('id', 'unnamed')
        if hint is not None:
            entry['hint'] = hint
            self.hint(f"UPGRADE_{code}", hint, element)
        self.warnings.append(entry)

    def hint(self, code, message, element=None):
        entry = {'code': code, 'message': message}
        if element is not None:
            tag = get_tag(element)
            if tag:
                entry['tag'] = tag
            if hasattr(element, 'attrib'):
                entry['id'] = element.attrib.get('id', 'unnamed')
        if not any(h['code'] == entry['code'] and h['message'] == entry['message'] for h in self.hints):
            self.hints.append(entry)

    @property
    def is_valid(self):
        return len(self.errors) == 0

    def to_dict(self):
        return {
            'valid': self.is_valid,
            'errors_count': len(self.errors),
            'warnings_count': len(self.warnings),
            'hints_count': len(self.hints),
            'errors': self.errors,
            'warnings': self.warnings,
            'hints': self.hints,
            'stats': self.stats
        }

def validate_svg_file(filepath):
    result = ValidationResult()

    if not os.path.exists(filepath):
        result.error("FILE_NOT_FOUND", f"File does not exist: {filepath}")
        return result

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_content = f.read()
    except Exception as e:
        result.error("READ_ERROR", f"Could not read file: {str(e)}")
        return result

    # 1. XML Well-formedness
    try:
        # Register namespaces to preserve prefixes during parse
        for prefix, uri in NAMESPACES.items():
            ET.register_namespace(prefix, uri)
        root = ET.fromstring(raw_content)
    except ET.ParseError as e:
        err_msg = str(e)
        if "unbound prefix" in err_msg.lower():
            pfx = "inkscape"
            for p in NAMESPACES.keys():
                if f"<{p}:" in raw_content or f" {p}:" in raw_content:
                    pfx = p
                    break
            result.error("MISSING_INKSCAPE_NS" if pfx == "inkscape" else "XML_PARSE_ERROR",
                         f"Undeclared XML namespace prefix '{pfx}'. Root <svg> must declare xmlns:{pfx}='...'",
                         hint=f"Add xmlns:{pfx}='{NAMESPACES.get(pfx, '...')}' to root <svg> or run SVG Maestro refinement verbs to auto-upgrade.")
            try:
                fixed_content = raw_content
                for p, uri in NAMESPACES.items():
                    if f"xmlns:{p}=" not in fixed_content:
                        fixed_content = re.sub(r'<svg\b', f'<svg xmlns:{p}="{uri}"', fixed_content, count=1)
                root = ET.fromstring(fixed_content)
            except Exception:
                return result
        else:
            result.error("XML_PARSE_ERROR", f"Malformed XML: {str(e)}")
            return result

    # 2. Root Element and Namespace Verification
    root_tag = get_tag(root)
    if root_tag != 'svg':
        result.error("ROOT_NOT_SVG", f"Root element must be <svg>, got <{root_tag}>",
                     hint="Wrap artwork in a root <svg xmlns='http://www.w3.org/2000/svg' ...> document.")
        return result

    # Check xmlns:inkscape in raw content (ElementTree strips or abstracts raw xmlns attributes)
    has_inkscape_ns = 'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"' in raw_content or \
                      "xmlns:inkscape='http://www.inkscape.org/namespaces/inkscape'" in raw_content
    result.stats['has_inkscape_ns'] = has_inkscape_ns
    if not has_inkscape_ns:
        result.error("MISSING_INKSCAPE_NS", "Root <svg> must declare xmlns:inkscape='http://www.inkscape.org/namespaces/inkscape'",
                     hint="Declare xmlns:inkscape='http://www.inkscape.org/namespaces/inkscape' on root <svg> or run SVG Maestro refinement verbs to auto-upgrade.")

    # Check viewBox
    viewbox = root.attrib.get('viewBox')
    if not viewbox:
        result.error("MISSING_VIEWBOX", "Root <svg> must define a 'viewBox' attribute",
                     hint="Add a viewBox attribute (e.g. viewBox='0 0 width height') to enable responsive vector scaling.")
    else:
        result.stats['has_viewbox'] = True
        parts = [p for p in re.split(r'[\s,]+', viewbox.strip()) if p]
        if len(parts) != 4:
            result.error("INVALID_VIEWBOX", f"viewBox must contain 4 space-delimited values (minX minY width height), got '{viewbox}'",
                         hint="Provide 4 space-delimited numerical values for viewBox='minX minY width height'.")

    # 3. Defs Hygiene and ID Naming
    defs_nodes = root.findall('{http://www.inkscape.org/namespaces/inkscape}defs') + \
                 root.findall('{http://www.w3.org/2000/svg}defs') + \
                 root.findall('defs')
    result.stats['defs_count'] = len(defs_nodes)

    # Search for gradients/filters declared outside <defs>
    for elem in root.iter():
        tag = get_tag(elem)
        if tag in ('linearGradient', 'radialGradient', 'filter', 'pattern', 'clipPath'):
            elem_id = elem.attrib.get('id', '')
            if not elem_id:
                result.warning("MISSING_DEF_ID", f"<{tag}> element should have a descriptive id", elem,
                               hint="Assign a descriptive id attribute (e.g. id='grad-primary') to definition elements.")
            elif re.match(r'^(linearGradient|radialGradient|filter)\d+$', elem_id):
                result.warning("GENERIC_DEF_ID", f"Descriptive id recommended for <{tag}>, avoid generic '{elem_id}'", elem,
                               hint="Rename generic IDs like 'linearGradient1' to descriptive names (e.g. 'grad-accent-core').")

    # 4. Semantic Inkscape Layers Verification
    inkscape_groupmode_key = '{http://www.inkscape.org/namespaces/inkscape}groupmode'
    inkscape_label_key = '{http://www.inkscape.org/namespaces/inkscape}label'

    layers_found = []
    for g in root.findall('{http://www.w3.org/2000/svg}g') + root.findall('g'):
        groupmode = g.attrib.get(inkscape_groupmode_key) or g.attrib.get('inkscape:groupmode')
        label = g.attrib.get(inkscape_label_key) or g.attrib.get('inkscape:label')

        if groupmode == 'layer':
            layers_found.append(label or 'unnamed-layer')
            if not label:
                result.warning("UNLABELED_LAYER", "Layer has inkscape:groupmode='layer' but missing inkscape:label", g,
                               hint="Add inkscape:label='Layer Name' attribute to the layer group.")

            # Check for Typography Layer & Outlined Text
            label_lower = (label or '').lower()
            layer_id_lower = (g.attrib.get('id') or '').lower()
            is_typo_layer = any(term in label_lower for term in ('typography', 'text', 'label')) or \
                            any(term in layer_id_lower for term in ('typography', 'text', 'label'))

            if is_typo_layer:
                layer_texts = 0
                layer_switches = 0
                layer_shapes = 0
                shape_tags = {'path', 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon'}
                for child in g.iter():
                    if child is g:
                        continue
                    ctag = get_tag(child)
                    if ctag == 'text':
                        layer_texts += 1
                    elif ctag == 'switch':
                        layer_switches += 1
                    elif ctag in shape_tags:
                        layer_shapes += 1

                if layer_shapes > 0 and layer_texts == 0 and layer_switches == 0:
                    result.warning("OUTLINED_TEXT_WARNING",
                        f"Typography layer '{label or layer_id_lower}' contains vector paths/shapes but zero semantic <text> or <switch> nodes. "
                        f"Ensure text is authored as editable <text> tags rather than outlined vector paths.",
                        g,
                        hint="Author text as editable <text> tags rather than outlined vector paths for i18n.")

    result.stats['layers_count'] = len(layers_found)
    if len(layers_found) == 0:
        result.error("NO_INKSCAPE_LAYERS", "No semantic Inkscape layers found. Main groups must use inkscape:groupmode='layer' and inkscape:label='...'",
                     hint="Wrap artwork in semantic layer groups with inkscape:groupmode='layer' and inkscape:label='...' (e.g. Background, Geometry, Typography).")

    # 5. Animation Verification & Mutation-Proof Wrapper Pattern
    style_nodes = root.findall('.//{http://www.w3.org/2000/svg}style') + root.findall('.//style')
    has_css_animation = False
    css_content = ""
    for s in style_nodes:
        if s.text:
            css_content += s.text
            if '@keyframes' in s.text or 'animation' in s.text:
                has_css_animation = True

    # Check SMIL animations
    smil_tags = {'animate', 'animateTransform', 'animateMotion'}
    smil_nodes = []
    for elem in root.iter():
        tag = get_tag(elem)
        if tag in smil_tags:
            smil_nodes.append(elem)

    result.stats['animated_elements_count'] = len(smil_nodes) + (1 if has_css_animation else 0)

    # Validate CSS animation transform-box and transform-origin
    if has_css_animation:
        # Check if transform animations exist without transform-box: fill-box
        if 'transform:' in css_content or 'rotate(' in css_content or 'scale(' in css_content:
            if 'transform-box' not in css_content or 'fill-box' not in css_content:
                result.error("MISSING_TRANSFORM_BOX", "CSS animations using transforms must specify 'transform-box: fill-box;' to ensure reliable rotation/scaling across browsers and preserve Inkscape positioning",
                             hint="Add 'transform-box: fill-box;' to CSS rules animating transforms to preserve element origin in Inkscape.")
            if 'transform-origin' not in css_content:
                result.warning("MISSING_TRANSFORM_ORIGIN", "CSS transform animations should explicitly specify 'transform-origin' (e.g. 'transform-origin: center;')",
                               hint="Add 'transform-origin: center;' to CSS transform classes to ensure uniform rotation/scaling across SVG renderers.")

    # Validate Wrapper Pattern (Isolation of Motion vs Content)
    if has_css_animation:
        # Map keyframe names to their body contents
        keyframes = {}
        for kf_match in re.finditer(r'@keyframes\s+([a-zA-Z0-9_-]+)\s*\{([\s\S]*?)\}(?=\s*(@keyframes|\s*$|[^{]*\{))', css_content):
            kf_name = kf_match.group(1)
            kf_body = kf_match.group(2)
            keyframes[kf_name] = kf_body

        # Match classes and their animation names
        class_rules = re.findall(r'\.([a-zA-Z0-9_-]+)\s*\{([^}]*)\}', css_content)
        for cls_name, cls_body in class_rules:
            anim_match = re.search(r'animation\s*:\s*([a-zA-Z0-9_-]+)', cls_body)
            if not anim_match:
                continue
            anim_name = anim_match.group(1)
            kf_body = keyframes.get(anim_name, '')
            animates_transform = 'transform' in kf_body or 'rotate' in kf_body or 'scale' in kf_body

            if animates_transform:
                # Find all elements using this class
                for elem in root.findall(".//*[@class]"):
                    cls_attr = elem.attrib.get('class', '')
                    if cls_name in cls_attr.split():
                        tag = get_tag(elem)
                        if tag not in ('g',):
                            result.warning("WRAPPER_PATTERN_COLLISION",
                                f"Element <{tag} class='{cls_attr}'> uses transform animation '{anim_name}'. "
                                f"Wrap it in a dedicated '<g class=\"anim-wrapper-...\">' to prevent Inkscape transforms from breaking motion.", elem,
                                hint="Wrap animated element inside a dedicated '<g class=\"anim-wrapper-...\">' to isolate motion from Inkscape element coordinates.")

    # 6. Typography & Internationalization (i18n) Verification
    switch_nodes = []
    text_count = 0
    for elem in root.iter():
        tag = get_tag(elem)
        if tag == 'text':
            text_count += 1
        elif tag == 'switch':
            switch_nodes.append(elem)

    result.stats['text_nodes_count'] = text_count
    result.stats['switch_nodes_count'] = len(switch_nodes)

    for sw in switch_nodes:
        children = list(sw)
        if len(children) == 0:
            result.warning("SWITCH_EMPTY", "<switch> element has no child alternatives", sw,
                           hint="Add language-specific text alternatives inside <switch>.")
            continue

        if len(children) == 1:
            child = children[0]
            if child.attrib.get('systemLanguage'):
                result.warning("SWITCH_MISSING_FALLBACK",
                    "<switch> with a language alternative should provide a fallback element without systemLanguage as its last child", sw,
                    hint="Provide a default fallback element without systemLanguage as the last child of <switch>.")
            continue

        # Check that non-final children have systemLanguage
        for idx, child in enumerate(children[:-1]):
            sys_lang = child.attrib.get('systemLanguage')
            if not sys_lang or not sys_lang.strip():
                ctag = get_tag(child)
                result.warning("SWITCH_FALLBACK_ORDER",
                    f"Child {idx + 1} (<{ctag}>) inside <switch> lacks 'systemLanguage' attribute. "
                    f"Fallback elements must be positioned as the last child of <switch> to avoid intercepting language alternatives.",
                    child,
                    hint="Move the default fallback element to be the last child of <switch>.")

        # Check that the last child is a fallback without systemLanguage
        last_child = children[-1]
        last_sys_lang = last_child.attrib.get('systemLanguage')
        if last_sys_lang and last_sys_lang.strip():
            result.warning("SWITCH_MISSING_FALLBACK",
                "<switch> element should provide a default fallback child without 'systemLanguage' as its last element",
                sw,
                hint="Provide a default fallback element without systemLanguage as the last child of <switch>.")

    return result

def main():
    parser = argparse.ArgumentParser(description="SVG Maestro - SVG Validation Engine")
    parser.add_argument("file", nargs="?", default=None, help="Path to SVG file to validate")
    parser.add_argument("--check-update", action="store_true", help="Check for SVG Maestro updates")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings as well as errors")
    args = parser.parse_args()

    if args.check_update:
        try:
            from update_notifier import check_for_updates, print_update_banner
            up_res = check_for_updates()
            if up_res and up_res.get("update_available"):
                print_update_banner(up_res, stream=sys.stderr)
            elif not args.file and not args.json:
                print(f"[OK] SVG Maestro is up to date (v{up_res.get('current_version', '') if up_res else ''}).")
        except Exception:
            pass
        if not args.file:
            sys.exit(0)

    if not args.file:
        parser.print_help(sys.stderr)
        sys.exit(2)

    result = validate_svg_file(args.file)

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(f"\n==========================================")
        print(f" SVG Maestro Validation Report")
        print(f" Target: {args.file}")
        print(f" Status: {'[PASS] VALID' if (result.is_valid and (not args.strict or len(result.warnings) == 0)) else '[FAIL] INVALID'}")
        print(f"==========================================\n")

        print(f"Stats:")
        for k, v in result.stats.items():
            print(f"  - {k}: {v}")
        print()

        if result.errors:
            print(f"[!] ERRORS ({len(result.errors)}):")
            for err in result.errors:
                print(f"  * [{err['code']}] {err['message']}")
            print()

        if result.warnings:
            print(f"[*] WARNINGS ({len(result.warnings)}):")
            for warn in result.warnings:
                print(f"  * [{warn['code']}] {warn['message']}")
            print()

        if result.hints:
            print(f"[i] ACTIONABLE UPGRADE HINTS ({len(result.hints)}):")
            for h in result.hints:
                print(f"  -> [{h['code']}] {h['message']}")
            print()

        if result.is_valid and not result.warnings:
            print("Perfect! SVG conforms completely to Inkscape semantic layers, defs hygiene, and animation wrapper contracts.")

    if not result.is_valid or (args.strict and result.warnings):
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
