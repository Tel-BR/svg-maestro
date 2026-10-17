# 04: Suíte de Retrocompatibilidade e Tolerância a SVGs Legados

**What to build:** Ingestion robustness across `scripts/refinement_verbs.py` and `scripts/validate_svg.py` guaranteeing that SVGs created with older or un-versioned releases of SVG Maestro (or raw SVGs lacking wrapper patterns) can still be safely processed, validated, and refined without crashing.

**Blocked by:** 01: Verificador de Versões e Notificador de Atualizações (CLI/Script)

**Status:** ready-for-agent

- [ ] Inspect and harden `scripts/refinement_verbs.py` so that legacy SVGs missing `anim-wrapper` groups or semantic layer markers are gracefully upgraded in-memory rather than failing execution.
- [ ] Add fixture SVGs simulating legacy v0.1.0-beta.1 outputs under `tests/fixtures/legacy/`.
- [ ] Add regression tests in `tests/test_backward_compatibility.py` testing each refinement verb (`bolder`, `quieter`, `distill`, `delight`, `animate`, `critique`) on legacy fixtures.
- [ ] Confirm `scripts/validate_svg.py` provides actionable upgrade hints when legacy elements are encountered.
