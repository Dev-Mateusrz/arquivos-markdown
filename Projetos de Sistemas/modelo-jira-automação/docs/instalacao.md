# Instalação e adaptação

[← Sumário](../README.md)

1. Copie [jira.py](../arquivos/jira.py) para `.github/workflows/scripts/jira.py` em cada repositório participante, sem editar o código por projeto.
2. Copie o [workflow](../arquivos/jira-automation.yml) para `.github/workflows/jira-automation.yml`. Substitua `{{BRANCH_DESENVOLVIMENTO}}` e `{{BRANCH_PRODUCAO}}` pelos nomes reais; se houver uma única branch de entrega, mantenha apenas ela nas listas. Adicione outras branches de entrega, se necessário.
3. Configure os secrets e variables descritos em [Configuração](configuracao.md), em Settings → Secrets and variables → Actions. Variáveis organizacionais podem ser compartilhadas quando o mapeamento do Jira for o mesmo.
4. Configure as [regras sistêmicas](metodos-e-praticas.md#definition-of-ready-sistêmica) e a [liberação de conclusão](conclusao-multirrepositorio.md) no Jira. Valide com uma issue de teste conforme [Operação e validação](operacao-e-validacao.md#verificação-local).
5. Disponibilize o script na branch padrão e nas bases dos PRs antes de ativar a automação. O checkout lê o script dessas referências para evitar executar código da branch de trabalho com secrets.
6. Use [issues-jira.md](../arquivos/issues-jira.md) como fonte dos modelos e alinhe as instruções do projeto a ele. Outros diretórios de templates deste repositório podem conter fluxos Jira diferentes; escolha um único responsável pela sincronização, evitando duas automações sobre a mesma issue.

O workflow usa runner hospedado `ubuntu-latest` e `actions/checkout@v7`. Para runner próprio ou GitHub Enterprise Server, confira compatibilidade e ajuste a versão da action. O script requer Python 3.10 ou superior e usa autenticação básica por e-mail/token para Jira Cloud.
