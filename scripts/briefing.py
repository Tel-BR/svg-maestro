#!/usr/bin/env python3
"""
SVG Maestro - Interactive Briefing Protocol & BRIEF.md Module
Fuses Matt Pocock's architectural discipline with Impeccable's radical art direction.

Provides:
1. Formal definitions for the 4 core vector dimensions:
   - Surface Viewport (16:9 Webcam Overlay, Telemetry Card, Alert Banner, Square Widget, Monumental Hero)
   - Surface Mode (Operate, Experience, Persuade)
   - Motion Profile (Continuous Line Tracing, Ambient Radar Spin / Breathing Pulse, SMIL Path Morphing, Static)
   - Handoff Target (Inkscape Manual Vector, OBS Studio Browser Source, Web DOM / HTML, Power BI DAX String)
2. Helper functions to build interactive `ask_question` payloads with recommended defaults in EN and PT-BR.
3. Generator for binding, structured `BRIEF.md` contracts.
4. Autonomous parser and validator enforcing that all 4 core dimensions exist before SVG code generation.
5. CLI and programmatic API.
"""

import os
import sys
import re
import json
import argparse
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict


# ---------------------------------------------------------------------------
# 1. CORE VECTOR DIMENSION DEFINITIONS & SPECIFICATIONS
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ViewportSpec:
    key: str
    name_en: str
    name_pt: str
    width: int
    height: int
    aspect_ratio: str
    description_en: str
    description_pt: str

    @property
    def viewbox(self) -> str:
        return f"0 0 {self.width} {self.height}"


@dataclass(frozen=True)
class ModeSpec:
    key: str
    name: str
    description_en: str
    description_pt: str


@dataclass(frozen=True)
class MotionSpec:
    key: str
    name: str
    tier: str
    description_en: str
    description_pt: str


@dataclass(frozen=True)
class HandoffSpec:
    key: str
    name: str
    description_en: str
    description_pt: str


VIEWPORTS: Dict[str, ViewportSpec] = {
    "webcam_16_9": ViewportSpec(
        key="webcam_16_9",
        name_en="16:9 Webcam Overlay (1920x1080)",
        name_pt="Overlay de Webcam 16:9 (1920x1080)",
        width=1920,
        height=1080,
        aspect_ratio="16:9",
        description_en="OBS Studio stream frame with transparent center and corner brackets",
        description_pt="Moldura de stream para OBS Studio com centro transparente e cantoneiras",
    ),
    "telemetry_card": ViewportSpec(
        key="telemetry_card",
        name_en="Telemetry Card (800x500)",
        name_pt="Cartão de Telemetria (800x500)",
        width=800,
        height=500,
        aspect_ratio="8:5",
        description_en="Modular dashboard card with high-scanability metric readouts",
        description_pt="Cartão modular de dashboard com leituras métricas de alta escaneabilidade",
    ),
    "alert_banner": ViewportSpec(
        key="alert_banner",
        name_en="Alert Banner (1200x300)",
        name_pt="Banner de Alerta (1200x300)",
        width=1200,
        height=300,
        aspect_ratio="4:1",
        description_en="Horizontal stream notification, event trigger, or status ticker",
        description_pt="Banner horizontal de notificação de stream, evento ou ticker de status",
    ),
    "square_widget": ViewportSpec(
        key="square_widget",
        name_en="Square Widget (600x600)",
        name_pt="Widget Quadrado (600x600)",
        width=600,
        height=600,
        aspect_ratio="1:1",
        description_en="Compact square badge, avatar frame, or telemetry gauge indicator",
        description_pt="Badge quadrado compacto, moldura de avatar ou indicador de gauge",
    ),
    "monumental_hero": ViewportSpec(
        key="monumental_hero",
        name_en="Monumental Hero Canvas (1920x1080)",
        name_pt="Hero Canvas Monumental (1920x1080)",
        width=1920,
        height=1080,
        aspect_ratio="16:9",
        description_en="Monumental Euclidean architectural showcase banner and brand art",
        description_pt="Banner arquitetural euclidiano monumental para arte e marca",
    ),
}

