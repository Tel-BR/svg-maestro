# 06: Multilingual Typography and Internationalization

**What to build:** An internationalization pipeline ensuring that text elements are never outlined into static vector paths, verifying semantic `<text>` decoupling in `layer-typography` and enabling native browser multilingual display via SVG `<switch>` and `systemLanguage`.

**Blocked by:** 03: OBS Streaming Overlays Pipeline (Experience Mode), 04: Dashboard Widgets and Power BI DAX Pipeline (Operate Mode).

**Status:** closed

- [x] Linter script updated with rule checking that text is authored as `<text>` nodes rather than outlined paths
- [x] Agent generates sample multilingual SVG asset demonstrating `<switch>` with `systemLanguage="pt"` and fallback
- [x] Typography remains 100% editable in Inkscape's text tool
- [x] Agent responds and conducts briefings in the user's conversational language while keeping XML tags canonical
