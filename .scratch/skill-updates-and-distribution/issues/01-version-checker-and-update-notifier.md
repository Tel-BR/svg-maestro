# 01: Verificador de Versões e Notificador de Atualizações (CLI/Script)

**What to build:** A standalone Python module and CLI check that detects when a newer release of SVG Maestro exists on GitHub (`https://api.github.com/repos/Tel-BR/svg-maestro/releases/latest`). It uses a 24-hour local cache (in a hidden JSON file or user cache directory) to avoid hitting GitHub API rate limits. When invoked or imported, it compares the current semver (from `SKILL.md` or package constants) against the remote release. If a newer version is found, it renders a clean, non-intrusive console notice informing the user how to update. The module must be resilient to network failures and timeouts without halting caller execution.

**Blocked by:** None (can start immediately)

**Status:** completed

- [x] Core module `scripts/update_notifier.py` implementing `check_for_updates(current_version, force=False)` with 24-hour caching.
- [x] CLI flag `--check-update` added to `scripts/validate_svg.py` and `scripts/refinement_verbs.py` (or executable directly via `python scripts/update_notifier.py`).
- [x] Unit tests in `tests/test_update_notifier.py` covering cache hits, cache expiration, network error handling/timeouts, and update banner formatting with mocked GitHub responses.
- [x] All tests passing under pytest without network calls during CI.
