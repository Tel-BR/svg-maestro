# 01: Core Linter Test Suite & Fixture Matrix

**What to build:** An automated test runner that feeds valid and deliberately malformed SVG documents into the validation linter, mechanically verifying that every architectural rule (Inkscape namespaces, semantic layers, defs hygiene, Wrapper Pattern transform scoping, and CSS transform-box contracts) correctly passes or fails with exact diagnostic codes.

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

- [ ] Automated test script that runs with zero external dependencies using only standard Python
- [ ] Test fixtures covering positive compliance cases for multi-layer Inkscape SVGs
- [ ] Test fixtures verifying rejection of SVGs missing Inkscape namespaces
- [ ] Test fixtures verifying detection of missing semantic layer attributes
- [ ] Test fixtures verifying warnings when transform animations directly target shape nodes instead of wrapper groups
- [ ] Test fixtures verifying rejection of transform keyframes missing `transform-box: fill-box`
- [ ] All assertions pass with exit code 0 when testing valid documents and exit code 1 when testing malformed documents
