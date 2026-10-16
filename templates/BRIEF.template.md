# Vector Design Brief: {ASSET_NAME}

## 1. Core Dimensions
- **Surface Viewport**: 16:9 Webcam Overlay (1920x1080) (`1920x1080`, `viewBox="0 0 1920 1080"`, Aspect Ratio: `16:9`)
  * Finalidade: OBS Studio stream frame with transparent center and corner brackets
- **Surface Mode**: `Experience` — Vibrant cyber neon illumination, high contrast, and ambient motion for OBS/streaming
- **Motion Profile**: `Ambient Radar Spin / Breathing Pulse` (Tier 1 CSS) — Subtle continuous rotation or breathing scale with transform-box: fill-box
- **Handoff Target**: `OBS Studio Browser Source` — Self-contained animated vector visual running at 60fps in OBS Browser

## 2. Color Palette & Lighting
- **Background Tone**: `#0a0e17` (Dark Slate / Midnight Base)
- **Primary Accent**: `#00f0ff` (Luminous Neon Cyan / Primary Accent)
- **Secondary Accent**: `#8a2be2` (High-contrast Violet / Amber Complement)
- **Contrast & Contrast Safety**: WCAG AAA for text readouts against dark surfaces.

## 3. Geometric Proportions & Grid
- **Canvas Width**: `1920px`
- **Canvas Height**: `1080px`
- **ViewBox**: `viewBox="0 0 1920 1080"`
- **Aspect Ratio**: `16:9`
- **Focal Architecture**: Modular geometric subdivisions with Euclidean circular arcs and 8px alignment grid.

## 4. Architectural Constraints & Craft Floor
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
  * 🚫 Banned: Generic AI clipart (no cartoon gears, floating lightbulbs, or mascots).
  * 🚫 Banned: Muddy gradients (no gray/brown dirty transition steps).
  * 🚫 Banned: Broken tangencies or unaligned anchor points.

## 5. Output Verification & Quality Checklist
- [ ] Validated with `scripts/validate_svg.py <file.svg> --json` (0 errors, 0 strict warnings).
- [ ] Layer hierarchy verified in Inkscape.
- [ ] Motion evaluated at 60fps in handoff environment (OBS Studio Browser Source).
