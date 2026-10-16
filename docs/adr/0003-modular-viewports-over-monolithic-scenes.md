# 0003: Modular Viewports Over Monolithic Scenes

## Context & Decision
When generating layouts for dashboards and OBS Studio streaming overlays, authors frequently face a choice between delivering a single monolithic 1920x1080 canvas with all components placed, or outputting discrete, independent SVG files for each component (e.g. webcam frame, chat box, metric card). We decided to standardize on **Modular Viewports**: every generated element possesses its own tight, aspect-ratio-accurate `viewBox`.

## Considered Options
- *Monolithic 1080p Full Canvas*: Rejected because OBS Studio and web layouts require flexible resizing, independent positioning, and individual source toggling. A monolithic canvas forces users to manually crop or mask sources.

## Consequences
- Each overlay or dashboard widget is an independent file (`webcam-frame.svg`, `metric-card.svg`).
- Users can import them into OBS Studio as standalone Browser Sources or Image Sources without awkward alignment steps.
