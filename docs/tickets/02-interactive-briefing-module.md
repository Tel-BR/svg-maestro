# 02: Interactive Briefing Module (`ask_question` Protocol)

**What to build:** The interactive briefing protocol within SVG Maestro, prompting the user with a structured, multi-choice interview via `ask_question` across 4 core vector dimensions (Surface Viewport, Mode, Motion Profile, Handoff Target) and synthesizing the constraints into a binding `BRIEF.md` prior to code generation.

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

- [ ] Automated routine triggers `ask_question` whenever a design request lacks core dimensions
- [ ] Multiple-choice options provide recommended defaults for Surface Viewport, Surface Mode, Motion Profile, and Handoff Target
- [ ] Agent conducts interview in the user's conversational language (e.g. Portuguese or English)
- [ ] Briefing generates a structured `BRIEF.md` capturing all agreed constraints
- [ ] Subsequent generation passes read `BRIEF.md` as the authoritative source of design truth
