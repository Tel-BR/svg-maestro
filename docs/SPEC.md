# Specification: SVG Maestro (Vector Craft & Motion Orchestration System)

## Problem Statement

AI coding agents (Antigravity, Claude, Codex) frequently produce naive, generic, or broken vector illustrations when requested to generate visual layouts, dashboard components, or streaming graphics. Their native output often suffers from:
1. **Generic Aesthetic Quality ("AI Slop")**: Lack of mathematical proportion, dissonant color choices, and visually repetitive clipart styles.
2. **Inkscape Incompatibility**: Missing namespaces (`xmlns:inkscape`), flat unorganized group hierarchies without semantic layers, and chaotic `<defs>`, making human handoff and manual vector editing in Inkscape painful or impossible.
3. **Fragile Animation**: Directly animating SVG elements without transform scoping (`transform-box: fill-box; transform-origin: center`), which causes browser visual glitches and causes animations to break or be destroyed whenever a user edits or scales the vector shapes in Inkscape.

Users require a dependable, cross-agent system that guarantees production-grade vector aesthetics, seamless two-way human/AI collaboration in Inkscape, and non-destructive native animation.

---

## Solution

The SVG Maestro system equips AI agents with a comprehensive vector engineering skill and an autonomous, zero-dependency validation linter. The solution guarantees:
- **Mathematical Geometric Direction**: Native reliance on Fibonacci scales, Golden Ratio proportions ($\phi \approx 1.618$), isometric projections, and harmonic color palettes, operating under a strict Zero-Bias Policy (no pre-drawn clipart templates to prevent model overfitting).
- **Impeccable Design Bridge**: Automatic inheritance of design tokens and color palettes from existing project design systems (`DESIGN.md` / `PRODUCT.md`) when present.
- **Inkscape Semantic Architecture**: Mandated root namespaces, semantic Inkscape layers (`inkscape:groupmode="layer"`, `inkscape:label`), and clean `<defs>` hygiene with human-readable IDs.
- **Mutation-Proof Wrapper Pattern**: Decoupling motion directives (`<g class="anim-wrapper-...">`) from static geometry (`<g inkscape:label="...">`), ensuring human manipulations in Inkscape do not collide with or destroy CSS `@keyframes` or SMIL animations.
- **Autonomous Validation Loop**: An embedded, zero-dependency Python linter that runs silently in the agent's background, verifying XML structure, Inkscape layers, and animation contracts before delivering the file to the user.

---

## User Stories

1. As a frontend developer, I want to request animated SVG metric cards for my dashboard, so that I can display live telemetry data with sophisticated visual hierarchy without relying on heavy external canvas libraries.
2. As a streaming broadcaster, I want to generate bespoke 16:9 webcam overlays with animated neon borders, so that I can enhance my OBS Studio production with crisp vector graphics that scale to any resolution.
3. As a UI designer, I want every generated SVG to open in Inkscape with organized, labeled layers, so that I can fine-tune shapes, adjust colors, and reorder elements in a visual vector editor.
4. As an illustrator, I want to adjust and move vector nodes in Inkscape without breaking browser animations, so that my collaborative workflow between AI generation and manual refinement remains non-destructive.
5. As an autonomous AI agent, I want a mechanical validation tool to inspect my generated SVG code, so that I can catch and repair missing namespaces, invalid viewports, or broken transform origins before presenting work to the user.
6. As a Power BI analyst, I want modular SVG cards formatted with standalone viewports, so that I can embed dynamic vector graphics directly inside DAX image measures.
7. As a motion designer, I want Tier 1 CSS animations to strictly declare `transform-box: fill-box` and `transform-origin: center`, so that geometric rotation and scaling behave predictably across all web engines.
8. As a content creator, I want OBS alert frames with animated line tracing (`stroke-dasharray`), so that viewers receive immediate visual feedback during live stream events.
9. As a design director, I want the AI to generate vector artwork from mathematical Euclidean principles rather than copy-pasting template boilerplate, so that every visual asset is uniquely tailored to the project prompt.
10. As a product developer, I want the SVG generator to seamlessly digest my project's existing `DESIGN.md` tokens, so that newly generated vector illustrations harmonize with my application's brand identity.
11. As a live streamer, I want modular SVG assets with independent viewports rather than a monolithic full-screen canvas, so that I can position, crop, and animate webcam, chat, and alert sources separately in OBS Studio.
12. As a system administrator in an isolated environment, I want the SVG validator to run using only the standard Python runtime, so that validation functions instantaneously without network access or package installation.
13. As an engineer building high-impact landing pages, I want Tier 2 SMIL path morphing support, so that abstract geometric backdrops can fluidly shift between polygonal states.
14. As an accessibility-focused developer, I want all semantic SVG layers to declare clear text labels, so that screen readers and vector inspection tools clearly convey visual structure.
15. As a QA engineer, I want the linter to emit machine-readable JSON reports, so that continuous integration agents can automatically parse and enforce vector standards.

