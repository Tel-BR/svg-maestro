# SVG Maestro

**English** | [Português (Brasil)](README.pt-BR.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](.github/workflows/ci.yml)
[![Inkscape: Layer Compatible](https://img.shields.io/badge/Inkscape-Layer%20Compatible-brightgreen.svg)](docs/SPEC.md)
[![Status: Beta v0.1.0-beta.1](https://img.shields.io/badge/status-v0.1.0--beta.1-orange.svg)](https://github.com/Tel-BR/svg-maestro/releases)

**SVG Maestro** is a vector design and motion orchestration system for AI coding agents (Antigravity, Claude Code, Codex, Cursor). It combines architectural discipline (structured briefing, vertical ticket slicing, autonomous validation) with expressive art direction (surface modes, non-destructive refinement verbs, decoupled typography) to produce mathematical SVG layouts, telemetry dashboard cards, and OBS streaming overlays structured for Inkscape.

---

## Quickstart

Generate, validate, and refine a production-ready telemetry card in three commands:

```bash
# 1. Generate a telemetry card in Operate mode
python scripts/dashboard_pipeline.py card \
  --output card.svg \
  --theme dark_slate \
  --kpi-value "$1,284,500" \
  --kpi-label "SYSTEM THROUGHPUT"

# 2. Validate structural integrity and Inkscape compliance
python scripts/validate_svg.py card.svg

# 3. Apply non-destructive creative refinement (writes to card_bolder.svg)
python scripts/refinement_verbs.py bolder --input card.svg
```

---

## Installation & Agent Setup

### Antigravity (Google)
```bash
git clone https://github.com/Tel-BR/svg-maestro.git ~/.gemini/config/skills/svg-maestro
```

### Claude Code (Anthropic)
```bash
git clone https://github.com/Tel-BR/svg-maestro.git ~/.claude/skills/svg-maestro
```

### Codex, Cursor, or Custom Agents
Reference [`SKILL.md`](SKILL.md) directly in your agent's system prompt or workspace instruction set.

---

## Status & Known Limitations

> [!NOTE]
> SVG Maestro is currently in **Beta (`v0.1.0-beta.1`)**. Core contracts and validation rules are active, but CLI flags and heuristic thresholds are subject to refinement based on community feedback.

- **Contrast Evaluation**: The palette critique checks for tonal separation between dark chassis tones and luminous accents using perceptual HLS thresholds. It does not compute per-character Euclidean relative luminance contrast ($L_1 / L_2 \ge 7:1$). High-contrast themes are provided as starting baselines.
- **Power BI DAX Output**: The DAX generator formats SVG markup into a standard Data URI (`data:image/svg+xml;utf8,...`) with `#` hex codes escaped as `%23` and double quotes escaped as `""`. It is not a full RFC 3986 URL encoder. Verify rendering in your target Power BI Desktop visual.
- **Inkscape Namespaces**: Layer hierarchies (`inkscape:groupmode="layer"`) and `<defs>` IDs are tuned specifically for Inkscape. Other vector applications (Illustrator, Figma) import these as regular `<g>` groups without native layer metadata.
- **Animation Portability**: Embedded CSS animations strictly declare `transform-box: fill-box` and `transform-origin: center` for browser and OBS Studio rendering. Raster image viewers or basic markdown renderers that disable CSS will display the SVG statically in its default state.

---

## Core Capabilities

### 1. Mathematical Geometry & Surface Modes
All vectors are constructed from geometric principles (Fibonacci sequences, Golden Ratio $\phi \approx 1.618$, isometric projections) without external clipart:
- **`Operate`**: High data density and crisp readability for web telemetry and Power BI cards.
- **`Experience`**: High contrast and ambient CSS keyframe loops for OBS Studio streaming overlays.
- **`Persuade`**: Monumental Euclidean proportions for branding and hero graphics.

### 2. Inkscape Compatibility & The Wrapper Pattern
- **Semantic Layers**: Every major element group belongs to an Inkscape layer (`Background`, `Geometric Structure`, `Accents & Lighting`, `Typography & Labels`).
- **Clean `<defs>` Hygiene**: Meaningful IDs (`id="grad-neon-cyan"`, `id="filter-cyber-glow"`) instead of arbitrary auto-generated hashes.
- **Wrapper Pattern**: Motion keyframes target dedicated `<g class="anim-wrapper-...">` elements, shielding static geometric shapes from transform attribute collisions during manual Inkscape editing.

### 3. Non-Destructive Refinement Verbs (`scripts/refinement_verbs.py`)
Iteratively steer existing vector graphics through expressive commands without manual coordinate manipulation:
- **`bolder`**: Amplifies stroke weights (1.4x-1.8x), enhances gradient contrasts, and intensifies glow filters.
- **`quieter`**: Desaturates colors, softens lighting/glows, and reduces stroke weights (0.6x-0.75x).
- **`distill`**: Strips secondary decorative shapes while preserving core Euclidean hierarchy and metrics.
- **`delight`**: Injects micro-motion accents (orbital radar rings or breathing pulses) encapsulated in Wrapper groups.
- **`animate`**: Converts static SVGs into motion assets by wrapping key elements in animation groups and injecting CSS `@keyframes`.
- **`critique`**: Emits a structured two-axis report scoring Technical Standards (linter compliance, layers, defs hygiene) and Aesthetic Craft (proportions, color harmony, typography decoupling).

```bash
# Non-destructive by default: creates card_bolder.svg
python scripts/refinement_verbs.py bolder --input card.svg

# Specify a custom output file
python scripts/refinement_verbs.py quieter --input card.svg --output card_minimal.svg

# Explicit in-place modification
python scripts/refinement_verbs.py distill --input card.svg --in-place

# Run two-axis critique
python scripts/refinement_verbs.py critique --input card.svg
python scripts/refinement_verbs.py critique --input card.svg --json
```

### 4. Interactive Briefing Engine (`scripts/briefing.py`)
Provides structured elicitation across 4 core vector dimensions (Surface Viewport, Mode, Motion Profile, Handoff Target) and synthesizes constraints into a binding `BRIEF.md`:

```bash
# Generate localized elicitation payload
python scripts/briefing.py questions --lang en --json

# Synthesize binding design brief
python scripts/briefing.py create \
  --name "Stream Frame" \
  --viewport "webcam_16_9" \
  --mode "experience" \
  --motion "radar_pulse" \
  --handoff "obs_browser_source" \
  --output BRIEF.md

# Validate brief completeness before code generation
python scripts/briefing.py validate BRIEF.md --json
```

### 5. Multilingual Typography & `<switch>` Support
SVG Maestro decouples text from geometry, keeping labels as semantic `<text>` nodes in a dedicated layer:
- **No Path Outlines**: Text remains editable via Inkscape's text tool. Converted vector paths in typography layers trigger an `OUTLINED_TEXT_WARNING`.
- **`<switch>` Contract**: Specific locales (`systemLanguage="pt"`, `systemLanguage="es"`) precede the default English fallback element as the final child.
- **Reference Example**: See `examples/i18n/multilingual_card.svg`.

### 6. The Navigator Router: `/ask-maestro`
Modeled directly after Matt Pocock's `/ask-matt` router, `/ask-maestro` acts as an architectural compass for users and AI agents:
- **The Main Flow**: Deterministic path from structured interview (`/svg-maestro brief` $\to$ `BRIEF.md`) to 3-pillar build, closed-loop linter (`validate_svg.py`), refinement verbs, and production handoff.
- **On-Ramps**: Dedicated entry points for existing SVG repairs (missing `transform-box`), foreign asset imports (Figma/Inkscape), multi-asset streaming kits (tracer-bullet ticket slicing), and Power BI DAX generation.
- **Context Hygiene**: Protects the LLM's **smart zone** (~150k tokens) by enforcing single-asset context windows when generating verbose vector XML.
- **Polyglot Interaction**: Greets, interviews, and troubleshoots in the user's conversational language (e.g. Portuguese) while keeping all XML tokens and code strictly in canonical English.

---

## Pipelines

### OBS Streaming Overlays (`scripts/obs_pipeline.py`)
Generates modular, transparent-viewport streaming overlays in `Experience` mode:

```bash
# Generate complete overlay kit (16:9 webcam frame + alert banner)
python scripts/obs_pipeline.py generate-all --output-dir examples/obs/ --theme cyan_magenta

# Generate customized webcam frame
python scripts/obs_pipeline.py webcam \
  --output examples/obs/webcam_frame_16_9.svg \
  --theme cyan_magenta \
  --cam-label "CAM 01 // LIVE FEED" \
  --status-label "REC ● 1080P"

# Generate customized alert banner
python scripts/obs_pipeline.py alert \
  --output examples/obs/alert_banner.svg \
  --theme cyan_magenta \
  --type "NEW SUBSCRIBER" \
  --user "CYBER_PHANTOM"
```

Available themes: `cyan_magenta`, `amber_gold`, `matrix_green`, `crimson_hazard`.

### Dashboard Widgets & Power BI DAX (`scripts/dashboard_pipeline.py`)
Generates metric cards in `Operate` mode and exports DAX measure snippets for Power BI Image visuals:

```bash
# Generate complete dashboard kit (SVG card + DAX measure)
python scripts/dashboard_pipeline.py generate-all --output-dir examples/dashboard/ --theme dark_slate

# Convert any SVG into a Power BI Data URI DAX measure
python scripts/dashboard_pipeline.py dax \
  --input examples/dashboard/telemetry_card.svg \
  --output examples/dashboard/telemetry_card.dax \
  --measure-name TelemetryCard
```

Available themes: `dark_slate`, `obsidian_amber`, `matrix_emerald`, `deep_violet`.

---

## Autonomous Closed-Loop Validation

SVG Maestro includes a zero-dependency validation linter (`validate_svg.py`):

```bash
python scripts/validate_svg.py path/to/vector.svg
```

For programmatic agent consumption:

```bash
python scripts/validate_svg.py path/to/vector.svg --json
```

---

## Repository Layout

```
svg-maestro/
├── .github/workflows/ci.yml    # Continuous integration workflow
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
│   ├── dashboard/              # Metric cards & DAX snippet
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
│   ├── tickets/                # Executable tracer-bullet tickets (01 - 06)
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

## Credits & Acknowledgments

- Inspired by **Matt Pocock's** agentic engineering ecosystem (`grilling`, `domain-modeling`, `to-spec`, `to-tickets`, `tdd`).
- Inspired by the **Impeccable** design skill for its philosophy of surface modes and creative refinement verbs.

---

## License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.
