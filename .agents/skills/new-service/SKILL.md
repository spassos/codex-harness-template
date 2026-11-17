---
name: new-service
description: Scaffold a new Python service repository from this Copier template — interview for name and integrations (PostgreSQL, Redis, Kafka/RabbitMQ), render it, verify it passes `make check`, and start discovery. Use for "novo serviço", "novo repositório", "scaffold", "criar projeto", "bootstrap".
---

# New service (scaffolding agent)

1. Ask (one round, offer defaults): product/service name, one-sentence description, owning team,
   Python version (3.12/3.13/3.14, default 3.13), PostgreSQL? Redis? event broker
   (none/kafka/rabbit), target directory (default `../<slug>`). Infer integrations from the
   description when obvious and confirm.
2. Render without prompts:
   ```bash
   uvx copier copy --defaults --vcs-ref=HEAD \
     -d project_name="<name>" -d description="<desc>" -d author_name="<team>" \
     -d python_version=<ver> -d use_postgres=<true|false> -d use_redis=<true|false> \
     -d event_broker=<none|kafka|rabbit> \
     . <target-dir>
   ```
   (From outside this repo use `gh:spassos/codex-harness-template` as source.)
3. Verify in `<target-dir>`: `make setup` then `make check` (Docker must be running for the
   integration tests). Any failure is a template bug — report it, do not patch the output by hand.
4. Initial commit: `git add -A && git commit -m "chore: scaffold from codex-harness-template"`.
5. Hand over: summarize what was generated (integrations, commands, CI/CD setup steps from
   `docs/ways-of-working.md#entrega-cicd`) and suggest starting `$discovery` inside the new repo.
