# 02: Interactive Briefing Module (`ask_question` Protocol)

**What to build:** The interactive briefing protocol within SVG Maestro, prompting the user with a structured, multi-choice interview via `ask_question` across 4 core vector dimensions (Surface Viewport, Mode, Motion Profile, Handoff Target) and synthesizing the constraints into a binding `BRIEF.md` prior to code generation.

**Blocked by:** None (can start immediately).

**Status:** closed

- [x] Automated routine triggers `ask_question` whenever a design request lacks core dimensions
- [x] Multiple-choice options provide recommended defaults for Surface Viewport, Surface Mode, Motion Profile, and Handoff Target
- [x] Agent conducts interview in the user's conversational language (e.g. Portuguese or English)
- [x] Briefing generates a structured `BRIEF.md` capturing all agreed constraints
- [x] Subsequent generation passes read `BRIEF.md` as the authoritative source of design truth
