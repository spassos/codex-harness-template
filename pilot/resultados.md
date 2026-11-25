# Tarefas e evidências da segunda etapa

| Tarefa | Estado | Evidência |
|---|---|---|
| Tornar CD e releases opt-in e deixar as permissões do Codex a cargo do time | Implementada e validada localmente | As quatro combinações dos controles passaram nos testes. Os quatro projetos gerados passaram no `make check`. Os workflows foram verificados com actionlint e zizmor. |
| Comparar o Codex com e sem orientação do projeto | Executor e avaliador implementados; coleta pendente | Matriz balanceada com 12 posições. Todos os arquivos compartilhados dos pacotes têm o mesmo conteúdo, incluindo o lockfile. Os dois testes reservados falharam no projeto inicial e passaram numa implementação de referência descartável. |

## Execução de 25 de novembro de 2026

**0 de 12 sessões iniciadas.** O workflow da revisão `de7e65fa23ec4bc013a1eab0b821e8ff6c818eb6`
parou em `Verify pilot credentials`, antes de distribuir as tarefas. O job de preparação
requer o segredo de Actions `OPENAI_API_KEY`. Na alternativa local, o Codex CLI recebeu
HTTP 401 e solicitou um novo login. [Execução no GitHub Actions](https://github.com/spassos/codex-harness-template/actions/runs/45610708039)

Na mesma revisão, a preparação local gerou três repetições para cada combinação de tarefa
e condição. Os 71 arquivos comuns aos dois pacotes tinham conteúdo idêntico, incluindo o
lockfile. A condição com orientação acrescentou 17 arquivos de instruções, skills e agentes.
O projeto de controle passou no `make check`, com 22 testes aprovados. Os dois testes de
aceitação reservados falharam no projeto inicial, como esperado antes das alterações.

A comparação de acertos, tempo, tokens e intervenções aguarda as sessões e a revisão cega
dos diffs. Para retomar a mesma revisão após configurar o segredo, reexecute todos os jobs
da execução vinculada acima.

As tarefas estão registradas no GitHub: [controles de entrega](https://github.com/spassos/codex-harness-template/issues/2) e [piloto do Codex](https://github.com/spassos/codex-harness-template/issues/3). O [roteiro](README.md) descreve a coleta, a revisão cega e
a exportação dos resultados.
