# 0007: Zero-Dependency Python Validation Engine

## Context & Decision
To ensure that the validation linter executes reliably across heterogeneous agent runtime environments (Antigravity local shell, Claude Code containers, Codex sandbox environments, CI runners, and user workstations), we decided that `validate_svg.py` must depend strictly on the **Python standard library** (`xml.etree.ElementTree`, `re`, `argparse`, `sys`, `json`).

## Considered Options
- *External XML / CSS Libraries (lxml, cssutils, tinycss2)*: Rejected because external packages require environment preparation (`pip install`), virtual environments, or compilation steps that fail or add latency in locked agent sandboxes.

## Consequences
- The validation script executes instantaneously with zero setup on any machine with Python 3.8+.
- XML parsing and CSS regex verification are fully self-contained within a single portable script.
