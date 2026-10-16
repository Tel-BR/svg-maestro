# SVG Maestro 🎨✨

🌐 **English** | [Português (Brasil)](README.pt-BR.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](scripts/validate_svg.py)
[![Inkscape: Fully Compatible](https://img.shields.io/badge/Inkscape-Compatible-brightgreen.svg)](docs/SPEC.md)

**SVG Maestro** is an open-source vector design and motion orchestration system for AI coding agents (Antigravity, Claude, Codex). It fuses **Matt Pocock's architectural discipline** (stateful elicitation, vertical slicing, mechanical validation loops) with **Impeccable's radical art direction** (surface modes, creative refinement verbs, Craft Floor quality standards) to generate high-end, mathematical SVG layouts, dashboard data-viz cards, and OBS Studio streaming overlays that are 100% editable in Inkscape.

---

## 🏛️ The Three Foundational Pillars

### 1. Aesthetic Direction & Mathematical Geometry (Dual-Engine)
- **Zero-Bias Policy**: Never copies boilerplate clipart. All artwork is generated bespoke using Fibonacci sequences, the Golden Ratio ($\phi \approx 1.618$), $30^\circ$ isometric grids, and Euclidean curvature.
- **Surface Modes**:
  - `Operate`: High data density and scanability for web dashboards and Power BI cards.
  - `Experience`: Vibrant neon glow, high contrast, and 60fps ambient motion loops for OBS Studio streaming overlays.
  - `Persuade`: Monumental Euclidean scale and harmonic proportions for hero illustrations and brand art.
- **Craft Floor**: Non-negotiable quality floor strictly banning generic "AI clipart", muddy gradients, and unanchored bezier paths.
- **Zero External Dependencies**: Operates 100% autonomously out of the box. Optionally bridges to `DESIGN.md` or `PRODUCT.md` tokens if the project already uses `impeccable`.

### 2. Total Inkscape Compatibility
- Full namespace compliance (`xmlns:inkscape`, `xmlns:sodipodi`).
- Native semantic Inkscape layers (`inkscape:groupmode="layer"` and `inkscape:label`).
- Clean `<defs>` hygiene with descriptive, human-readable IDs.

### 3. Native Animation & Mutation-Proofing (Wrapper Pattern)
- **Wrapper Pattern**: Encapsulates animated nodes inside dedicated wrappers (`<g class="anim-wrapper-...">`) protecting static geometry groups (`<g inkscape:label="...">`) from transform collisions during manual Inkscape edits.
- **Tier 1 (Universal CSS)**: Embedded `@keyframes` strictly enforcing `transform-box: fill-box` and `transform-origin: center` for rock-solid cross-browser and OBS rendering.
- **Tier 2 (SMIL Vector Motion)**: Native path morphing and guide motion.
- **Vector Filter FX**: Hardware-accelerated SVG filters (`feTurbulence`, `feDisplacementMap`, `feDropShadow`) for cyber/neon/liquid effects.

---

## 🌐 Internationalization (i18n)

- **Polyglot Agent**: The agent conducts interactive briefings and critiques in the user's conversational language, while generating standard English XML tokens for universal team interoperability.
- **Decoupled Typography**: Text is never outlined to vector paths. All labels remain editable `<text>` elements in a dedicated `layer-typography` layer, supporting native browser multilingual `<switch>` selection.

---

## ⚡ Creative Refinement Verbs

Iterate on generated vectors using expressive creative verbs:
- `/svg-maestro brief`: Triggers the interactive elicitation interview via `ask_question` across 4 core dimensions (Surface Viewport, Surface Mode, Motion Profile, Handoff Target), generating a binding `BRIEF.md`.
- `/svg-maestro bolder`: Intensifies stroke weights, gradient saturation, and neon contrast.
- `/svg-maestro quieter`: Softens luminescence, reduces saturation, and refines lines for an understated look.
- `/svg-maestro distill`: Strips secondary clutter, keeping only essential geometric lines and data readouts.
- `/svg-maestro delight`: Adds micro-motion touches (orbital radar sweeps, edge glows, pulsing rings).
- `/svg-maestro animate`: Converts static Inkscape SVGs into motion-enabled assets using the Wrapper Pattern.
- `/svg-maestro critique`: Two-axis review evaluating Technical Standards (Inkscape/linter) and Aesthetic Craft.

### 📋 Interactive Briefing Engine (`scripts/briefing.py`)

Generate `ask_question` elicitation prompts and validate binding design contracts:

```bash
# Generate localized elicitation payload for ask_question
python scripts/briefing.py questions --lang en --json

# Synthesize binding design brief
python scripts/briefing.py create \
  --name "Stream Frame" \
  --viewport "webcam_16_9" \
  --mode "experience" \
  --motion "radar_pulse" \
  --handoff "obs_browser_source" \
  --output BRIEF.md

# Validate brief completeness before SVG code generation
python scripts/briefing.py validate BRIEF.md --json
```

### 🎥 OBS Streaming Overlays Pipeline (`scripts/obs_pipeline.py`)

Generate production-ready, transparent-viewport OBS streaming overlays in `Experience` mode:

```bash
# Generate complete overlay kit (16:9 webcam frame + alert banner)
python scripts/obs_pipeline.py generate-all --output-dir examples/obs/ --theme cyan_magenta

# Generate customized webcam frame
python scripts/obs_pipeline.py webcam \
  --output examples/obs/webcam_frame_16_9.svg \
  --theme cyan_magenta \
  --cam-label "CAM 01 // LIVE FEED" \
  --status-label "REC ● 1080P 60FPS"

# Generate customized alert notification banner
python scripts/obs_pipeline.py alert \
  --output examples/obs/alert_banner.svg \
  --theme cyan_magenta \
  --type "NEW SUBSCRIBER" \
  --user "CYBER_PHANTOM" \
  --detail "TIER 3 // 12 MONTH STREAK"
```

Available visual themes: `cyan_magenta`, `amber_gold`, `matrix_green`, and `crimson_hazard`.

### 📊 Dashboard Widgets & Power BI DAX Pipeline (`scripts/dashboard_pipeline.py`)

Generate modular, data-dense metric cards in `Operate` mode adhering to golden ratio proportions ($\phi \approx 1.618$), featuring glowing radar sweep indicators, sparklines, decoupled typography, and instant URL-encoded DAX measure snippets for Power BI visuals:

```bash
# Generate complete dashboard kit (SVG card + Power BI DAX measure)
python scripts/dashboard_pipeline.py generate-all --output-dir examples/dashboard/ --theme dark_slate

# Generate customized standalone telemetry card SVG
python scripts/dashboard_pipeline.py card \
  --output examples/dashboard/telemetry_card.svg \
  --theme dark_slate \
  --kpi-value "$1,284,500" \
  --kpi-change "+14.2% ↑" \
  --kpi-label "TOTAL SYSTEM THROUGHPUT"

# Convert any SVG into a Power BI Image Visual DAX measure
python scripts/dashboard_pipeline.py dax \
  --input examples/dashboard/telemetry_card.svg \
  --output examples/dashboard/telemetry_card.dax \
  --measure-name TelemetryCard
```

Available visual themes: `dark_slate`, `obsidian_amber`, `matrix_emerald`, and `deep_violet`.

### 🎨 Art Direction Refinement Verbs (`scripts/refinement_verbs.py`)

Iteratively sculpt and refine generated vector graphics using expressive creative direction commands rather than micromanaging coordinates:

- **`bolder`**: Amplifies stroke weights (1.4x-1.8x), enhances gradient contrasts, and intensifies luminescent glow filters.
- **`quieter`**: Desaturates colors, softens lighting/glows, and reduces stroke weights (0.6x-0.75x) for an understated, elegant look.
- **`distill`**: Strips secondary decorative shapes (micro grid tics, secondary accent embellishments, decorative noise) while preserving core Euclidean hierarchy and metrics.
- **`delight`**: Injects subtle micro-motion accents (orbital radar rings or breathing pulses), strictly encapsulated using the Wrapper Pattern with `transform-box: fill-box; transform-origin: center;`.
- **`animate`**: Converts a static SVG into a motion asset by identifying central geometry or accents, wrapping target elements in `<g class="anim-wrapper-...">` and injecting CSS `@keyframes` with `transform-box: fill-box; transform-origin: center;`.
- **`critique`**: Emits a structured two-axis review scoring (1) Technical Standards (linter compliance, Inkscape layers, defs hygiene, Wrapper Pattern) and (2) Aesthetic Craft (proportions, color harmony, typography decoupling, Craft Floor bans).

```bash
# Refine an existing SVG asset
python scripts/refinement_verbs.py bolder --input card.svg --output card_bolder.svg
python scripts/refinement_verbs.py quieter --input card.svg
python scripts/refinement_verbs.py distill --input widget.svg -o widget_distilled.svg
python scripts/refinement_verbs.py delight --input overlay.svg
python scripts/refinement_verbs.py animate --input static_card.svg

# Run Two-Axis Design Critique
python scripts/refinement_verbs.py critique --input card.svg
python scripts/refinement_verbs.py critique --input card.svg --json
```

### 🌐 Multilingual Typography & Internationalization (`<switch>`)

SVG Maestro enforces strict typography decoupling, preventing destructive text-to-path conversion and enabling native, browser-evaluated multilingual graphics via SVG `<switch>` and `systemLanguage`:

- **Decoupled Typography**: Text elements reside strictly as semantic `<text>` tags in `layer-typography`, remaining 100% editable inside Inkscape's text tool. Converted vector paths in typography layers are flagged with `OUTLINED_TEXT_WARNING`.
- **Sequential `<switch>` Contract**: Specific language alternatives (e.g. `systemLanguage="pt"`, `systemLanguage="es"`) are authored first, followed by an unconditioned default fallback element (English) as the final child.
- **Reference Asset**: See `examples/i18n/multilingual_card.svg` for a production-grade telemetry card demonstrating automated locale switching across Portuguese, Spanish, and fallback English.

---

## 🚀 Autonomous Closed-Loop Validation

SVG Maestro includes a zero-dependency validation engine (`validate_svg.py`) based exclusively on the Python standard library:

```bash
python scripts/validate_svg.py path/to/vector.svg
```

For programmatic agent consumption:

```bash
python scripts/validate_svg.py path/to/vector.svg --json
```

---

## ❓ Do I need the Impeccable skill installed?

**No! SVG Maestro is completely self-contained.**

- **Autonomous Mode (Default):** Generates all mathematical proportions, Euclidean geometries, and harmonious WCAG AAA color palettes natively from first principles.
- **Integrated Mode (Optional):** If your workspace already contains `DESIGN.md` or `PRODUCT.md`, SVG Maestro automatically inherits those tokens to match your app's existing visual identity.

---

## 📦 Installation & Agent Usage

### Antigravity (Google)
```bash
git clone https://github.com/Tel-BR/svg-maestro.git ~/.gemini/config/skills/svg-maestro
```

### Claude Code (Anthropic)
```bash
git clone https://github.com/Tel-BR/svg-maestro.git ~/.claude/skills/svg-maestro
```

### Codex, Cursor, or Custom Agents
Reference [`SKILL.md`](SKILL.md) directly in your agent's system prompt or workspace skills.

---

## 📂 Repository Layout

```
svg-maestro/
├── CONTEXT.md                  # Formal domain glossary
├── SKILL.md                    # Agent skill specification
├── README.md                   # Canonical English documentation
├── README.pt-BR.md             # Localized Portuguese documentation
├── CONTRIBUTING.md             # Community contribution guide
├── LICENSE                     # Permissive MIT License
├── scripts/
│   ├── briefing.py             # Interactive briefing and elicitation engine
│   ├── dashboard_pipeline.py   # Dashboard telemetry cards & Power BI DAX pipeline
│   ├── obs_pipeline.py         # OBS streaming overlays generator & pipeline
│   ├── refinement_verbs.py     # Creative refinement verbs & design critique engine
│   └── validate_svg.py         # Zero-dependency Python validation linter
├── examples/
│   ├── dashboard/              # Production-ready metric cards & DAX snippet
│   │   ├── telemetry_card.svg
│   │   └── telemetry_card.dax
│   ├── i18n/                   # Multilingual vector assets (<switch> + systemLanguage)
│   │   └── multilingual_card.svg
│   └── obs/                    # Production-ready streaming overlays
│       ├── webcam_frame_16_9.svg
│       └── alert_banner.svg
├── templates/
│   └── BRIEF.template.md       # Canonical briefing template
├── docs/
│   ├── SPEC.md                 # System specification
│   ├── tickets/                # Executable tracer-bullet tickets
│   │   ├── 01-core-linter-test-suite.md
│   │   ├── 02-interactive-briefing-module.md
│   │   ├── 03-obs-streaming-overlays-pipeline.md
│   │   ├── 04-dashboard-widgets-and-powerbi-dax-pipeline.md
│   │   ├── 05-art-direction-refinement-verbs.md
│   │   └── 06-multilingual-typography-and-i18n.md
│   └── adr/                    # Architectural Decision Records (ADRs 0001 - 0008)
└── tests/
    ├── fixtures/               # Comprehensive validation test fixtures
    ├── test_briefing.py        # Briefing engine test suite
    ├── test_dashboard_pipeline.py # Dashboard & DAX pipeline test suite
    ├── test_i18n.py            # Multilingual typography & <switch> test suite
    ├── test_linter.py          # Core linter test suite
    ├── test_obs_overlays.py    # OBS overlays test suite
    ├── test_refinement_verbs.py # Refinement verbs & critique test suite
    └── test_card.svg           # Canonical test fixture
```

---

## 🙏 Credits & Acknowledgments

**SVG Maestro** stands on the shoulders of giants:
- Inspired by **Matt Pocock's** agentic workflow ecosystem (`grilling`, `domain-modeling`, `to-spec`, `to-tickets`, `tdd`).
- Inspired by the **Impeccable** design skill for its radical philosophy of out-of-distribution craft, surface modes, and creative refinement verbs.

---

## 📜 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details. Free for personal, academic, and commercial use.
