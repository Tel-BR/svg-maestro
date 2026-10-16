# Specification: SVG Maestro (Vector Craft & Motion Orchestration System)

## Problem Statement

AI coding agents (Antigravity, Claude, Codex) produce visually generic, fragile, or broken vector graphics when asked to generate layouts, telemetry widgets, or streaming overlays. This failure stems from three distinct root causes:
1. **Generic Aesthetic Direction ("AI Slop")**: Lack of mathematical proportion, dissonant color ramps, and timid cliches (e.g. floating cartoon gears or lightbulbs) due to the absence of a strong art direction framework.
2. **Inkscape Incompatibility**: Missing XML namespaces (`xmlns:inkscape`), flat ungrouped hierarchies lacking semantic layers, and chaotic `<defs>`, making manual collaboration in Inkscape frustrating or destructive.
3. **Fragile Animation & Mutation Collisions**: Directly animating element-level transforms without scoping (`transform-box: fill-box`), causing browser glitches and causing animations to break whenever a human editor scales, moves, or edits the vector in Inkscape.
4. **Language & Text Bottlenecks**: AI agents frequently bake text into vector paths (`path`), rendering graphics impossible to translate, inaccessible to screen readers, and locked into a single language.

Creators require a unified system that pairs disciplined software engineering processes with award-winning art direction, yielding production-grade, editable, and animated SVG vector assets.

---

## Solution

**SVG Maestro** fuses Matt Pocock's architectural discipline with Impeccable's radical design craft, establishing a deterministic vector engineering system:
- **Interactive Briefing Protocol (`/svg-maestro brief`)**: Multi-round structured elicitation using the interactive `ask_question` tool across 4 core dimensions (Surface Viewport, Mode, Motion Profile, and Handoff Target), generating a binding `BRIEF.md` before code generation.
- **Surface Modes & Craft Floor**: Classifies vector surfaces into `Operate` (data density for dashboards/Power BI), `Experience` (vibrant neon and ambient loops for OBS Studio), and `Persuade` (monumental Euclidean scale), with strict bans against generic clipart and muddy palettes.
- **Creative Refinement Verbs**: Empowers users to iteratively steer generated vectors using expressive direction commands (`bolder`, `quieter`, `distill`, `delight`, `animate`, and `critique`).
- **Mutation-Proof Wrapper Pattern**: Isolates motion wrappers (`<g class="anim-wrapper-...">`) from static Inkscape geometry nodes (`<g inkscape:label="...">`), ensuring full editability in Inkscape without breaking CSS `@keyframes` or SMIL animations.
- **Decoupled Typography & i18n**: Mandates that text remains semantic `<text>` tags in a dedicated Inkscape layer, with built-in `<switch>` and `systemLanguage` support for native multilingual graphics.
- **Autonomous Validation Loop**: An integrated, zero-dependency Python linter (`validate_svg.py`) that executes in the agent's background, verifying XML structure, Inkscape namespaces, layer conventions, and CSS transform contracts.

---

## User Stories

1. As a live stream broadcaster, I want to use `/svg-maestro brief` with interactive clickable options, so that I can define my 16:9 webcam overlay constraints in 20 seconds without writing long prompt instructions.
2. As an OBS Studio streamer, I want an animated neon webcam frame with transparent center and corner brackets, so that my camera feed looks sleek at 60fps without burdening CPU/GPU.
3. As a Power BI analyst, I want to generate a telemetry card in the `Operate` mode, so that metric readouts remain primary while geometric accents provide visual hierarchy.
4. As a business intelligence developer, I want the agent to output the metric card as a URL-encoded DAX string (`data:image/svg+xml;utf8,...`), so that I can paste it directly into a Power BI measure.
5. As a vector illustrator, I want every generated SVG to open in Inkscape with organized, labeled semantic layers, so that I can manually tweak anchor points and colors.
6. As a designer collaborating with AI, I want to move or resize elements in Inkscape without breaking browser animations, so that the human-in-the-loop workflow remains non-destructive.
7. As a creative director, I want to type `/svg-maestro bolder` on an existing card, so that the agent amplifies line weights, glow contrasts, and gradient saturation without manual coordinate editing.
8. As a UI designer, I want to run `/svg-maestro quieter`, so that overstimulated neon graphics are softened into understated, elegant tones.
9. As a minimalist engineer, I want to run `/svg-maestro distill`, so that secondary ornamental clutter is stripped away, leaving only pure Euclidean geometry.
10. As a motion designer, I want to run `/svg-maestro delight`, so that subtle orbital sweeps and breathing pulses are injected as micro-interactions.
11. As an animator, I want to feed a static SVG into `/svg-maestro animate`, so that the agent wraps target shapes in the Wrapper Pattern and injects CSS keyframes automatically.
12. As a quality engineer, I want to trigger `/svg-maestro critique`, so that I receive a two-axis heuristic audit scoring Technical Standards and Aesthetic Direction.
13. As an international content creator, I want the agent to conduct the briefing in Portuguese (or my native language) while writing canonical English XML attributes, so that I can communicate effortlessly without breaking global code standards.
14. As a global software developer, I want text elements preserved as semantic `<text>` tags with `<switch>` multilingual support, so that SVGs automatically display Portuguese or English depending on the visitor's browser.
15. As an autonomous AI agent, I want a zero-dependency Python script to inspect my generated SVG code, so that I catch and repair missing namespaces, invalid viewports, or broken transform origins before delivering to the user.

