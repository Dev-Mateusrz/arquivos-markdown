# Modelos de issue — {{CHAVE_PROJETO_TRACKER}}

> Base reutilizável para qualquer domínio ou quantidade de repositórios. Copie os blocos dos modelos para `docs/JIRA_TAREFAS.md` ou use-os na descrição das issues. Configure os campos e validadores conforme os guias de [configuração](../docs/configuracao.md) e [métodos e práticas](../docs/metodos-e-praticas.md); escrever uma lista na descrição não cria uma trava sistêmica.

## Parâmetros de adaptação

| Placeholder | Significado | Exemplo genérico |
|---|---|---|
| `{{CHAVE_PROJETO_TRACKER}}` | Nome ou chave do projeto | `PROJ` |
| `{{PREFIXO_ISSUE_MAIUSCULO}}` | Prefixo do código da issue | `PROJ` |
| `{{PREFIXO_ISSUE}}` | Prefixo usado na branch; deve constar em `JIRA_PREFIXOS` | `proj` |
| `{{URL_BASE_TRACKER}}` | Origem do Jira seguida de `/browse` | `https://org.atlassian.net/browse` |
| `{{IDIOMA_PADRAO}}` | Idioma de títulos e descrições | `Português` |

As expressões entre colchetes nos modelos são instruções de preenchimento. Substitua-as por dados reais ou por `Não se aplica — [motivo]`. Não é necessário criar modelos diferentes para front-end, back-end, mobile, dados ou infraestrutura: ajuste as linhas de escopo.

## Como escolher o modelo

| Situação | Tipo no Jira | Modelo |
|---|---|---|
| Comportamento observado diverge de uma regra existente | Bug | A — evidência, causa e regressão |
| Nova capacidade, melhoria ou mudança intencional | Tarefa ou História, conforme o projeto | B — valor, contrato e BDD |
| Recorte de uma entrega maior | Subtarefa | B — escopo reduzido e vínculo com a issue pai |
| Investigação ou prova de conceito | Tarefa / Spike, conforme o projeto | C — pergunta, limite e artefato de decisão |

Uma issue representa um resultado verificável. Esse resultado pode exigir vários PRs e repositórios; cada frente deve estar identificada. Separe issues quando houver resultados independentes, não apenas porque o código está em repositórios distintos.

## Campos comuns

- **Título:** resultado ou defeito em uma frase, sem repetir o código gerado pelo Jira.
- **Prioridade:** impacto, urgência, alcance e risco para usuários/operação. Registre complexidade e esforço separadamente; dificuldade técnica sozinha não define prioridade.
- **Responsável:** pessoa ou equipe definida pela política do projeto. Não adivinhe identidades nem fixe um responsável universal no template.
- **Labels:** reutilize categorias existentes que ajudem a filtrar o trabalho.
- **Prazo:** registre quando houver compromisso informado; não invente uma data nem exija nova confirmação se ela já foi fornecida.
- **Relacionamentos:** use vínculos do Jira para dependências, duplicatas e issue pai; inclua links completos no texto quando ajudarem a leitura.

## Modelo A — Bug

<!-- guia: descreva fatos observados. Se a causa ainda não é conhecida, registre "Sob investigação"; não trate uma hipótese como diagnóstico confirmado. -->

````markdown
## Sintoma
- Ambiente e versão/commit: [local, homologação ou produção; versão afetada]
- Impacto: [quem é afetado, alcance, frequência e desde quando]
- Pré-condições e entrada: [dados mínimos anonimizados para reproduzir]
- Passos para reproduzir: [sequência verificável]
- Resultado atual: [saída, erro ou comportamento observado]
- Resultado esperado: [regra existente e sua referência]
- Evidência: [log sanitizado, resposta, captura ou teste que falha]

## Causa
[Confirmada: repositório/componente, premissa incorreta e evidência; ou Sob investigação]

## Fix
[Correção proposta e comportamento existente que deve ser preservado]

## Escopo por repositório
| Repositório/componente | Alteração | Dependência ou contrato afetado |
|---|---|---|
| [org/repo ou componente] | [correção] | [vínculo ou não se aplica] |

