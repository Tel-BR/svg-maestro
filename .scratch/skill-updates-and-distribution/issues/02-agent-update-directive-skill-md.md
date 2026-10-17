# 02: Diretiva de Atualização e Autodiagnóstico no SKILL.md

**What to build:** An update awareness protocol inside `SKILL.md` (and child skills such as `skills/ask-maestro/SKILL.md`) that guides agents (Antigravity and Claude Code) to autonomously diagnose out-of-date installations when initiated, and offer upgrade instructions politely to the user without breaking user flow.

**Blocked by:** 01: Verificador de Versões e Notificador de Atualizações (CLI/Script)

**Status:** ready-for-agent

- [ ] `SKILL.md` updated with an explicit "Lifecycle & Version Management" section instructing the agent how and when to check for updates (`scripts/update_notifier.py`).
- [ ] Clear agent guidelines on informing the user cordially if a newer release exists, supplying copy-paste update commands (`git -C <path> pull`).
- [ ] Child skill `skills/ask-maestro/SKILL.md` aligned with the same versioning and discovery protocol.
- [ ] Integration validation verifying that the agent protocol instructions adhere to project craft floor standards and CONTEXT.md architectural rules.
