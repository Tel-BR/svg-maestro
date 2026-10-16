# 0004: Dual-Engine Aesthetics and Impeccable Bridge

## Context & Decision
To guarantee exceptional visual direction without introducing brittle hard dependencies or analysis paralysis between stand-alone operation and integration with the `impeccable` design skill, we established the **Dual-Engine Aesthetics** model. The skill contains complete native mathematical geometry specifications (Fibonacci/Golden Ratio proportions, isometric projections, Euclidean curvature continuity, harmonized OKLCH/HSL palettes), while natively supporting an **Impeccable Bridge** that reads and maps `DESIGN.md` / `PRODUCT.md` tokens when they exist in the project workspace.

## Considered Options
- *Mandatory Two-Pass Workflow (Chaining Impeccable)*: Rejected because requiring a full Impeccable review before generating an SVG asset adds excessive friction and fails in environments where Impeccable is not installed.
- *Strictly Independent Styling*: Rejected because ignoring project tokens would cause stylistic divergence in projects already managed by Impeccable.

## Consequences
- The skill generates museum-grade geometric vectors out of the box in zero-config environments.
- When embedded in an Impeccable-managed repository, generated SVGs automatically match project typography, palettes, and design tokens.
