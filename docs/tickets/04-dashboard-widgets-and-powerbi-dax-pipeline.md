# 04: Dashboard Widgets and Power BI DAX Pipeline (Operate Mode)

**What to build:** The capability for an agent to engineer modular telemetry and metric cards in `Operate` mode with golden ratio proportions, pulsing radar rings, and clean data typography, supporting both standalone SVG export for web apps and URL-encoded DAX measure string generation for Power BI visuals.

**Blocked by:** 01: Core Linter Test Suite & Fixture Matrix, 02: Interactive Briefing Module (`ask_question` Protocol).

**Status:** closed

- [x] Agent generates standalone metric card SVG with clean grid lines and animated sweep indicators
- [x] Agent provides the exact DAX measure snippet with `data:image/svg+xml;utf8,` formatting and `%23` hex escaping for Power BI
- [x] Typography and metric readouts are decoupled into dedicated Inkscape text layers for effortless human editing
- [x] Motion elements utilize `transform-box: fill-box` and `transform-origin: center` for cross-browser stability
- [x] Generated SVG files pass linter verification with zero errors