SURFACE_MODES: Dict[str, ModeSpec] = {
    "experience": ModeSpec(
        key="experience",
        name="Experience",
        description_en="Vibrant cyber neon illumination, high contrast, and ambient motion for OBS/streaming",
        description_pt="Iluminação neon cyber vibrante, alto contraste e movimento ambiente para OBS/streaming",
    ),
    "operate": ModeSpec(
        key="operate",
        name="Operate",
        description_en="Data density, crisp legibility, and high scanability for dashboards and Power BI",
        description_pt="Densidade de dados, legibilidade nítida e alta escaneabilidade para dashboards e Power BI",
    ),
    "persuade": ModeSpec(
        key="persuade",
        name="Persuade",
        description_en="Monumental Euclidean scale, golden ratio harmony, and emotional brand resonance",
        description_pt="Escala euclidiana monumental, harmonia da proporção áurea e ressonância emocional",
    ),
}

MOTION_PROFILES: Dict[str, MotionSpec] = {
    "radar_pulse": MotionSpec(
        key="radar_pulse",
        name="Ambient Radar Spin / Breathing Pulse",
        tier="Tier 1 CSS",
        description_en="Subtle continuous rotation or breathing scale with transform-box: fill-box",
        description_pt="Rotação contínua sutil ou pulso de respiração com transform-box: fill-box",
    ),
    "line_tracing": MotionSpec(
        key="line_tracing",
        name="Continuous Line Tracing",
        tier="Tier 1 CSS",
        description_en="Continuous stroke-dasharray and stroke-dashoffset loop animation",
        description_pt="Animação contínua em loop de traçado de linhas (stroke-dasharray/dashoffset)",
    ),
    "path_morphing": MotionSpec(
        key="path_morphing",
        name="SMIL Path Morphing",
        tier="Tier 2 SMIL",
        description_en="Native SVG <animate> path morphing between matching vertex coordinates",
        description_pt="Metamorfose nativa SVG com <animate> entre coordenadas de vértices compatíveis",
    ),
    "static": MotionSpec(
        key="static",
        name="Static",
        tier="Static Vector",
        description_en="Pure Euclidean geometry without animation, organized into clean Inkscape layers",
        description_pt="Geometria euclidiana pura sem animação, organizada em camadas limpas do Inkscape",
    ),
}

HANDOFF_TARGETS: Dict[str, HandoffSpec] = {
    "obs_browser_source": HandoffSpec(
        key="obs_browser_source",
        name="OBS Studio Browser Source",
        description_en="Self-contained animated vector visual running at 60fps in OBS Browser",
        description_pt="Visual vetorial animado autocontido rodando a 60fps no navegador do OBS",
    ),
    "inkscape_manual": HandoffSpec(
        key="inkscape_manual",
        name="Inkscape Manual Vector",
        description_en="Clean semantic layers and human-readable IDs optimized for manual vector editing",
        description_pt="Camadas semânticas limpas e IDs legíveis otimizados para edição manual no Inkscape",
    ),
    "web_dom": HandoffSpec(
        key="web_dom",
        name="Web DOM / HTML",
        description_en="Semantic inline SVG engineered for web components and responsive DOM styling",
        description_pt="SVG semântico inline projetado para componentes web e estilização no DOM",
    ),
    "powerbi_dax": HandoffSpec(
        key="powerbi_dax",
        name="Power BI DAX String",
        description_en="URL-encoded data:image/svg+xml;utf8 measure string for Power BI visuals",
        description_pt="String data:image/svg+xml;utf8 codificada para medidas DAX no Power BI",
    ),
}


# ---------------------------------------------------------------------------
# 2. HELPER FUNCTIONS: BUILD ASK_QUESTION PAYLOAD
# ---------------------------------------------------------------------------

def is_portuguese(language: str) -> bool:
    """Returns True if the language string denotes Portuguese."""
    lang = (language or "").strip().lower()
    return lang in ["pt", "pt-br", "pt_br", "portuguese", "português"]


