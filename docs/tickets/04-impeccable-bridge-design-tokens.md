# 04: Impeccable Bridge Token Reader

**What to build:** An automated token extraction mechanism that checks whether the target workspace contains design documentation (`DESIGN.md` or `PRODUCT.md` produced by the `impeccable` skill) and maps project color ramps, dark-mode surfaces, and typography onto the generated SVG vectors so they blend seamlessly into the existing application.

**Blocked by:** 02: OBS Streaming Overlays Pipeline, 03: Dashboard Widgets and Power BI DAX Pipeline.

**Status:** ready-for-agent

- [ ] Agent inspects workspace for design tokens before synthesizing SVG palettes
- [ ] If tokens exist, generated gradients and stroke fills directly mirror the project's brand palette
- [ ] If no tokens exist, the agent falls back cleanly to autonomous mathematical geometric palettes (OKLCH harmonic ramps) without failing or stalling
- [ ] Injected tokens and font families remain completely editable inside Inkscape
- [ ] Generated files pass linter verification with zero errors
