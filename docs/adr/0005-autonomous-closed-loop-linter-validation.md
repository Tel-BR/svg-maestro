# 0005: Autonomous Closed-Loop Linter Validation

## Context & Decision
LLMs frequently introduce subtle XML, CSS, or namespace regressions when emitting complex SVG files (such as missing `xmlns:inkscape`, omitted `transform-box: fill-box`, or malformed `<style>` tags). We decided to implement an **Autonomous Validation Loop**: the agent executes `python scripts/validate_svg.py <target.svg>` immediately after generation, parses the linter's diagnostic report, fixes any identified defects in an automatic remediation pass, and only presents the final artifact to the user once validation reports zero errors.

## Considered Options
- *Manual On-Demand Linting*: Rejected because asking the user to manually execute a linter and report errors back to the agent introduces cognitive burden and breaks flow.
- *Visual Self-Critique Only*: Rejected because visual checks cannot reliably detect hidden DOM or namespace bugs that corrupt Inkscape or break CSS transforms in edge-case browsers.

## Consequences
- Every SVG produced by the agent is mechanically verified against XML, Inkscape namespaces, layer attributes, and CSS transform standards before delivery.
