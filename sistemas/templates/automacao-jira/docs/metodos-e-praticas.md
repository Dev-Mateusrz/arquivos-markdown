# Métodos e práticas

[← Sumário](../README.md)

Os [modelos de issue](../arquivos/issues-jira.md) aplicam estas orientações a bugs, tarefas e investigações. A [conclusão entre repositórios](conclusao-multirrepositorio.md) detalha a trava final.

| Conceito do estudo | Aplicação neste conjunto |
|---|---|
| Valor antes da solução | Modelo B abre com valor, persona e capacidade esperada |
| BDD e aceite negativo | Modelos descrevem Dado/Quando/Então, falhas e autorização na API/interface |
| Contrato antes do código | Schema/interface, erros, compatibilidade e acordo entre frentes na issue |
| DoR sistêmica | Configurar campos próprios e validadores antes de entrar em A Fazer e iniciar |
| Evidências automatizadas | PR registra comando/resultado e liga jobs/artefatos dos testes relevantes |
| Revisores por CODEOWNERS | Configurar `.github/CODEOWNERS` nas branches base e exigência de revisão nas proteções do projeto |
| Limpeza de ambientes efêmeros | Workflow de infraestrutura trata `pull_request: closed`, com ou sem merge, usando o identificador do ambiente do PR |
| DORA | Pipeline de deploy registra SHA, ambiente, horário e resultado para correlacionar commit → produção |

CODEOWNERS solicita revisão quando o PR fica pronto para revisão; essa responsabilidade não pertence à transição de fechamento do Jira. Limpeza e publicação de métricas dependem da infraestrutura e da plataforma de observabilidade do projeto: devem ser integradas nos respectivos pipelines, com permissões próprias. Este template não remove ambientes nem escreve métricas de produção.

## Definition of Ready sistêmica

A descrição orienta pessoas e IAs; campos e validadores do workflow aplicam a regra. Use campos próprios para **Critérios de aceite**, **Testes esperados**, **Escopo por repositório** e **Contrato/decisão** quando houver validação sistêmica. Eles são a fonte validada; a descrição pode apontar para eles para evitar duplicação.

| Momento | Regra a configurar no Jira |
|---|---|
| Entrada em A Fazer | Impedir a transição com critérios de aceite ou testes esperados vazios; rejeitar conteúdo ainda não preenchido pela política de revisão |
| Início da implementação | Exigir escopo, dependências resolvidas e contrato acordado quando houver integração; exceções devem ter justificativa |
| Conclusão | Validar evidências, frentes envolvidas e ausência de bloqueios; exigir liberação explícita do campo de conclusão |
| Reabertura ou nova frente | Revogar a liberação de conclusão antes de retomar o trabalho |

As capacidades de validação dependem do tipo de projeto e workflow. Se a instância não suportar o validador necessário, registre a limitação e mantenha a verificação humana explícita. Uma automação que devolve a issue após a transição é corretiva: ela não impede a transição original.

## Evidência de entrega e métricas

**Change lead time (DORA)** mede o intervalo entre o commit no controle de versão e sua disponibilização em produção. Issue criada → Feito é uma métrica de fluxo do trabalho; abertura de PR → merge mede outra janela. Nenhuma delas substitui o evento de deploy em produção.

Antes de iniciar, defina como cada deploy referencia os commits e PRs e como o resultado em produção será observado. O pipeline de deploy deve fornecer ambiente, versão/SHA, horário e resultado. A automação deste diretório registra rastreabilidade; não calcula métricas DORA e não considera merge uma evidência de deploy.
