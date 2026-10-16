# 0001: Multiplatform Skill Packaging with Autonomous Python Validation Linter

## Context & Decision
To empower AI agents (Antigravity, Claude, Codex) to consistently generate complex, high-aesthetic, Inkscape-compatible SVGs without hallucinating broken namespaces or invalid CSS properties, we decided to package the solution as a portable Agent Skill (`SKILL.md`) paired with a lightweight, zero-dependency Python linter (`validate_svg.py`). The agent executes this linter autonomously during generation passes to guarantee syntactic, semantic, and structural compliance before delivering artifacts.

## Considered Options
- *Pure Prompt / Markdown-only Skill*: Rejected because LLMs reliably drop Inkscape namespaces or mangle `transform-box` without mechanical feedback.
- *Node/NPM CLI Tooling*: Rejected due to environment dependencies; Python standard library (`xml.etree.ElementTree` or `re`) runs universally in agent execution environments without requiring `npm install`.

## Consequences
- Agents must run `python validate_svg.py <file.svg>` as part of their generation loop.
- Inkscape compliance and animation safety are verified mechanically rather than relying on LLM memory alone.
