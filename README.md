# codex-harness-template

Template ([Copier](https://copier.readthedocs.io)) que gera repositórios Python prontos para um
**ways of working de engenharia agêntico com o OpenAI Codex**: do *discovery* do produto até a
verificação automática em produção.

Você responde algumas perguntas (nome, Postgres? Redis? Kafka/RabbitMQ?) e recebe um serviço
com código de referência, testes, gates de qualidade/segurança, CI/CD e a camada agêntica do
Codex (`AGENTS.md`, skills por fase do SDLC, subagents e review no PR) já configurados.

## Gerar um novo repositório

```bash
# Interativo
uvx copier copy gh:spassos/codex-harness-template meu-servico

# Não interativo
uvx copier copy --defaults gh:spassos/codex-harness-template meu-servico \
  -d project_name="Orders Service" -d use_postgres=true -d use_redis=true -d event_broker=kafka

cd meu-servico && make setup && make check
```

Com o Codex (agente de scaffolding): abra este repositório no `codex` e peça
`$new-service` (ou "crie um novo serviço de pedidos com Postgres e Kafka"). A skill faz a
entrevista, renderiza o template, roda `make check` no resultado e sugere começar o `$discovery`.

Atualizar um projeto já gerado quando o template evoluir: `uvx copier update` dentro dele.

## O que vem configurado

| Área | Escolha (não reinventar a roda) |
|---|---|
| Arquitetura | Hexagonal (ports & adapters), camadas verificadas por **import-linter** |
| Pacotes / Python | **uv** (lockfile, `uv sync --locked`), `.python-version` |
| Lint / PEP 8 / PEP 257 | **Ruff** (lint + format, regras pycodestyle, pydocstyle, bugbear, bandit, complexidade ≤ 8...) |
| Tipos | **mypy --strict** + plugin pydantic |
| Testes | **pytest**, cobertura mínima, **testcontainers** (infra real), **respx**, FastStream TestBroker |
| Segurança | **pip-audit** (lockfile completo), Ruff `S`, **gitleaks**, **zizmor**, **Trivy**, Dependabot, actions fixadas por SHA |
| API (entrada/saída HTTP) | **FastAPI**, pydantic, health `live`/`ready`, `X-Request-ID` |
| Banco | **PostgreSQL** · SQLAlchemy Core async · asyncpg · **Alembic** *(opcional)* |
| Cache | **Redis** cache-aside *(opcional)* |
| Eventos (entrada/saída) | **FastStream** com **Kafka** ou **RabbitMQ**: publisher + worker consumidor *(opcional)* |
| APIs externas | **httpx** com timeouts + **stamina** (retry só para falhas transitórias) |
| Observabilidade | **structlog** (JSON fora do local) + correlation id |
| Config | **pydantic-settings** (`APP_*`, `SecretStr`), `.env.example` |
| Local | `compose.yaml` (app, worker, migrações, infra) + `Makefile` como interface única |
| CI | lint, tipos, arquitetura, testes + integração, auditoria, segredos, scan da imagem, título Conventional Commit |
| CD | imagem no GHCR com *provenance attestation* → staging → produção (aprovação) → **smoke test confirma o SHA no ar** → rollback automático |
| Release | **release-please** (semver + CHANGELOG) |
| Codex | `AGENTS.md`, `.codex/config.toml`, subagents (`architect`, `test_engineer`, `reviewer`, `security_auditor`), skills (`$discovery`, `$specify`, `$plan`, `$implement`, `$integrate`, `$review`, `$ship`), review de PR com `openai/codex-action` |

## SDLC agêntico no projeto gerado

```
Discovery ─► Specify ─► Plan ─► Implement ─► Review ─► Ship ─► produção verificada
$discovery   $specify   $plan    $implement   $review   $ship
PRD          spec.md    plan.md  TDD +        reviewer + PR → CI → CD
docs/product ACs        ADRs     make check   security   smoke test
```

Cada fase gera um artefato versionado e tem um gate humano. Detalhes em
[`template/docs/ways-of-working.md`](template/docs/ways-of-working.md) e as regras para
agentes em [`template/AGENTS.md.jinja`](template/AGENTS.md.jinja).

## Desenvolvendo o template

```bash
uv sync
uv run pytest            # renderiza 4 cenários e valida a estrutura (segundos)
uv run pytest -m slow    # + `make check` completo em cada projeto gerado (precisa de Docker)
```

Leia [`AGENTS.md`](AGENTS.md) antes de alterar o template.
