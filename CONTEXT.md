# SVG Maestro (Vector Orchestration System)

A reusable design and vector engineering system for AI agents (Antigravity, Claude, Codex) to orchestrate high-end geometric SVG layouts, dashboard components, OBS streaming overlays, and standalone vector illustrations with native animation and full Inkscape editability.

## Language

### Core Architecture

**Agent Skill**:
A structured specification file (`SKILL.md`) interoperable across Antigravity, Claude Code, and Codex, defining prompting protocols, geometric constraints, and code generation contracts.
_Avoid_: Prompt string, system prompt snippet, custom instruction

**Validation Linter**:
A lightweight standalone Python script (`validate_svg.py`) executed by the agent to programmatically verify SVG syntax, Inkscape namespaces, layer conventions, defs cleanliness, and animation safety before delivery.
_Avoid_: Visual tester, manual inspection

**Autonomous Validation Loop**:
The mandatory agent protocol of executing the validation linter against every generated SVG in the background, automatically repairing detected defects before delivering the artifact to the user.
_Avoid_: User-assisted testing, manual QA

**Wrapper Pattern**:
An architectural pattern separating animation directives (`<g class="anim-wrapper-...">`) from geometric and shape definitions (`<g inkscape:label="...">`) to ensure edits in Inkscape never corrupt or collide with CSS or SMIL animations.
_Avoid_: Direct animation, inline transform mutation

**Semantic Layer**:
An SVG group marked with Inkscape-native attributes (`inkscape:groupmode="layer"` and `inkscape:label`) that maps directly into Inkscape's Layer panel for human editing.
_Avoid_: Generic group, raw `<g>` tag

**Modular Viewport**:
An SVG sizing architecture where every asset (dashboard widget, webcam frame, alert banner) is authored within its own tight, aspect-ratio-accurate `viewBox`, ensuring flexible positioning and scaling.
_Avoid_: Monolithic canvas, full-screen canvas

### Aesthetics & Geometry

**Dual-Engine Aesthetics**:
A design protocol combining built-in mathematical proportions (Golden Ratio, Fibonacci scales, isometric axes, Euclidean tangencies) with the ability to consume project-level design tokens (`DESIGN.md`, `PRODUCT.md`) when available.
_Avoid_: Hardcoded aesthetics, unconstrained styling

**Zero-Bias Specification**:
An architectural rule stating that skills must convey geometric logic, math formulas, and abstract syntactic schemas rather than pre-drawn visual templates, preventing the agent from overfitting or copying fixed graphics.
_Avoid_: Boilerplate drawing, template clipart

**Vector Filter FX**:
Advanced native SVG filter pipelines (`feTurbulence`, `feDisplacementMap`, `feGaussianBlur`, `feColorMatrix`) configured to produce organic, electric, or neon effects for streaming and high-impact UI.
_Avoid_: CSS backdrop filter, raster image overlay

### Animation Tiers

**Tier 1 Animation (Universal CSS)**:
Native declarative animation using CSS `@keyframes` embedded in the SVG `<style>` tag, utilizing `transform-box: fill-box` and `transform-origin: center`, compatible with all browsers, OBS, `<img>` tags, and fully non-destructive in Inkscape.
_Avoid_: Basic CSS, inline transitions

**Tier 2 Animation (SMIL Vector Motion)**:
Declarative vector morphing and path-following animation using native SVG `<animate>`, `<animateTransform>`, and `<animateMotion>` elements, self-contained without external scripts.
_Avoid_: JS vector animation, canvas animation

**Tier 3 Animation (Scripted Interactive)**:
Advanced dynamic animation or reactive behavior driven by embedded JavaScript or external animation APIs, intended strictly for browser contexts and OBS Browser Sources.
_Avoid_: Incompatible SVG, broken vector

### Domain Surfaces

**Streaming Overlay**:
A modular vector component designed for OBS Studio broadcasting (such as webcam frames, chat boxes, alert containers, and lower-thirds) with dedicated aspect ratios and transparent backdrops.
_Avoid_: Video asset, OBS plugin

**Dashboard Widget**:
A modular vector component designed to embed seamlessly within web application cards, grid containers, or Power BI visual measures.
_Avoid_: Full page SVG, static icon
