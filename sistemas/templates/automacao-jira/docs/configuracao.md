# Configuração da integração

[← Sumário](../README.md)

Configure estes valores nas Actions do repositório ou da organização, conforme a [instalação](instalacao.md).

## Secrets

| Nome | Conteúdo |
|---|---|
| `JIRA_USER_EMAIL` | Conta da integração com acesso às issues envolvidas |
| `JIRA_API_TOKEN` | Token da conta com permissão para consultar, transicionar e comentar |

Não conceda administração à conta apenas para executar o script. Restrinja acesso aos projetos necessários. O script não imprime credenciais nem corpos de respostas HTTP e recusa redirecionamentos autenticados.

Use `JIRA_BASE_URL` como variable, pois ela aparece nos links de rastreabilidade. O workflow aceita o secret homônimo como compatibilidade com instalações anteriores; nesse caso o mascaramento do GitHub pode afetar a exibição dos links.

## Actions Variables

Os valores numéricos abaixo são exemplos, não IDs universais.

| Nome | Exemplo | Finalidade |
|---|---|---|
| `JIRA_BASE_URL` | `https://org.atlassian.net` | Origem HTTPS do Jira, sem `/browse`, caminho do board ou credenciais |
| `JIRA_PREFIXOS` | `PROJ,OPS` | Chaves de projetos autorizadas, separadas por vírgula |
| `JIRA_TIPOS_BRANCH` | `feat,feature,bugfix,fix,hotfix,chore,docs,refactor,test,perf,ci,build` | Tipos autorizados; usa esta lista se omitida |
| `JIRA_STATUS_INICIAIS` | `10000,10001` | IDs de A Fazer/Backlog que autorizam o início |
| `JIRA_STATUS_FAZENDO` | `10002` | ID do status de implementação |
| `JIRA_STATUS_ANALISE` | `10003` | ID do status de revisão |
| `JIRA_STATUS_FEITO` | `10004` | ID do status concluído |
| `JIRA_TRANSITION_ID_INICIO` | `11` | Transição para Fazendo |
| `JIRA_TRANSITION_ID_ANALISE` | `21` | Transição para Em análise |
| `JIRA_TRANSITION_ID_CONCLUSAO` | `31` | Transição para Feito |
| `JIRA_CAMPO_CONCLUSAO` | `customfield_12345` | Campo que autoriza a conclusão global |
| `JIRA_VALOR_CONCLUSAO` | `Liberado` | Valor exato que libera a conclusão, sensível a maiúsculas/minúsculas |

**Status e transição são entidades diferentes.** Consulte `GET /rest/api/3/issue/{key}?fields=status` para o status atual e `GET /rest/api/3/issue/{key}/transitions` para os IDs disponíveis e seus destinos. Consulte `GET /rest/api/3/field` para identificar campos. O script confirma que a transição configurada está disponível e leva ao status esperado.

Todas as issues autorizadas por uma instalação devem compartilhar este mapeamento de workflow. Se projetos tiverem workflows diferentes, configure integrações separadas ou adicione um mapeamento por projeto antes de incluí-los em `JIRA_PREFIXOS`. Não autorize prefixos de outros workflows com IDs incompatíveis.

IDs de status distintos representam as etapas. Um ID de transição configurado precisa estar disponível nas origens autorizadas; se o workflow usar transições distintas por origem, adapte esse mapeamento ou configure uma transição adequada no Jira. Nunca coloque Em análise/Feito em `JIRA_STATUS_INICIAIS` para contornar uma falha.
