# AGENTS.md — codex-harness-template

This repository ships the **codex-scaffold CLI**. It uses Copier to generate Python services
with a project-scoped SDLC for Codex. The CLI entry point lives in `src/codex_scaffold/cli.py`.

- `copier.yml` — questions. `template/` — everything rendered into new projects (`*.jinja` files
  are rendered; conditional files/dirs use `{% if ... %}name{% endif %}`).
- `.agents/skills/new-service/` — skill that scaffolds a new service (`$new-service`).
- `tests/test_template.py` — renders five scenarios and checks their layout. Use `-m smoke`
  for CLI generation and a live HTTP smoke test. Use `-m slow` for `make check` in each
  generated project (Docker for integration scenarios).

## Rules when changing the template
- Generated code must pass its own gates for **every** scenario: `uv run pytest -m slow`.
  Watch Jinja whitespace (`{%-`): ruff format/isort failures usually come from it.
- Keep generated projects lean: prefer standard library and already-chosen libraries
  (template/docs/adr/0002). New option in `copier.yml` ⇒ new scenario in `tests/test_template.py`.
- Workflows in `template/.github/workflows` pin actions by commit SHA and use least privilege;
  validate with `uvx zizmor --offline template/.github/workflows` and actionlint.
- Agent-facing files (AGENTS.md, skills, subagents) are English; human docs are Portuguese.
