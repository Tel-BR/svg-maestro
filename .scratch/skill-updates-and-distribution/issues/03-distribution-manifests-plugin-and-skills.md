# 03: Manifestos de Distribuição para Registros de Skills (plugin.json e skills.json)

**What to build:** Native package manifests making SVG Maestro discoverable, installable, and auto-updatable via standard agent package ecosystems (Claude Code `/plugin marketplace add Tel-BR/svg-maestro` and `npx skills add Tel-BR/svg-maestro`).

**Blocked by:** 01: Verificador de Versões e Notificador de Atualizações (CLI/Script)

**Status:** completed

- [x] Create `.claude-plugin/plugin.json` (or root `plugin.json`) with plugin metadata, name, version (`0.1.0-beta.1`), author, description, and repository schema matching Claude Code marketplace conventions.
- [x] Create `skills.json` (or package configuration) adhering to the `npx skills` registry specification.
- [x] Ensure version fields across `SKILL.md`, `plugin.json`, and Python scripts are centralized or documented in synchronization.
- [x] Automated validation test checking JSON schema compliance and version parity across manifests.
