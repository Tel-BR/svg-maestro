# 02: OBS Streaming Overlays Pipeline

**What to build:** The capability for an agent to generate modular, transparent-viewport streaming overlays (such as a 16:9 webcam frame and an alert notification banner) featuring pulsing neon borders, animated stroke-tracing, and full Inkscape editability, verified autonomously by the linter before delivery.

**Blocked by:** 01: Core Linter Test Suite & Fixture Matrix.

**Status:** ready-for-agent

- [ ] Agent generates standalone 16:9 webcam frame SVG with transparent center and animated corner accents
- [ ] Agent generates modular alert banner SVG with continuous line tracing motion
- [ ] Every overlay adheres to the Wrapper Pattern so moving or resizing shapes in Inkscape does not break CSS animations
- [ ] All elements are organized into semantic Inkscape layers (`inkscape:groupmode="layer"`)
- [ ] Generated files pass automated linter validation with zero errors
- [ ] Overlays render crisply with transparency when imported as browser sources in streaming software
