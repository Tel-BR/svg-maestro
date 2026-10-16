# 01: Core Linter Test Suite & Fixture Matrix

**What to build:** An automated test runner that feeds valid and deliberately malformed SVG documents into the validation linter, mechanically verifying that every architectural rule (Inkscape namespaces, semantic layers, defs hygiene, Wrapper Pattern transform scoping, and CSS transform-box contracts) correctly passes or fails with exact diagnostic codes.

**Blocked by:** None (can start immediately).

**Status:** closed

- [x] Automated test script that runs with zero external dependencies using only standard Python
- [x] Test fixtures covering positive compliance cases for multi-layer Inkscape SVGs
- [x] Test fixtures verifying rejection of SVGs missing Inkscape namespaces
- [x] Test fixtures verifying detection of missing semantic layer attributes
- [x] Test fixtures verifying warnings when transform animations directly target shape nodes instead of wrapper groups
- [x] Test fixtures verifying rejection of transform keyframes missing `transform-box: fill-box`
- [x] All assertions pass with exit code 0 when testing valid documents and exit code 1 when testing malformed documents
