# Tarefas e evidências da segunda etapa

| Tarefa | Estado | Evidência |
|---|---|---|
| Tornar CD e releases opt-in e deixar as permissões do Codex a cargo do time | Implementada e validada localmente | As quatro combinações dos controles passaram nos testes. Os quatro projetos gerados passaram no `make check`. Os workflows foram verificados com actionlint e zizmor. |
| Comparar o Codex com e sem orientação do projeto | Executor e avaliador implementados; coleta pendente | Matriz balanceada com 12 posições. Todos os arquivos compartilhados dos pacotes têm o mesmo conteúdo, incluindo o lockfile. Os dois testes reservados falharam no projeto inicial e passaram numa implementação de referência descartável. |

A preparação local usou a revisão de entrega `5a2dac74eae6cf966da331251bc1ea54e70ef97b`.
O preflight autenticado do Codex CLI foi bloqueado pelo proxy antes de uma resposta do modelo.
Há **0 de 12 tentativas concluídas**, sem medições de eficácia, consumo ou tempo para comparar.
Os controles do avaliador utilizam alterações de referência e estão fora da amostra.

A abertura de issues foi bloqueada pelo acesso à API do GitHub. As duas tarefas estão registradas
na tabela até a criação das issues. O [roteiro](README.md) descreve a coleta, a revisão cega e
a exportação dos resultados.
