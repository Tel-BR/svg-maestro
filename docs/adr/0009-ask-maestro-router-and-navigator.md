# 0009: Ask Maestro Router and Operational Navigator

## Context & Decision
Creators and AI coding agents operating across SVG Maestro frequently face decision paralysis due to the rich multi-pipeline toolset (briefing protocols, Python linters, OBS animation layers, DAX exporters, refinement verbs, and internationalization). Without a singular operational router, users either guess coordinates, bypass the briefing phase, or overload the LLM context window with multi-asset XML.

Drawing direct architectural inspiration from Matt Pocock's `/ask-matt` skill, we decided to build **`/ask-maestro`**:
1. **The Canonical Main Flow (`brief` &rarr; `validate` &rarr; `refine` &rarr; `handoff`)**: Establishes a deterministic path where the agent is strictly prohibited from emitting code without a binding `BRIEF.md` and prohibited from asking user approval before the linter exits with code 0 (`valid: true`).
2. **Four Specialized On-Ramps**: Defines clear entry points for foreign SVG imports (Figma/Inkscape), broken mutation collisions (missing `transform-box`), multi-asset kits (requiring tracer-bullet tickets), and Power BI telemetry cards.
3. **Context Hygiene in the Smart Zone**: Vector XML is coordinate-heavy. To prevent degraded reasoning, hallucinated closing tags, or broken CSS contracts, multi-asset generation must clear context between tickets.
4. **Bilingual & Internationalization Protocol**: Instructions are maintained in canonical English for global agent precision, while the agent conversationally diagnoses, questions, and guides in the user's native tongue (e.g., Portuguese).

## Considered Options
- *Static Cheatsheet / Manual*: Rejected because users do not read static documentation during interactive coding sessions.
- *Unconstrained Chat Free-Form*: Rejected because agents frequently hallucinate unlayered, unlinted clipart when given open-ended prompts.

## Consequences
- Lost users can type `/ask-maestro` to receive an instant, authoritative recommendation of what to do, how to do it, and in what order.
- Production vector generation becomes disciplined, mutation-proof, and consistent across all projects.