---

## Implementation Decisions

- **Multiplatform Agent Skill**: Packaged as a standard specification (`SKILL.md`) that guides Antigravity, Claude Code, and Codex on mathematical geometry, Inkscape layering conventions, and animation contracts.
- **Dual-Engine Aesthetics**: Incorporates built-in mathematical geometry formulas (Golden Ratio, Fibonacci scales, isometric projection grids, OKLCH harmonic ramps) for standalone operation, while defining an optional bridge to consume project tokens (`DESIGN.md` / `PRODUCT.md`).
- **Zero Visual Blueprints Policy**: Strictly excludes pre-drawn clipart, visual templates, or concrete SVG drawings from skill documentation to avoid biasing LLMs toward repetitive copy-paste outputs.
- **Inkscape Semantic Layer Convention**: Enforces that all top-level graphic groupings include `inkscape:groupmode="layer"` and `inkscape:label="{Layer Name}"`.
- **Defs Hygiene & ID Naming**: Mandates that all gradients, filters, masks, and clip paths reside in a root `<defs>` container with semantic, human-readable IDs (e.g. `grad-neon-cyan`, `filter-radar-glow`).
- **The Wrapper Pattern**: Mandates the encapsulation of animated geometry inside an animation wrapper group (`<g class="anim-wrapper-...">`) wrapping a static geometry group (`<g inkscape:label="...">`), protecting element-level transforms from Inkscape edit collisions.
- **Universal CSS Animation Contract**: Mandates that CSS `@keyframes` transform animations embedded in `<style>` must specify `transform-box: fill-box;` and `transform-origin: center;`.
- **Modular Viewport Architecture**: Mandates that each visual component (webcam frame, card, alert box) be authored in an independent SVG file with its own tightly bounded `viewBox`.
- **Autonomous Python Validation Linter**: Implements a standalone validation script using strictly Python standard library modules (`xml.etree.ElementTree`, `re`, `argparse`, `sys`, `json`) capable of emitting human-readable reports and machine-readable JSON payloads.

---

## Testing Decisions

- **External Behavior Testing**: Tests must verify the integrity of the exported SVG document and the diagnostic output of the validation linter rather than mocking internal regex or parsing passes.
- **Primary Test Seam**: The highest and primary seam is `validate_svg.py` CLI and programmatic module (`validate_svg_file(filepath)`). All behavioral contracts (namespaces, layers, defs, wrapper pattern, transform-box) are verified against real SVG files.
- **Verification Matrix**:
  - Valid multi-layer animated SVG files must pass with exit code 0 (`valid: true`).
  - SVGs missing `xmlns:inkscape` or `viewBox` must trigger hard errors.
  - SVGs without semantic Inkscape layers must trigger layer errors.
  - SVGs with direct transform animations on shape nodes without wrapper groups must trigger wrapper pattern collision warnings.
  - SVGs with CSS transform animations missing `transform-box: fill-box` must trigger transform contract errors.
- **Prior Art**: Modeled after standard CLI linters (ESLint, Prettier, Ruff) designed to provide immediate mechanical feedback to agents in closed remediation loops.

---

## Out of Scope

- Client-side JavaScript interactivity or external runtime scripting (Tier 3 animation) within standalone SVG files.
- Monolithic full-screen 1080p canvas layouts containing all streaming widgets in a single uncropped file.
- Direct raster rendering pipelines or server-side PNG/WebP rasterization tooling.
- Proprietary third-party vector format conversions (e.g. Adobe Illustrator `.ai` or CorelDRAW `.cdr` binary formats).

---

## Further Notes

- The skill is installed both in the canonical Obsidian project vault (`C:\Users\Admin\Vaults\Sync\Projetos\svg-maestro`) and mirrored in the global agent configuration directory (`C:\Users\Admin\.gemini\config\skills\svg-maestro`).
- The canonical test fixture `tests/test_card.svg` serves as an active golden test demonstrating 100% compliance with all architectural decisions.
