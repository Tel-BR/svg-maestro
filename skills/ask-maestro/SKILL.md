---
name: ask-maestro
description: Ask which vector craft skill, flow, or refinement fits your situation. A router and architectural navigator over the SVG Maestro ecosystem.
disable-model-invocation: true
metadata:
  version: 0.1.0-beta.1
---

# Ask Maestro

You don't remember every SVG parameter, Inkscape namespace, or linter flag, so ask.

In the Maestro philosophy, **vectors are software architecture, not casual drawings**. You do not paint with an AI agent; you architect mathematical geometry, layer semantic node trees, isolate mutations, and enforce closed-loop linting.

A **flow** is a path through the vector skills. Most work travels along one **Main Flow**, and four **On-Ramps** merge onto it. Everything else is a creative refinement verb or a foundational vocabulary layer running underneath.

---

## The Main Flow: Idea → Production Vector

The route 90% of vector work travels. You have a visual requirement and want a production-grade, editable, and animated SVG delivered.

### 1. `/svg-maestro brief` sharpens the constraints by interview
Start here whenever creating a new graphic. **Absolute prohibition**: the agent must NEVER generate raw SVG code from a loose, unconstrained prompt (e.g. "make a cool webcam overlay").
The agent triggers an interactive elicitation interview covering the 4 core dimensions:
- **Surface Viewport**: Exact dimensions and aspect ratio (16:9 webcam, 800x500 telemetry card, alert banner, etc.).
- **Surface Mode**: `Operate` (data density for dashboards/Power BI), `Experience` (cyber neon & ambient motion for OBS), or `Persuade` (monumental Euclidean scale).
- **Motion Profile**: Universal CSS keyframes (Tier 1), SMIL morphing (Tier 2), or Static.
- **Handoff Target**: OBS Browser Source, Power BI DAX string, Web DOM, or Inkscape editable vector.

The agreed constraints are serialized into `BRIEF.md`. It is the binding single source of truth.

### 2. Branch: Do you need to test visual rhythm and contrast before committing?
- **No** (the aesthetic tokens and layout are clear in your mind) $\to$ proceed directly to step 3.
- **Yes** (you need to evaluate whether the color harmony and line balance feel right) $\to$ **Detour through a Tracer-Bullet Prototype**:
  - Generate a minimal static wireframe containing only core geometric outlines and color ramps.
  - Review in your browser or Inkscape.
  - Fold the approved palette into `BRIEF.md` and merge back onto the main flow at step 3.

### 3. Branch: Is this a single asset or a multi-asset kit?
- **Single Asset** (e.g., one telemetry card or one webcam frame) $\to$ Build right here in the current context window.
- **Multi-Asset Kit** (e.g., full Stream Pack with Webcam, Alert, Chat, and Goal Bar; or an executive KPI suite) $\to$ **NEVER generate all assets in a single context window**.
  - Detailed SVG code is dense with coordinates. Emitting multiple large files causes the model to exit its **smart zone**, resulting in hallucinated closing tags (`</g>`) and forgotten CSS contracts.
  - Slice the kit into tracer-bullet tickets under `docs/tickets/` (one file per asset declaring its viewport and mode).
  - Implement each ticket in an isolated, fresh context window (`/clear` or dedicated subagent), inheriting shared tokens from `BRIEF.md`.

### 4. Architectural Build under the Three Foundational Pillars
Every generated SVG must satisfy three non-negotiables:
1. **Mathematical Geometry & Craft Floor**: Proportions derived from Fibonacci, Golden Ratio ($\phi \approx 1.618$), or an 8px modular grid. Palette calculated using perceptual ramps (OKLCH/HSL). *Strictly banned*: generic AI clipart (floating gears, lightbulbs) and muddy gradients.
2. **Total Inkscape Compatibility**: Root namespaces (`xmlns:inkscape`, `xmlns:sodipodi`), semantic layers (`layer-background`, `layer-geometry`, `layer-accents`, `layer-typography`), and structured `<defs>` with human-readable IDs.
3. **The Wrapper Pattern**: All CSS `@keyframes` and SMIL animations target ONLY dedicated wrapper groups (`<g class="anim-wrapper-...">`), strictly isolated from static Inkscape geometry nodes (`<g inkscape:label="...">`). Any CSS transform MUST declare:
   ```css
   transform-box: fill-box;
   transform-origin: center;
   ```

