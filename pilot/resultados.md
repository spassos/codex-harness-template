# Tarefas e evidências da segunda etapa

| Tarefa | Estado | Evidência |
|---|---|---|
| Tornar CD e releases opt-in e deixar as permissões do Codex a cargo do time | Implementada e validada localmente | As quatro combinações dos controles passaram nos testes. Os quatro projetos gerados passaram no `make check`. Os workflows foram verificados com actionlint e zizmor. |
| Comparar o Codex com e sem orientação do projeto | Coleta bloqueada pelo saldo da API | Os 12 candidatos passaram pela preparação. A etapa do Codex falhou nos 12 e nenhum chegou à avaliação. A verificação isolada da API retornou `credit_balance_exhausted`. |

## Execução de 25 de novembro de 2026

Na primeira tentativa, o workflow da revisão `de7e65fa23ec4bc013a1eab0b821e8ff6c818eb6`
parou em `Verify pilot credentials`, antes de distribuir as tarefas. O job de preparação
requer o segredo de Actions `OPENAI_API_KEY`. Na alternativa local, o Codex CLI recebeu
HTTP 401 e solicitou um novo login. [Primeira tentativa](https://github.com/spassos/codex-harness-template/actions/runs/45610708039/attempts/1)

Na mesma revisão, a preparação local gerou três repetições para cada combinação de tarefa
e condição. Os 71 arquivos comuns aos dois pacotes tinham conteúdo idêntico, incluindo o
lockfile. A condição com orientação acrescentou 17 arquivos de instruções, skills e agentes.
O projeto de controle passou no `make check`, com 22 testes aprovados. Os dois testes de
aceitação reservados falharam no projeto inicial, como esperado antes das alterações.

Após o cadastro do segredo, a segunda tentativa usou a mesma revisão. Os 12 runners
prepararam a aplicação com sucesso. Os 12 falharam em `Apply the requested change`.
O avaliador pulou os testes reservados e o `make check` dos 12 candidatos.
A matriz de correspondência permaneceu fechada. [Segunda tentativa](https://github.com/spassos/codex-harness-template/actions/runs/45610708039/attempts/2)

Uma chamada isolada à Responses API com a mesma configuração de segredo e modelo recebeu
**HTTP 429 (`credit_balance_exhausted`)**. O diagnóstico usou a revisão `2742d16`,
que acrescenta essa checagem antes da distribuição das tarefas. [Diagnóstico de acesso à API](https://github.com/spassos/codex-harness-template/actions/runs/45613326094)

**0 de 12 resultados avaliáveis.** Os testes e a revisão cega dos diffs ainda são
necessários para medir a eficácia das instruções. Quando houver saldo disponível,
execute o workflow com `check_access_only` e, após o sucesso, rode o piloto completo.

As tarefas estão registradas no GitHub: [controles de entrega](https://github.com/spassos/codex-harness-template/issues/2) e [piloto do Codex](https://github.com/spassos/codex-harness-template/issues/3). O [roteiro](README.md) descreve a coleta, a revisão cega e
a exportação dos resultados.
