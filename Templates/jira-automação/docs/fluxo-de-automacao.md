# Fluxo da automação

[← Sumário](../README.md)

A chave vem exclusivamente de `<tipo>/<prefixo>-<numero>-<descricao-em-kebab-case>`, por exemplo `feature/proj-42-validar-acesso`. Prefixos são configurados como uma lista, sem diferenciar maiúsculas/minúsculas. Uma branch deve conter uma única chave autorizada. Não há consultas ao GitHub para descobrir a issue.

| Evento | Origem permitida | Ação |
|---|---|---|
| Push que cria uma branch | IDs em `JIRA_STATUS_INICIAIS` | Avançar para Fazendo |
| PR aberto, reaberto ou pronto para revisão | Status iniciais ou Fazendo | Avançar para Em análise |
| PR fechado com merge | Em análise + liberação explícita | Avançar para Feito |
| Status já no destino | Qualquer evento compatível | Registrar o evento sem repetir a transição |
| Card avançado, encerrado, bloqueado ou fora das origens permitidas | Qualquer evento | Preservar status e registrar a frente |

Um push atrasado do back-end não devolve para Fazendo um card já Em análise pelo front-end. PR em rascunho, fechamento sem merge e PR de fork externo não executam o job. Se um PR já estava Em análise e volta a rascunho, este template preserva o status; configure uma regra própria se o projeto exigir outro comportamento.

Cada evento processado tenta adicionar um comentário no Jira com repositório, branch, resultado, PR e execução. O resumo da execução no GitHub recebe a chave e o link do Jira. Inclua também o link da issue no corpo do PR e mantenha a integração nativa Jira/GitHub, se disponível.

Consulte [Configuração](configuracao.md) para o mapeamento dos IDs e [Conclusão entre repositórios](conclusao-multirrepositorio.md) para a liberação final.