### 5. Autonomous Closed-Loop Validation
**Facts are the linter's job; decisions are yours.**
Before presenting any SVG code to the human, the agent executes:
```bash
python scripts/validate_svg.py <generated-file.svg> --json
```
The agent is **strictly forbidden** from delivering the file or asking for human feedback if the linter exits with non-zero status. If missing namespaces, broken transform origins, or outlined paths are flagged, the agent repairs the code in an autonomous closed loop until `valid: true`.

### 6. Creative Refinement Verbs (Steering Art Direction)
Once the SVG is valid on screen, **never edit coordinates manually in conversation** ("move x by 10px"). Steer the aesthetic using expressive refinement verbs:
- `/bolder` $\to$ Boost stroke weights (1.4x-1.8x) and amplify glow contrast.
- `/quieter` $\to$ Tone down saturation and soften lines (0.6x-0.75x).
- `/distill` $\to$ Strip secondary decorative noise, preserving pure Euclidean geometry.
- `/delight` $\to$ Inject micro-interaction motion (orbital radar ring, breathing pulse).
- `/animate` $\to$ Upgrade a static graphic into a motion asset via the Wrapper Pattern.
- `/critique` $\to$ Run a two-axis audit evaluating Technical Standards vs. Aesthetic Craft.

### 7. Handoff & Deployment
Deliver the finalized asset in its target production format:
- **OBS Studio**: Clean SVG ready for Browser Source with transparent background.
- **Power BI**: Exported as an URL-encoded DAX measure string via `scripts/dashboard_pipeline.py`.
- **Inkscape**: Fully editable vector with decoupled typography and structured layers.

---

## On-Ramps

Specialized starting situations that generate work, then merge onto the Main Flow.

### 1. "I have an existing SVG from Figma, Illustrator, or Inkscape and want to animate or standardize it"
You do not recreate human design from scratch.
1. Run the audit: `python scripts/validate_svg.py input.svg --json`.
2. Inspect diagnostic warnings (missing Inkscape namespaces, ungrouped shapes, or text baked into `path`).
3. Apply the **Wrapper Pattern** around movable geometry groups.
4. Merge onto the Main Flow at **Step 6** using `/svg-maestro animate` or `/svg-maestro delight`.

### 2. "Something is broken: the animation is erratic in OBS or Inkscape broke my transforms"
For tough mutation bugs:
- The Maestro refuses to theorize. Run `python scripts/validate_svg.py <file.svg> --json`.
- Missing `transform-box: fill-box` makes CSS rotations spin around the entire canvas instead of the element's center.
- Missing wrapper groups cause Inkscape's inline `transform="..."` to collide with CSS keyframes.
- Apply surgical repair and merge back onto the Main Flow at **Step 5** (Linter verification).

### 3. "I need a multi-asset streaming pack or KPI dashboard suite"
- Do not draft assets one by one haphazardly.
- Execute `/svg-maestro brief` to establish common palette tokens, typography, and theme mode.
- Generate tickets in `docs/tickets/` with explicit viewport dimensions for each asset.
- Work ticket-by-ticket, clearing context between runs.

### 4. "I need an interactive Power BI telemetry widget"
- Standard web SVGs fail in Power BI due to unescaped special characters and unsupported external CSS.
- Route directly to `scripts/dashboard_pipeline.py`.
- Forces `Operate` mode (high scanability and data density), wraps metrics in dynamic DAX variables, and outputs ready-to-paste `data:image/svg+xml;utf8,...` code.

### 5. "I want to check toolchain health or update SVG Maestro to the latest release"
- The router checks version status via `python scripts/update_notifier.py --check-update`.
- If an update is available, provide copy-paste update instructions:
  ```bash
  git -C <path-to-skill> pull
  ```
- Toolchain updates never halt creative momentum: inform the user cordially and proceed immediately with the design task.

---

## Context Hygiene: The Smart Zone in Vector Engineering

Vector code is exceptionally token-heavy: hundreds of numerical coordinates, path commands, and CSS keyframe rules consume token capacity rapidly.

