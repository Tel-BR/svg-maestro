# SVG Maestro (Vector Craft & Motion Orchestration System)

A reusable design and vector engineering system for AI agents (Antigravity, Claude, Codex) fusing Matt Pocock's architectural discipline with Impeccable's radical art direction to orchestrate high-end geometric SVG layouts, dashboard components, OBS streaming overlays, and standalone vector illustrations with native animation, mutation-proof Inkscape compatibility, and internationalization.

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

### Aesthetics & Art Direction (The Impeccable Fusion)

**Surface Mode**:
The experiential intent defining visual density, contrast, and motion behavior for a given vector artifact:
- `Operate`: Prioritizes data density, scanability, and crisp legibility for dashboard cards and Power BI visuals.
- `Experience`: Prioritizes immersion, high-contrast neon illumination, and ambient motion for OBS streaming overlays.
- `Persuade`: Prioritizes grand Euclidean geometric scale and emotional resonance for hero banners and brand art.
_Avoid_: Generic style, one-size-fits-all aesthetic

**Craft Floor**:
The non-negotiable floor of visual excellence that forbids generic "AI slop", muddy three-color gradients, broken vector tangencies, and unanchored clipart.
_Avoid_: Safe design, timid vector, generic clipart

**Art Direction Verbs**:
A suite of expressive command verbs (`bolder`, `quieter`, `distill`, `delight`, `animate`, `critique`) allowing users to sculpt vector aesthetics through high-level creative direction rather than micromanaging coordinates.
_Avoid_: Coordinate tweaking, manual path dragging

**Zero-Bias Specification**:
An architectural rule stating that skills must convey geometric logic, math formulas, and abstract syntactic schemas rather than pre-drawn visual templates, preventing the agent from overfitting or copying fixed graphics.
_Avoid_: Boilerplate drawing, template clipart

### Discovery & Internationalization

**Interactive Briefing Protocol**:
A rapid multi-round elicitation process executed via the interactive `ask_question` tool, extracting constraints across 4 core dimensions (Surface, Mood, Motion, Handoff) before emitting any SVG code.
_Avoid_: Open-ended interview, guessing prompt

**Decoupled Typography**:
The architectural requirement that all textual labels and metrics remain editable SVG `<text>` elements isolated in a dedicated Inkscape layer, supporting native multilingual `<switch>` selection and easy human translation.
_Avoid_: Text-to-path, outlined text, baked typography

**Polyglot Agent**:
An agent behavior where all user-facing interactions, questions, and critique reports occur in the user's conversational language, while internal XML markup, classes, and IDs remain in canonical English.
_Avoid_: English-only interaction, localized XML tags