## Critérios de aceite
### Cenário: reprodução corrigida
Dado que [as pré-condições do defeito estão presentes]
Quando [a ação que reproduzia o erro é executada]
Então [o resultado esperado é observado]

### Cenário: regressão e borda
Dado que [um caso válido já suportado ou uma entrada de borda]
Quando [a mesma operação é executada]
Então [o comportamento especificado é preservado ou o erro é tratado]

### Cenário: acesso negado, quando aplicável
Dado que [uma identidade sem a permissão necessária]
Quando [ela tenta a operação diretamente pela API/interface disponível]
Então [o acesso é negado e nenhum dado protegido é exposto ou alterado]

## Testes esperados
- Regressão: [teste que reproduz o defeito e passa após a correção]
- Preservação/borda: [comportamentos que precisam continuar válidos]
- Evidência no PR: [comando, resultado e link do job/artefato do pipeline]

## Entrega e observabilidade
[Como detectar a correção em produção, riscos, rollback e sinal de regressão]

## Card relacionado
[{{PREFIXO_ISSUE_MAIUSCULO}}-XX]({{URL_BASE_TRACKER}}/{{PREFIXO_ISSUE_MAIUSCULO}}-XX) — [relação]
````

## Modelo B — Tarefa

<!-- guia: o valor vem primeiro. Contrato e escopo devem abranger todas as frentes; remova apenas cenários que não se apliquem e registre o motivo. -->

````markdown
## Contexto
Para que [valor de negócio ou melhoria mensurável seja alcançado],
como [persona ou consumidor], quero [capacidade necessária].
Problema atual e evidência: [situação que motiva a mudança].

## Objetivo
[Resultado observável, métrica/sinal de sucesso e referência atual quando disponível]

## Área afetada
[Repositórios, componentes, personas e integrações envolvidos; inclua infra/dados/mobile quando aplicável]

## Alinhamento de contrato e arquitetura
- Contrato versionado: [link para OpenAPI, schema, evento, interface ou decisão]
- Entrada e saída: [campos, tipos, obrigatoriedade e exemplos mínimos]
- Erros e autorização: [códigos, regras de acesso e resposta esperada]
- Compatibilidade e evolução: [versão, migração, consumidores existentes]
- Acordo entre frentes: [responsáveis e registro da validação antes de implementar]
[Sem integração: Não se aplica — motivo]

## Escopo sugerido
| Repositório/componente | Entrega desta frente | Dependências | Responsável |
|---|---|---|---|
| [org/repo-a] | [comportamento a construir] | [contrato/issue] | [equipe/pessoa] |
| [org/repo-b, se houver] | [comportamento a construir] | [contrato/issue] | [equipe/pessoa] |
Fora do escopo: [limites necessários para manter o resultado claro].

## Critérios de aceite
### Cenário: fluxo principal
Dado que [a persona atende às pré-condições]
Quando [executa a ação com dados válidos]
Então [obtém o resultado observável que entrega valor]

### Cenário: falha ou entrada inválida
Dado que [ocorre uma falha de dependência ou uma entrada inválida]
Quando [a operação é solicitada]
Então [o erro definido no contrato é apresentado e a consistência é preservada]

### Cenário: acesso negado, quando aplicável
Dado que [a identidade não possui a permissão necessária]
Quando [tenta executar a operação, inclusive diretamente pela API]
Então [o acesso é negado e os dados protegidos permanecem inacessíveis]
E [a interface respeita a mesma regra, se existir]

## Testes esperados
| Frente/camada | Comportamento validado | Tipo de teste | Evidência esperada |
|---|---|---|---|
| [componente] | [cenário BDD, erro, borda ou concorrência] | [unitário/contrato/integração/E2E] | [job/artefato] |
- O PR liga a issue, identifica a frente e informa os comandos e resultados.
- Os testes relevantes rodam no pipeline e publicam evidências acessíveis.
- Se um teste automatizado não se aplicar, registre justificativa e validação alternativa.

