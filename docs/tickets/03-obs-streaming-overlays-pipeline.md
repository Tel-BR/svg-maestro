# 03: OBS Streaming Overlays Pipeline (Experience Mode)

**What to build:** The capability for an agent to generate modular, transparent-viewport streaming overlays in `Experience` mode (such as a 16:9 webcam frame and an alert notification banner) featuring pulsing neon borders, animated stroke-tracing, and full Inkscape editability, verified autonomously by the linter before delivery.

**Blocked by:** 01: Core Linter Test Suite & Fixture Matrix, 02: Interactive Briefing Module (`ask_question` Protocol).

**Status:** closed

- [x] Agent generates standalone 16:9 webcam frame SVG with transparent center and animated corner accents
- [x] Agent generates modular alert banner SVG with continuous line tracing motion
- [x] Every overlay adheres to the Wrapper Pattern so moving or resizing shapes in Inkscape does not break CSS animations
- [x] All elements are organized into semantic Inkscape layers (`inkscape:groupmode="layer"`)
- [x] Generated files pass automated linter validation with zero errors
- [x] Overlays render crisply with transparency when imported as browser sources in streaming software
