# 05: Documentação de Ciclo de Vida e Guias de Atualização

**What to build:** Comprehensive, bilingual documentation in `README.md` and `README.pt-BR.md` explaining installation channels (`git clone`, `npx skills`, Claude Code `/plugin`), update workflows, and semver stability guarantees, as well as release guidelines in `CONTRIBUTING.md`.

**Blocked by:** 02: Diretiva de Atualização e Autodiagnóstico no SKILL.md, 03: Manifestos de Distribuição para Registros de Skills (plugin.json e skills.json), 04: Suíte de Retrocompatibilidade e Tolerância a SVGs Legados

**Status:** completed

- [x] Update `README.md` and `README.pt-BR.md` with a new dedicated "Updates & Versioning" section.
- [x] Document one-line update commands for Git (`git -C <path> pull`), `npx skills update`, and `/plugin update`.
- [x] Update `CONTRIBUTING.md` with the release protocol (how to bump version in `SKILL.md`, `plugin.json`, `update_notifier.py`, and draft GitHub release).
- [x] Verify all docs links and formatting across both English and Portuguese versions.
