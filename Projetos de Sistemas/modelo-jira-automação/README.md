# Automação Jira + GitHub

Templates reutilizáveis para integrar Jira e GitHub. Use os guias conforme a etapa de implantação ou a dúvida a resolver.

## Documentação

| Guia | Conteúdo |
|---|---|
| [Instalação e adaptação](docs/instalacao.md) | Arquivos a copiar, pré-requisitos e adoção em um projeto |
| [Configuração da integração](docs/configuracao.md) | Secrets, variables, IDs de status e transições |
| [Fluxo da automação](docs/fluxo-de-automacao.md) | Convenção de branches, eventos e regras de avanço |
| [Conclusão entre repositórios](docs/conclusao-multirrepositorio.md) | Liberação global, impedimentos e concorrência |
| [Métodos e práticas](docs/metodos-e-praticas.md) | BDD, contratos, DoR, evidências, revisão e métricas |
| [Operação e validação](docs/operacao-e-validacao.md) | Best-effort, recuperação e verificações locais e reais |
| [Referências](docs/referencias.md) | Estudo de caso e documentação de apoio |

## Templates e código

| Arquivo | Finalidade |
|---|---|
| [issues-jira.md](arquivos/issues-jira.md) | Modelos de bug, tarefa e investigação |
| [jira.py](arquivos/jira.py) | Script de integração com Jira Cloud |
| [jira-automation.yml](arquivos/jira-automation.yml) | Workflow do GitHub Actions |
| [test_jira.py](arquivos/test_jira.py) | Testes locais com API simulada |
