# Piloto de desenvolvimento com Codex

O workflow manual **Codex scaffolding pilot** avalia o efeito incremental das instruções,
skills e agentes especializados. O controle mantém o mesmo código, documentação técnica,
configuração de execução e lockfile. A matriz usa três sessões novas para cada combinação
de tarefa e condição, em runners Linux isolados. As tarefas e o roteiro aprovado para a
mudança de contrato ficam em `tasks.json`.

## Execução

No repositório do **template**, configure o segredo de Actions `OPENAI_API_KEY` e execute
o workflow manual na revisão desejada. Isso utiliza a conta de API configurada para até
12 sessões, com limite de 15 minutos por etapa Codex. O workflow não é gerado nos serviços.
A revisão fixada, os parâmetros do modelo e o lockfile permitem reproduzir os insumos.
O tempo inclui a inicialização da Action. O orçamento e o esforço são iguais nas duas condições.

Antes de preparar os projetos, o workflow faz uma chamada à Responses API com o modelo do
piloto e limite de 16 tokens de saída. Essa chamada verifica se o projeto da API consegue
usar o modelo e fica fora da amostra. Para verificar só esse acesso, marque
`check_access_only` ao executar o workflow. Se a API recusar a chamada, o GitHub mostra
o status HTTP e o código de erro na anotação do job `access`.

O job de preparação renderiza uma vez, remove somente os arquivos de orientação no controle
e embaralha os identificadores. Cada executor recebe apenas seu pacote e a tarefa indicada.
A avaliação roda em outra máquina depois de o agente terminar. A aplicação é reconstruída a
partir do pacote original e do diff, incluindo arquivos novos. O avaliador executa os testes
reservados e `make check`. Falhas de autenticação, de instalação e de execução são registradas
separadamente e impedem concluir a comparação. O protocolo não envia respostas humanas durante
a sessão: pedidos adicionais de intervenção contam como resultado da revisão.

## Revisão cega e relatório

Entregue a um revisor somente os artefatos `review-run-*`. Antes de consultar a matriz ou os
logs do CI, registre por identificador o comportamento entregue, regressões, alterações fora de
escopo e pedidos de intervenção. Consulte o diff e a mensagem final. Para a tarefa de nota,
verifique também que os eventos preservam o contrato anterior. Depois revele a correspondência
em `assignment/matrix.json` e agregue por tarefa e condição. Reporte acertos sobre três, falhas,
intervenções solicitadas e realizadas, duração e tokens (quando disponíveis). Use as diferenças
observadas para propor mudanças nas instruções. Com três repetições, o resultado é exploratório.

Os artefatos não incluem transcrições de ferramentas nem credenciais. O relatório desta execução
fica em [resultados.md](resultados.md).

### Alternativa com a sessão autorizada do CLI

Em um controlador execute `uv run --locked python pilot/prepare.py /tmp/pilot-inputs --revision HEAD`.
Guarde a matriz no controlador. Para cada linha, envie somente o tar da condição a uma VM limpa
com a mesma versão de uv, Python e Codex CLI (0.172.0-alpha.2) e a mesma autorização para o modelo.
Extraia o tar e rode `python worker.py <tarefa> <diretório-de-saída>` na raiz extraída. Recolha a saída
com o identificador da matriz. A VM do candidato não recebe o checkout do template, os testes
reservados ou o resultado das outras sessões. Use o mesmo executor para as 12 tentativas.

Em outro runner, extraia o mesmo tar, inicialize Git em `project`, aplique o patch com
`git apply` se houver alterações e execute `uv sync --locked --all-groups`. Rode o caso
`uv run --frozen pytest /caminho/do/avaliador/acceptance.py::test_<tarefa>` e `make check` dentro
de `project`. Registre os códigos de saída separadamente, inclusive quando o primeiro teste falhar.

Para reunir os resultados, baixe os artefatos do run preservando os nomes dos diretórios.
O revisor registra um CSV com cabeçalho
`id,regressions,out_of_scope,interventions_requested,notes`. Anote contagens, inclusive zero,
para cada diff examinado. Depois da revisão, execute
`python pilot/report.py artefatos revisao.csv > resultados.csv`. Campos vazios representam
dados indisponíveis. Agrupe as linhas por tarefa e condição ao atualizar o relatório. O GitHub
disponibiliza o gatilho manual depois que o arquivo do workflow existir na branch padrão.