---

## Implementation Decisions

- **Architecture & Modularity**: Packaged as a standard specification (`SKILL.md`) interoperable across Antigravity, Claude Code, and Codex, with canonical documentation in English (`README.md`) and Portuguese (`README.pt-BR.md`).
- **Interactive Briefing Protocol**: Implemented via `ask_question` prompting, producing a binding `BRIEF.md` prior to multi-asset code generation.
- **Surface Modes & Craft Floor**: Embeds explicit rules for `Operate`, `Experience`, and `Persuade` modes, backed by absolute bans on generic clipart, muddy gradients, and unaligned nodes.
- **Creative Refinement Verbs**: Codifies standard transformation patterns for `bolder`, `quieter`, `distill`, `delight`, `animate`, and `critique`.
- **The Wrapper Pattern**: Enforces dedicated animation wrapper groups (`<g class="anim-wrapper-...">`) encapsulating child static geometry groups (`<g inkscape:label="...">`).
- **Universal CSS Transform Contract**: Requires that all `@keyframes` transform animations specify `transform-box: fill-box;` and `transform-origin: center;`.
- **Decoupled Vector Typography**: Prohibits text-to-path conversion; mandates semantic `<text>` nodes isolated in `layer-typography`.
- **Autonomous Python Validation Linter**: Implements `validate_svg.py` using strictly Python standard library modules (`xml.etree.ElementTree`, `re`, `argparse`, `sys`, `json`) with exit code 0 on pass and structured JSON diagnostics on error.

---

## Testing Decisions

- **Primary Test Seam**: The highest and primary seam is the CLI and programmatic entrypoint of `validate_svg.py` (`validate_svg_file(filepath)`).
- **Test Matrix & Fixtures**:
  - Positive compliance test: Valid multi-layer animated SVG documents must exit with code 0 (`valid: true`).
  - Namespace verification: Reject SVGs missing `xmlns:inkscape` or `viewBox`.
  - Layer verification: Reject SVGs lacking semantic layers (`inkscape:groupmode="layer"`).
  - Wrapper Pattern collision check: Flag warnings when transform animations target raw shape elements instead of wrapper groups.
  - Transform-box contract check: Reject CSS transform animations missing `transform-box: fill-box`.
  - i18n typography check: Verify that text nodes remain `<text>` and are not outlined as raw paths.

---

## Out of Scope

- Client-side interactive JavaScript or canvas scripting within standalone SVGs.
- Monolithic uncropped 1080p full-canvas artboards forcing manual source cropping in OBS.
- Proprietary vector formats (Adobe Illustrator `.ai` or CorelDRAW `.cdr`).
- Raster-only rendering pipelines.

---

## Further Notes

- Source repository managed in Git at `https://github.com/Tel-BR/svg-maestro`.
- Canonical documentation mirrored in Obsidian vault at `C:\Users\Admin\Vaults\Sync\Projetos\svg-maestro`.
- Global skill registered at `C:\Users\Admin\.gemini\config\skills\svg-maestro`.