- **Keep Steps 1 and 2 in one unbroken context window**: The briefing interview and the resulting `BRIEF.md` must stay fresh in memory.
- **Clear context between kit assets**: When building a multi-asset suite, never generate all assets in the same conversation. Work one ticket, run `validate_svg.py`, commit or save, and `/clear` before tackling the next asset.
- **The Smart Zone Limit**: SOTA models reason with peak architectural clarity up to ~150k tokens. Once you generate multiple large SVGs in one session, the model's spatial reasoning degrades, leading to unclosed XML tags and broken CSS selectors. `/compact` or `/clear` at phase boundaries.

---

## Creative Refinement Verbs (The Standalone Palette)

Reach for these verbs when the vector already exists and needs aesthetic adjustment:

- **`bolder`**: Amplifies stroke widths (1.4x-1.8x), enhances gradient contrast, and strengthens neon glow.
- **`quieter`**: Softens tonal contrast, reduces saturation, and refines line thickness for calm elegance.
- **`distill`**: Removes secondary ornamentations (micro grid tics, auxiliary rings), revealing pure geometry.
- **`delight`**: Encapsulates subtle micro-interactions (orbital satellites, pulsating radar, ambient sweeps).
- **`animate`**: Automatically wraps static shapes in `<g class="anim-wrapper-...">` and injects CSS keyframes.
- **`critique`**: Delivers a two-axis evaluation: (1) Technical Standards (Inkscape layers, linter zero-error pass) and (2) Aesthetic Craft (modular proportions, color balance, Craft Floor compliance).

---

## Underneath Vocabulary

Foundational concepts that inform all skills:

- **Surface Modes**:
  - `Operate`: Dashboards, KPIs, and Power BI. Visual hierarchy serves metric comprehension. Zero distracting fluff.
  - `Experience`: OBS Studio and live streaming. Cyber neon, high-contrast illumination, transparent center, 60fps ambient motion.
  - `Persuade`: Hero canvases and branding. Monumental scale, Golden Ratio harmony, emotional resonance.
- **The Wrapper Pattern**: The structural firewall separating machine animations from human edits. The outer `<g class="anim-wrapper-...">` is animated; the inner `<g inkscape:label="...">` is edited by humans. Neither overrides the other.
- **Decoupled Typography**: Text is strictly authored as semantic `<text>` nodes in `layer-typography`. Never outline fonts into static `<path>` shapes. Multi-locale graphics use native `<switch>` and `systemLanguage`.
- **The Craft Floor**: Non-negotiable quality baseline. Absolute bans on generic AI clipart, muddy 3-stop gradients, and broken curve tangencies.
- **Lifecycle & Version Management**: Autonomous background verification (`scripts/update_notifier.py`) that checks for upstream releases with 24-hour caching and zero interruption to active vector design flows.

---

## Internationalization (i18n) Protocol

1. **Polyglot Conversational Navigator**:
   - Detect the user's conversational language automatically.
   - Conduct the interactive briefing, diagnostic troubleshooting, and refinement critique in the user's native tongue (e.g. Portuguese or English).
   - All internal XML attributes, CSS classes, layer names, and CLI flags remain in canonical English.
2. **Native Multilingual Graphics**:
   - When the user requires multi-language assets, leverage SVG `<switch>` with `systemLanguage="pt"`, `systemLanguage="es"`, and an unadorned English fallback.
   - Text elements remain 100% editable in Inkscape's text tool for translators.

---

## Lifecycle & Version Management

SVG Maestro maintains version awareness across host environments (Antigravity, Claude Code, Codex):
- **Autonomous Version Check**: Agents verify toolchain currency using `python scripts/update_notifier.py --check-update --json`.
- **Distribution Manifests**: Packaged with `.claude-plugin/plugin.json` (Claude Code) and `skills.json` (`npx skills`) locked at parity (`0.1.0-beta.1`).
- **24-Hour Local Cache**: Avoids GitHub API rate limiting by caching release status in `.update_cache.json`.
- **Cordial Notification**: When a new release is detected, notify the user cordially with copy-paste upgrade commands (`git -C <path-to-skill> pull`).
- **Unbroken Workflow Guarantee**: Never block or halt active vector drafting, briefing, or linting loops.
