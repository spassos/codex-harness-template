---
name: new-service
description: Scaffold and verify a new Python service repository from this Copier template. The default is an in-memory FastAPI API, with optional PostgreSQL, Redis and Kafka or RabbitMQ. Use for "novo serviço", "novo repositório", "scaffold", "criar projeto", "bootstrap".
---

# New service

1. Use the inputs already provided. Ask for the project name if missing. Default to Python 3.13,
   `../<slug>` as the destination, and the in-memory profile. Enable integrations requested for
   the service. Use Copier's defaults for the description and owning team unless provided.
2. Render from the template checkout using its locked Copier CLI:
   ```bash
   uv run --locked copier copy --defaults --vcs-ref=HEAD -d project_name="<name>" . "<target-dir>"
   ```
   Pass any provided `description`, `author_name` or `python_version` with `-d`. Add
   `-d use_postgres=true`, `-d use_redis=true` or `-d event_broker=kafka` /
   `-d event_broker=rabbit` only as selected. Outside this checkout, use `uvx copier copy`
   with `gh:spassos/codex-harness-template` as the source.
3. In the generated repository, run `make bootstrap` and `make check`. Integration profiles
   require a running Docker daemon for their tests. If a step fails, investigate the environment
   and dependencies before attributing the failure to the template.
4. Once validation passes, create the initial local commit:
   `git add -A && git commit -m "chore: scaffold from codex-harness-template"`.
5. Report the generated profile, the checks run, and how to start the app. The in-memory profile
   starts with `make run`. For infrastructure profiles, follow the generated README.