## Entrega e métricas
- Produção: [como e em qual ambiente o resultado chega aos usuários]
- Sequência: [ordem entre repositórios, migração, feature flag, rollback]
- Observabilidade: [sinal de sucesso/falha e responsável por acompanhar]
- Rastreio DORA: [como associar commits/PRs ao deploy bem-sucedido em produção]
- Conclusão global: [quem verifica frentes/PRs, bloqueios e libera o campo no Jira]

## Observações técnicas
[Decisões pendentes, risco, dependência e limites; resolver bloqueios antes do início]

## Cards relacionados
[{{PREFIXO_ISSUE_MAIUSCULO}}-XX]({{URL_BASE_TRACKER}}/{{PREFIXO_ISSUE_MAIUSCULO}}-XX) — [relação]
````

## Modelo C — Investigação / Spike

```markdown
## Contexto e valor
Para que [uma decisão ou redução de risco seja possível], investigar [pergunta].

## Pergunta e limite
[Hipótese, alternativas, prazo/timebox acordado e o que não será investigado]

## Escopo
[Repositórios, componentes e fontes de evidência envolvidos]

## Critérios de aceite
Dado que [as alternativas e restrições foram definidas]
Quando [o experimento ou análise for concluído dentro do limite acordado]
Então [um relatório/ADR compara evidências, limitações e recomenda uma decisão]
E [as tarefas de continuidade ficam identificadas, quando necessárias]

## Testes esperados
[Método de validação, dados anonimizados, forma de reproduzir e artefato esperado]

## Entrega
[Link do relatório/ADR, responsáveis pela decisão e vínculo às próximas issues]
```

## Definition of Ready sistêmica

Consulte [Definition of Ready sistêmica](../docs/metodos-e-praticas.md#definition-of-ready-sistêmica) para os campos, validadores e regras por etapa.

## Evidência de entrega e métricas

Consulte [Evidência de entrega e métricas](../docs/metodos-e-praticas.md#evidência-de-entrega-e-métricas) para correlacionar commits, PRs e deploys em produção.

## Regras de escrita e uso por IA

1. Use `{{IDIOMA_PADRAO}}`, fatos verificáveis e links completos. Não invente causa, responsável, contrato, data ou métrica.
2. Descreva aceite com Dado/Quando/Então. Cubra fluxo principal, falha e acesso negado quando houver autorização; ocultar um botão não protege a API.
3. Defina contratos antes do código. Inclua exemplos, erros, compatibilidade e responsáveis pelo acordo, sem impor uma tecnologia universal.
4. Preserve os cabeçalhos estáveis ao integrar buscas ou validadores. O script `jira.py` depende da branch e de campos do Jira, não dos títulos da descrição.
5. Use `<tipo>/{{PREFIXO_ISSUE}}-<id>-<descricao-em-kebab-case>`, uma issue por branch. Vários repositórios podem usar a mesma chave em branches próprias.
6. Ligue issue e PR nos dois sentidos e informe o escopo da frente. Merge de uma frente não encerra a entrega inteira.
7. Crie testes proporcionais ao comportamento e risco. Evidências devem mostrar comando, resultado e versão testada, sem dados sensíveis.
8. Siga a autorização e a política do projeto para criar ou alterar issues. Estes modelos não criam uma exigência universal de aprovação extra.

## Como adaptar

1. Preencha os parâmetros e ajuste tipos/campos aos disponíveis no Jira.
2. Configure a [Definition of Ready](../docs/metodos-e-praticas.md#definition-of-ready-sistêmica) e a [liberação de conclusão](../docs/conclusao-multirrepositorio.md); mantenha a conclusão travada até essa configuração estar pronta.
3. Alinhe referências a estes modelos nos arquivos de instruções do projeto, caso existam (`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md` ou equivalentes).
4. Ajuste as linhas de escopo e as evidências ao projeto, mantendo os mesmos modelos. Não crie uma variante por camada sem necessidade.
5. Remova os comentários de guia e esta seção na cópia de uso. Se mantiver links de apoio, ajuste-os à estrutura de documentação do projeto. Preserve o template genérico neste repositório.