def build_briefing_questions(
    language: str = "en",
    defaults: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Builds the interactive ask_question tool payload with recommended defaults.
    
    Conforms to Antigravity ask_question conventions:
    - Options phrased as direct user responses.
    - Recommended default placed first and prefixed with '(Recommended)' or '(Recomendado)'.
    - No forbidden 'Other' or 'Select all that apply' phrases.
    - is_multi_select set to False for each core dimension.
    """
    pt = is_portuguese(language)
    rec_prefix = "(Recomendado)" if pt else "(Recommended)"
    defaults = defaults or {}

    default_viewport = defaults.get("viewport", "webcam_16_9").lower()
    default_mode = defaults.get("mode", "experience").lower()
    default_motion = defaults.get("motion", "radar_pulse").lower()
    default_handoff = defaults.get("handoff", "obs_browser_source").lower()

    # 1. Viewport Question
    viewport_question_text = (
        "Qual é a superfície e proporção alvo para este ativo vetorial?"
        if pt
        else "What is the target surface viewport and aspect ratio for this vector asset?"
    )
    viewport_options = []
    # Order items: default first
    sorted_v_keys = [k for k in VIEWPORTS if k == default_viewport] + [k for k in VIEWPORTS if k != default_viewport]
    for idx, k in enumerate(sorted_v_keys):
        spec = VIEWPORTS[k]
        name = spec.name_pt if pt else spec.name_en
        desc = spec.description_pt if pt else spec.description_en
        prefix = f"{rec_prefix} " if idx == 0 else ""
        action_verb = "Usar" if pt else "Use"
        viewport_options.append(f"{prefix}{action_verb} {name} — {desc}")

    # 2. Surface Mode Question
    mode_question_text = (
        "Qual modo de superfície e densidade visual deve reger este design?"
        if pt
        else "Which surface mode and visual density should govern this design?"
    )
    mode_options = []
    sorted_m_keys = [k for k in SURFACE_MODES if k == default_mode] + [k for k in SURFACE_MODES if k != default_mode]
    for idx, k in enumerate(sorted_m_keys):
        spec = SURFACE_MODES[k]
        desc = spec.description_pt if pt else spec.description_en
        prefix = f"{rec_prefix} " if idx == 0 else ""
        mode_options.append(f"{prefix}{spec.name} — {desc}")

    # 3. Motion Profile Question
    motion_question_text = (
        "Qual perfil de animação vetorial deve ser implementado no SVG?"
        if pt
        else "What vector motion profile should be engineered into the SVG?"
    )
    motion_options = []
    sorted_mot_keys = [k for k in MOTION_PROFILES if k == default_motion] + [k for k in MOTION_PROFILES if k != default_motion]
    for idx, k in enumerate(sorted_mot_keys):
        spec = MOTION_PROFILES[k]
        desc = spec.description_pt if pt else spec.description_en
        prefix = f"{rec_prefix} " if idx == 0 else ""
        motion_options.append(f"{prefix}{spec.name} ({spec.tier}) — {desc}")

    # 4. Handoff Target Question
    handoff_question_text = (
        "Qual é o destino principal de entrega técnica deste arquivo?"
        if pt
        else "What is the primary technical handoff target for this vector asset?"
    )
    handoff_options = []
    sorted_h_keys = [k for k in HANDOFF_TARGETS if k == default_handoff] + [k for k in HANDOFF_TARGETS if k != default_handoff]
    for idx, k in enumerate(sorted_h_keys):
        spec = HANDOFF_TARGETS[k]
        desc = spec.description_pt if pt else spec.description_en
        prefix = f"{rec_prefix} " if idx == 0 else ""
        handoff_options.append(f"{prefix}{spec.name} — {desc}")

    return {
        "questions": [
            {
                "dimension": "viewport",
                "question": viewport_question_text,
                "options": viewport_options,
                "is_multi_select": False,
            },
            {
                "dimension": "mode",
                "question": mode_question_text,
                "options": mode_options,
                "is_multi_select": False,
            },
            {
                "dimension": "motion",
                "question": motion_question_text,
                "options": motion_options,
                "is_multi_select": False,
            },
            {
                "dimension": "handoff",
                "question": handoff_question_text,
                "options": handoff_options,
                "is_multi_select": False,
            },
        ]
    }


# ---------------------------------------------------------------------------
# 3. GENERATION OF STRUCTURED BRIEF.MD
# ---------------------------------------------------------------------------

def resolve_viewport(val: str) -> ViewportSpec:
    """Resolves string key or label to ViewportSpec."""
    val_norm = val.lower().strip()
    if val_norm in VIEWPORTS:
        return VIEWPORTS[val_norm]
    for v in VIEWPORTS.values():
        if str(v.width) in val_norm and str(v.height) in val_norm:
            return v
        if v.key in val_norm or v.name_en.lower() in val_norm:
            return v
    # Fallback default
    return VIEWPORTS["webcam_16_9"]


def resolve_mode(val: str) -> ModeSpec:
    """Resolves string key or label to ModeSpec."""
    val_norm = val.lower().strip()
    if val_norm in SURFACE_MODES:
        return SURFACE_MODES[val_norm]
    for m in SURFACE_MODES.values():
        if m.key in val_norm or m.name.lower() in val_norm:
            return m
    return SURFACE_MODES["experience"]


def resolve_motion(val: str) -> MotionSpec:
    """Resolves string key or label to MotionSpec."""
    val_norm = val.lower().strip()
    if val_norm in MOTION_PROFILES:
        return MOTION_PROFILES[val_norm]
    for mot in MOTION_PROFILES.values():
        if mot.key in val_norm or mot.name.lower() in val_norm:
            return mot
    if "radar" in val_norm or "spin" in val_norm or "pulse" in val_norm:
        return MOTION_PROFILES["radar_pulse"]
    if "line" in val_norm or "trace" in val_norm or "tracing" in val_norm:
        return MOTION_PROFILES["line_tracing"]
    if "morph" in val_norm or "smil" in val_norm:
        return MOTION_PROFILES["path_morphing"]
    if "static" in val_norm or "sem" in val_norm:
        return MOTION_PROFILES["static"]
    return MOTION_PROFILES["radar_pulse"]


def resolve_handoff(val: str) -> HandoffSpec:
    """Resolves string key or label to HandoffSpec."""
    val_norm = val.lower().strip()
    if val_norm in HANDOFF_TARGETS:
        return HANDOFF_TARGETS[val_norm]
    for h in HANDOFF_TARGETS.values():
        if h.key in val_norm or h.name.lower() in val_norm:
            return h
    if "obs" in val_norm:
        return HANDOFF_TARGETS["obs_browser_source"]
    if "inkscape" in val_norm:
        return HANDOFF_TARGETS["inkscape_manual"]
    if "web" in val_norm or "dom" in val_norm or "html" in val_norm:
        return HANDOFF_TARGETS["web_dom"]
    if "powerbi" in val_norm or "power bi" in val_norm or "dax" in val_norm:
        return HANDOFF_TARGETS["powerbi_dax"]
    return HANDOFF_TARGETS["obs_browser_source"]


def generate_brief_markdown(
    asset_name: str,
    viewport: str,
    mode: str,
    motion: str,
    handoff: str,
    language: str = "en",
    accent_color: str = "#00f0ff",
    secondary_accent: str = "#8a2be2",
    background_tone: str = "#0a0e17",
    design_notes: Optional[str] = None,
) -> str:
    """
    Generates a structured, binding BRIEF.md markdown document capturing all agreed constraints.
    """
    pt = is_portuguese(language)
    v_spec = resolve_viewport(viewport)
    m_spec = resolve_mode(mode)
    mot_spec = resolve_motion(motion)
    h_spec = resolve_handoff(handoff)

    title_header = (
        f"# Briefing de Design Vetorial: {asset_name}"
        if pt
        else f"# Vector Design Brief: {asset_name}"
    )

    core_dim_header = "## 1. Dimensões Canônicas da Superfície" if pt else "## 1. Core Dimensions"
    color_header = "## 2. Paleta de Cores & Iluminação Perceptual" if pt else "## 2. Color Palette & Lighting"
    geom_header = "## 3. Proporções Geométricas & Grid Modular" if pt else "## 3. Geometric Proportions & Grid"
    arch_header = "## 4. Restrições Arquiteturais & Craft Floor" if pt else "## 4. Architectural Constraints & Craft Floor"
    verif_header = "## 5. Checklist de Verificação & Validação" if pt else "## 5. Output Verification & Quality Checklist"

    viewport_name = v_spec.name_pt if pt else v_spec.name_en
    viewport_desc = v_spec.description_pt if pt else v_spec.description_en
    mode_desc = m_spec.description_pt if pt else m_spec.description_en
    mot_desc = mot_spec.description_pt if pt else mot_spec.description_en
    h_desc = h_spec.description_pt if pt else h_spec.description_en

    notes_section = ""
    if design_notes:
        notes_header = "## 6. Notas de Design Específicas" if pt else "## 6. Specific Design Notes"
        notes_section = f"\n{notes_header}\n{design_notes}\n"

    aspect_label = "Proporção" if pt else "Aspect Ratio"

    md = f"""{title_header}

{core_dim_header}
- **Surface Viewport**: {viewport_name} (`{v_spec.width}x{v_spec.height}`, `viewBox="{v_spec.viewbox}"`, {aspect_label}: `{v_spec.aspect_ratio}`)
  * Finalidade: {viewport_desc}
- **Surface Mode**: `{m_spec.name}` — {mode_desc}
- **Motion Profile**: `{mot_spec.name}` ({mot_spec.tier}) — {mot_desc}
- **Handoff Target**: `{h_spec.name}` — {h_desc}

{color_header}
- **Background Tone**: `{background_tone}` (Dark Slate / Midnight Base)
- **Primary Accent**: `{accent_color}` (Luminous Neon Cyan / Primary Accent)
- **Secondary Accent**: `{secondary_accent}` (High-contrast Violet / Amber Complement)
- **Contrast & Contrast Safety**: WCAG AAA for text readouts against dark surfaces.

{geom_header}
- **Canvas Width**: `{v_spec.width}px`
- **Canvas Height**: `{v_spec.height}px`
- **ViewBox**: `viewBox="{v_spec.viewbox}"`
- **Aspect Ratio**: `{v_spec.aspect_ratio}`
- **Focal Architecture**: Modular geometric subdivisions with Euclidean circular arcs and 8px alignment grid.

{arch_header}
- **Inkscape Namespaces**: Root `<svg>` must declare `xmlns="http://www.w3.org/2000/svg"`, `xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"`, `xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"`.
- **Semantic Layers**: Must strictly organize elements into Inkscape layer groups:
  * `<g inkscape:groupmode="layer" id="layer-background" inkscape:label="Background">`
  * `<g inkscape:groupmode="layer" id="layer-geometry" inkscape:label="Geometric Structure">`
  * `<g inkscape:groupmode="layer" id="layer-accents" inkscape:label="Accents & Lighting">`
  * `<g inkscape:groupmode="layer" id="layer-typography" inkscape:label="Typography & Labels">`
- **The Wrapper Pattern**: All motion keyframes and animations MUST target wrapper groups (`<g class="anim-wrapper-...">`) leaving inner geometric groups (`<g id="geom-...">`) pure and editable for Inkscape.
- **Universal Transform Contract**: Any CSS transform animation must include `transform-box: fill-box;` and `transform-origin: center;`.
- **Decoupled Typography**: Text elements must remain semantic `<text>` nodes in `layer-typography`. Never outline or bake text into vector paths.
- **Craft Floor Non-Negotiable Bans**:
  * **Banned: Generic AI clipart** (no cartoon gears, floating lightbulbs, or mascots).
  * **Banned: Muddy gradients** (no gray/brown dirty transition steps).
  * **Banned: Broken tangencies** or unaligned anchor points.

{verif_header}
- [ ] Validated with `scripts/validate_svg.py <file.svg> --json` (0 errors, 0 strict warnings).
- [ ] Layer hierarchy verified in Inkscape.
- [ ] Motion evaluated smoothly in handoff environment ({h_spec.name}).
{notes_section}"""
    return md


def create_brief_file(
    output_path: str,
    asset_name: str,
    viewport: str,
    mode: str,
    motion: str,
    handoff: str,
    language: str = "en",
    accent_color: str = "#00f0ff",
    secondary_accent: str = "#8a2be2",
    background_tone: str = "#0a0e17",
    design_notes: Optional[str] = None,
) -> str:
    """Generates and writes a BRIEF.md file to disk."""
    content = generate_brief_markdown(
        asset_name=asset_name,
        viewport=viewport,
        mode=mode,
        motion=motion,
        handoff=handoff,
        language=language,
        accent_color=accent_color,
        secondary_accent=secondary_accent,
        background_tone=background_tone,
        design_notes=design_notes,
    )
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    return output_path


# ---------------------------------------------------------------------------
# 4. PARSER AND VALIDATOR FOR BRIEF.MD
# ---------------------------------------------------------------------------

@dataclass
class BriefValidationResult:
    is_valid: bool
    errors: List[Dict[str, str]] = field(default_factory=list)
    warnings: List[Dict[str, str]] = field(default_factory=list)
    dimensions: Dict[str, Any] = field(default_factory=dict)
    file_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "errors_count": len(self.errors),
            "warnings_count": len(self.warnings),
            "dimensions": self.dimensions,
            "file_path": self.file_path,
        }


def parse_brief_content(content: str) -> Dict[str, Any]:
    """
    Parses a BRIEF.md text and extracts the 4 core dimensions and metadata.
    Supports bullet formats, table formats, and frontmatter.
    """
    parsed: Dict[str, Any] = {}

    # Extract Title / Asset Name
    title_match = re.search(r"^#\s+(?:Vector Design Brief|Briefing de Design Vetorial):\s*(.+)$", content, re.MULTILINE | re.IGNORECASE)
    if title_match:
        parsed["asset_name"] = title_match.group(1).strip()
    else:
        first_h1 = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if first_h1:
            parsed["asset_name"] = first_h1.group(1).strip()

    # 1. Surface Viewport Extraction
    vp_match = re.search(
        r"^[ \t]*[-*]?[ \t]*\*{0,2}(?:Surface Viewport|Superfície e Viewport)\*{0,2}[ \t]*[:=][ \t]*([^\r\n]+)",
        content,
        re.MULTILINE | re.IGNORECASE,
    )
    if not vp_match:
        vp_match = re.search(r"^viewport[ \t]*[:=][ \t]*([^\r\n]+)", content, re.MULTILINE | re.IGNORECASE)

    if vp_match:
        vp_raw = vp_match.group(1).strip()
        parsed["viewport_raw"] = vp_raw
        
        # Dimensions width x height
        dim_match = re.search(r"(\d{2,5})\s*[x×]\s*(\d{2,5})", vp_raw)
        if not dim_match:
            dim_match = re.search(r'viewBox="0 0 (\d{2,5}) (\d{2,5})"', content, re.IGNORECASE)
        if not dim_match:
            dim_match = re.search(r"(\d{2,5})\s*[x×]\s*(\d{2,5})", content)

        if dim_match:
            parsed["viewport_width"] = int(dim_match.group(1))
            parsed["viewport_height"] = int(dim_match.group(2))
            parsed["viewbox"] = f"0 0 {parsed['viewport_width']} {parsed['viewport_height']}"

    # 2. Surface Mode Extraction
    mode_match = re.search(
        r"^[ \t]*[-*]?[ \t]*\*{0,2}(?:Surface Mode|Modo de Superfície)\*{0,2}[ \t]*[:=][ \t]*([^\r\n]+)",
        content,
        re.MULTILINE | re.IGNORECASE,
    )
    if not mode_match:
        mode_match = re.search(r"^mode[ \t]*[:=][ \t]*([^\r\n]+)", content, re.MULTILINE | re.IGNORECASE)

    if mode_match:
        mode_raw = mode_match.group(1).strip().strip("`* ")
        parsed["mode_raw"] = mode_raw
        for m_key, m_spec in SURFACE_MODES.items():
            if re.search(rf"\b{re.escape(m_spec.name)}\b", mode_raw, re.IGNORECASE):
                parsed["mode"] = m_spec.name
                break

    # 3. Motion Profile Extraction
    mot_match = re.search(
        r"^[ \t]*[-*]?[ \t]*\*{0,2}(?:Motion Profile|Perfil de Movimento)\*{0,2}[ \t]*[:=][ \t]*([^\r\n]+)",
        content,
        re.MULTILINE | re.IGNORECASE,
    )
    if not mot_match:
        mot_match = re.search(r"^motion[ \t]*[:=][ \t]*([^\r\n]+)", content, re.MULTILINE | re.IGNORECASE)

    if mot_match:
        mot_raw = mot_match.group(1).strip().strip("`* ")
        parsed["motion_raw"] = mot_raw
        for mot_key, mot_spec in MOTION_PROFILES.items():
            if mot_spec.name.lower() in mot_raw.lower() or mot_spec.key in mot_raw.lower():
                parsed["motion"] = mot_spec.name
                break
        if "motion" not in parsed:
            if "radar" in mot_raw.lower() or "pulse" in mot_raw.lower() or "spin" in mot_raw.lower():
                parsed["motion"] = MOTION_PROFILES["radar_pulse"].name
            elif "line" in mot_raw.lower() or "tracing" in mot_raw.lower():
                parsed["motion"] = MOTION_PROFILES["line_tracing"].name
            elif "morph" in mot_raw.lower() or "smil" in mot_raw.lower():
                parsed["motion"] = MOTION_PROFILES["path_morphing"].name
            elif "static" in mot_raw.lower() or "sem animação" in mot_raw.lower():
                parsed["motion"] = MOTION_PROFILES["static"].name

    # 4. Handoff Target Extraction
    h_match = re.search(
        r"^[ \t]*[-*]?[ \t]*\*{0,2}(?:Handoff Target|Destino de Entrega)\*{0,2}[ \t]*[:=][ \t]*([^\r\n]+)",
        content,
        re.MULTILINE | re.IGNORECASE,
    )
    if not h_match:
        h_match = re.search(r"^handoff[ \t]*[:=][ \t]*([^\r\n]+)", content, re.MULTILINE | re.IGNORECASE)

    if h_match:
        h_raw = h_match.group(1).strip().strip("`* ")
        parsed["handoff_raw"] = h_raw
        for h_key, h_spec in HANDOFF_TARGETS.items():
            if h_spec.name.lower() in h_raw.lower():
                parsed["handoff"] = h_spec.name
                break
        if "handoff" not in parsed:
            if "obs" in h_raw.lower():
                parsed["handoff"] = HANDOFF_TARGETS["obs_browser_source"].name
            elif "inkscape" in h_raw.lower():
                parsed["handoff"] = HANDOFF_TARGETS["inkscape_manual"].name
            elif "web" in h_raw.lower() or "dom" in h_raw.lower() or "html" in h_raw.lower():
                parsed["handoff"] = HANDOFF_TARGETS["web_dom"].name
            elif "power bi" in h_raw.lower() or "powerbi" in h_raw.lower() or "dax" in h_raw.lower():
                parsed["handoff"] = HANDOFF_TARGETS["powerbi_dax"].name

    return parsed


def validate_brief_content(content: str, file_path: Optional[str] = None) -> BriefValidationResult:
    """
    Validates that a BRIEF.md text contains all 4 binding dimensions with acceptable values.
    """
    errors: List[Dict[str, str]] = []
    warnings: List[Dict[str, str]] = []

    parsed = parse_brief_content(content)

    # 1. Surface Viewport validation
    if "viewport_raw" not in parsed:
        errors.append({
            "code": "MISSING_SURFACE_VIEWPORT",
            "message": "BRIEF.md is missing the required 'Surface Viewport' specification.",
        })
    elif "viewport_width" not in parsed or "viewport_height" not in parsed:
        errors.append({
            "code": "INVALID_VIEWPORT_DIMENSIONS",
            "message": "Could not determine valid width and height dimensions from 'Surface Viewport'.",
        })
    elif parsed["viewport_width"] <= 0 or parsed["viewport_height"] <= 0:
        errors.append({
            "code": "INVALID_VIEWPORT_DIMENSIONS",
            "message": f"Viewport dimensions must be positive integers, got {parsed.get('viewport_width')}x{parsed.get('viewport_height')}.",
        })

    # 2. Surface Mode validation
    if "mode_raw" not in parsed:
        errors.append({
            "code": "MISSING_SURFACE_MODE",
            "message": "BRIEF.md is missing the required 'Surface Mode' specification.",
        })
    elif "mode" not in parsed:
        valid_modes = [m.name for m in SURFACE_MODES.values()]
        errors.append({
            "code": "INVALID_SURFACE_MODE",
            "message": f"Unrecognized Surface Mode '{parsed.get('mode_raw')}'. Expected one of: {', '.join(valid_modes)}.",
        })

    # 3. Motion Profile validation
    if "motion_raw" not in parsed:
        errors.append({
            "code": "MISSING_MOTION_PROFILE",
            "message": "BRIEF.md is missing the required 'Motion Profile' specification.",
        })
    elif "motion" not in parsed:
        valid_motions = [m.name for m in MOTION_PROFILES.values()]
        errors.append({
            "code": "INVALID_MOTION_PROFILE",
            "message": f"Unrecognized Motion Profile '{parsed.get('motion_raw')}'. Expected one of: {', '.join(valid_motions)}.",
        })

    # 4. Handoff Target validation
    if "handoff_raw" not in parsed:
        errors.append({
            "code": "MISSING_HANDOFF_TARGET",
            "message": "BRIEF.md is missing the required 'Handoff Target' specification.",
        })
    elif "handoff" not in parsed:
        valid_handoffs = [h.name for h in HANDOFF_TARGETS.values()]
        errors.append({
            "code": "INVALID_HANDOFF_TARGET",
            "message": f"Unrecognized Handoff Target '{parsed.get('handoff_raw')}'. Expected one of: {', '.join(valid_handoffs)}.",
        })

    is_valid = len(errors) == 0
    return BriefValidationResult(
        is_valid=is_valid,
        errors=errors,
        warnings=warnings,
        dimensions=parsed,
        file_path=file_path,
    )


def validate_brief_file(file_path: str) -> BriefValidationResult:
    """Reads and validates a BRIEF.md file from disk."""
    if not os.path.exists(file_path):
        return BriefValidationResult(
            is_valid=False,
            errors=[{
                "code": "FILE_NOT_FOUND",
                "message": f"Briefing file does not exist: {file_path}",
            }],
            file_path=file_path,
        )
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return BriefValidationResult(
            is_valid=False,
            errors=[{
                "code": "FILE_READ_ERROR",
                "message": f"Failed to read file: {e}",
            }],
            file_path=file_path,
        )
    return validate_brief_content(content, file_path=file_path)


# ---------------------------------------------------------------------------
# 5. CLI INTERFACE
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="briefing.py",
        description="SVG Maestro Interactive Briefing Protocol & BRIEF.md Manager",
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Subcommand: questions
    q_parser = subparsers.add_parser("questions", help="Generate ask_question tool payload")
    q_parser.add_argument("--lang", default="en", help="Language code ('en' or 'pt')")
    q_parser.add_argument("--viewport", help="Default viewport key")
    q_parser.add_argument("--mode", help="Default mode key")
    q_parser.add_argument("--motion", help="Default motion profile key")
    q_parser.add_argument("--handoff", help="Default handoff target key")
    q_parser.add_argument("--json", action="store_true", help="Output pure JSON")

    # Subcommand: create
    c_parser = subparsers.add_parser("create", help="Generate a binding BRIEF.md document")
    c_parser.add_argument("--name", default="Vector Asset", help="Asset / Project name")
    c_parser.add_argument("--viewport", default="webcam_16_9", help="Viewport key or dimensions")
    c_parser.add_argument("--mode", default="experience", help="Surface mode (Operate, Experience, Persuade)")
    c_parser.add_argument("--motion", default="radar_pulse", help="Motion profile key or name")
    c_parser.add_argument("--handoff", default="obs_browser_source", help="Handoff target key or name")
    c_parser.add_argument("--output", default="BRIEF.md", help="Output file path")
    c_parser.add_argument("--lang", default="en", help="Language code ('en' or 'pt')")
    c_parser.add_argument("--accent", default="#00f0ff", help="Primary accent color")
    c_parser.add_argument("--secondary", default="#8a2be2", help="Secondary accent color")
    c_parser.add_argument("--background", default="#0a0e17", help="Background tone")

    # Subcommand: validate
    v_parser = subparsers.add_parser("validate", help="Validate a BRIEF.md document")
    v_parser.add_argument("file", help="Path to BRIEF.md file")
    v_parser.add_argument("--json", action="store_true", help="Output JSON diagnostic report")

    # Subcommand: template
    t_parser = subparsers.add_parser("template", help="Output standard reference BRIEF.md template")
    t_parser.add_argument("--output", help="Optional path to write template")

    args = parser.parse_args()

    if args.command == "questions":
        defaults = {}
        if args.viewport:
            defaults["viewport"] = args.viewport
        if args.mode:
            defaults["mode"] = args.mode
        if args.motion:
            defaults["motion"] = args.motion
        if args.handoff:
            defaults["handoff"] = args.handoff
        payload = build_briefing_questions(language=args.lang, defaults=defaults)
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(f"=== SVG Maestro Briefing Questions ({args.lang.upper()}) ===")
            for q in payload["questions"]:
                print(f"\n[Dimension: {q['dimension']}] {q['question']}")
                for opt in q["options"]:
                    print(f"  * {opt}")

    elif args.command == "create":
        create_brief_file(
            output_path=args.output,
            asset_name=args.name,
            viewport=args.viewport,
            mode=args.mode,
            motion=args.motion,
            handoff=args.handoff,
            language=args.lang,
            accent_color=args.accent,
            secondary_accent=args.secondary,
            background_tone=args.background,
        )
        print(f"[OK] Generated binding brief: {args.output}")

    elif args.command == "validate":
        res = validate_brief_file(args.file)
        if args.json:
            print(json.dumps(res.to_dict(), indent=2, ensure_ascii=False))
        else:
            if res.is_valid:
                print(f"[PASS] VALID BRIEF: {args.file}")
                print(f"  * Asset: {res.dimensions.get('asset_name', 'Unnamed')}")
                print(f"  * Viewport: {res.dimensions.get('viewport_width')}x{res.dimensions.get('viewport_height')}")
                print(f"  * Mode: {res.dimensions.get('mode')}")
                print(f"  * Motion: {res.dimensions.get('motion')}")
                print(f"  * Handoff: {res.dimensions.get('handoff')}")
            else:
                print(f"[FAIL] INVALID BRIEF: {args.file}")
                for err in res.errors:
                    print(f"  [X] [{err['code']}] {err['message']}")
        sys.exit(0 if res.is_valid else 1)

    elif args.command == "template":
        sample = generate_brief_markdown(
            asset_name="{ASSET_NAME}",
            viewport="webcam_16_9",
            mode="experience",
            motion="radar_pulse",
            handoff="obs_browser_source",
            language="en",
        )
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(sample)
            print(f"[OK] Template written to {args.output}")
        else:
            print(sample)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
