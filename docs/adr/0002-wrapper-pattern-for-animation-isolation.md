# 0002: Wrapper Pattern for Mutation-Proof SVG Animation

## Context & Decision
When users edit animated SVG files in Inkscape (moving, scaling, or reshaping elements), Inkscape injects or mutates inline `transform` attributes directly on the targeted nodes, which overrides or corrupts CSS `@keyframes` and SMIL transformations. To achieve non-destructive human-machine collaboration, we mandate the **Wrapper Pattern**: every animated element must encapsulate its geometry within a dedicated animation wrapper group (`<g class="anim-wrapper-...">`), while static Inkscape layer and shape descriptors are kept in child content groups (`<g inkscape:label="...">`).

## Considered Options
- *Direct element targeting (animating paths or shapes directly)*: Rejected because any positional tweak in Inkscape breaks transform origins or gets overwritten by CSS keyframes.
- *Strict static-only exports*: Rejected because native motion in dashboards and OBS Studio is an explicit core requirement.

## Consequences
- Clean separation of concerns: humans edit geometry inside Inkscape without touching animation wrappers; the browser or OBS renders animations smoothly on top of updated geometry.
- SVG DOM hierarchy has one additional wrapping level per animated cluster.
