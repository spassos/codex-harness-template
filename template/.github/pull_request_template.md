## O quê e por quê
<!-- Uma ou duas frases. -->

Spec: `docs/specs/NNN-.../spec.md` · Plano: `.../plan.md` · ADR: <!-- se houver -->

## Critérios de aceite
| AC | Teste |
|---|---|
| AC-1 | `tests/...::test_...` |

## Checklist (Definition of Done)
- [ ] `make check` verde localmente
- [ ] Cada critério de aceite tem teste
- [ ] Contratos (API/eventos/dados) documentados na spec e compatíveis (ou versionados)
- [ ] Migrações reversíveis ou expand/contract
- [ ] Sem segredos/PII em código, logs ou fixtures
- [ ] Docs/ADRs atualizados
- [ ] `$review` executado (reviewer + security_auditor) sem bloqueios

## Riscos e rollout
<!-- Feature flag? Ordem de deploy? Plano de rollback? -->
