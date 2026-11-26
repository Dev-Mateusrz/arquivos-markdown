# 003 — Projetos e validação prática

Status: Specify — rascunho para revisão. Os detalhamentos desta spec ainda serão revisados pelo usuário antes de Plan.

## Fontes e dependências

- [Projetos e progressão](../../00-contexto/visao-produto.md#projetos-práticos-e-progressão) e [validação dos conteúdos](../../00-contexto/visao-produto.md#relação-entre-projetos-e-prática-dos-conteúdos).
- [Quatro projetos e critérios iniciais](../../00-contexto/referencias/roadmap-frontend.md#projetos-progressivos).
- [Glossário](../../00-contexto/glossario.md).
- Depende de [001 — Organização dos estudos](../001-organizacao-dos-estudos/spec.md) e integra os indicadores de [002 — Progresso e avaliação](../002-progresso-e-avaliacao/spec.md).

## Objetivo

Organizar os exercícios práticos, explicitar os conteúdos que eles abordam e registrar a confirmação dos resultados para compor a cobertura prática.

Os projetos são dados de aprendizado acompanhados pelo usuário. Esta feature permite gerenciá-los e registrar as entregas.

## Escopo e histórias

- US-003-01: Como usuário, quero consultar e cadastrar projetos com conhecimentos necessários e resultados esperados para escolher minha próxima prática.
- US-003-02: Como usuário, quero associar conteúdos concretos ao projeto para identificar o que será demonstrado.
- US-003-03: Como usuário, quero marcar critérios e confirmar minha entrega para registrar a prática realizada.
- US-003-04: Como usuário, quero corrigir ou reabrir um projeto para que os indicadores reflitam sua situação real.
- Incluir cadastro, edição, ordenação de referência e estados dos projetos; resultados e checklists; vínculos com conteúdos; links e observações opcionais; conteúdo inicial recebido.

## Dados e validações propostas

| Informação | Regra |
| --- | --- |
| Nome | Obrigatório e único no roadmap, ignorando caixa e espaços nas extremidades. |
| Roadmap | Obrigatório; cada projeto pertence a um roadmap. |
| Fase de referência | Obrigatória, escolhida entre as fases do roadmap; indica nível de conhecimento. |
| Objetivo e conhecimentos necessários | Textos obrigatórios que explicam a entrega e a preparação recomendada. |
| Resultado esperado | Texto obrigatório que orienta os critérios de conclusão. |
| Critérios | Pelo menos um, com texto não vazio; sem duplicatas no projeto, ignorando caixa e espaços nas extremidades. |
| Conteúdos abordados | Seleção de itens cadastrados no mesmo roadmap; pode ficar pendente no cadastro, mas exige pelo menos um item antes de confirmar a conclusão. |
| Links e observações | Opcionais; uma URL informada deve ter formato válido e usar HTTP ou HTTPS. |

O projeto pode abranger conteúdos de várias fases e tópicos do mesmo roadmap. A fase de referência orienta o percurso e não restringe esses vínculos. A identidade do conteúdo, e não apenas seu título, determina a validação da prática.

## Estados e cálculo

- **Não iniciado:** projeto cadastrado, sem início registrado e com critérios desmarcados.
- **Em andamento:** usuário iniciou o projeto ou marcou algum critério; o estado permanece até confirmação de conclusão.
- **Concluído:** todos os critérios cumpridos, pelo menos um conteúdo vinculado e confirmação manual de que o resultado foi demonstrado.

O avanço do projeto é critérios cumpridos ÷ total de critérios × 100, com peso igual e exibição de quantidade/total e percentual. Cumprir todos os critérios deixa a entrega pronta para confirmação, sem concluir automaticamente o projeto.

## Requisitos

- REQ-003-01: QUANDO o usuário consultar os projetos de um roadmap, O SISTEMA DEVE apresentar nome, fase de referência, conhecimentos necessários, resultado esperado e estado.
- REQ-003-02: QUANDO o usuário cadastrar ou editar um projeto, O SISTEMA DEVE validar os campos e critérios conforme as regras acima e preservar seus dados para correção quando inválidos.
- REQ-003-03: QUANDO selecionar conteúdos abordados, O SISTEMA DEVE permitir identificar fase, tópico e título de cada conteúdo, mantendo cada vínculo único no projeto.
- REQ-003-04: QUANDO for solicitado vínculo com conteúdo de outro roadmap, O SISTEMA DEVE rejeitá-lo e explicar o escopo permitido.
- REQ-003-05: ENQUANTO o projeto estiver sem vínculos concretos, O SISTEMA DEVE apresentar essa pendência e permitir organizar o projeto, mantendo indisponível sua confirmação de conclusão.
- REQ-003-06: QUANDO o usuário iniciar o projeto ou marcar seu primeiro critério, O SISTEMA DEVE registrá-lo como Em andamento e atualizar seu avanço.
- REQ-003-07: QUANDO o usuário marcar ou desmarcar critérios, O SISTEMA DEVE recalcular o avanço e preservar o resultado após recarregar a aplicação.
- REQ-003-08: QUANDO todos os critérios estiverem cumpridos e houver conteúdo vinculado, O SISTEMA DEVE permitir a confirmação manual do resultado, com links e observações opcionais.
- REQ-003-09: QUANDO o usuário confirmar validamente a conclusão, O SISTEMA DEVE registrar o projeto como Concluído, guardar a data da confirmação e validar a prática dos conteúdos explicitamente vinculados.
- REQ-003-10: ENQUANTO faltar critério ou conteúdo vinculado, O SISTEMA DEVE informar o impedimento e manter o projeto sem conclusão.
- REQ-003-11: QUANDO um projeto concluir, O SISTEMA DEVE recalcular a prática e a conclusão dos conjuntos afetados, preservando as marcações de estudo e as avaliações pessoais existentes.
- REQ-003-12: QUANDO vários projetos concluídos abordarem o mesmo conteúdo, O SISTEMA DEVE considerar sua prática uma única vez, conforme a feature 002.
- REQ-003-13: QUANDO o usuário reabrir um projeto concluído, O SISTEMA DEVE devolvê-lo a Em andamento, retirar sua confirmação ativa e recalcular sua contribuição à prática.
- REQ-003-14: QUANDO um critério de projeto concluído for desmarcado, O SISTEMA DEVE reabri-lo e retirar a confirmação ativa, mantendo o critério desmarcado.
- REQ-003-15: QUANDO for alterar critérios, conteúdos abordados ou resultado esperado de projeto concluído, O SISTEMA DEVE exigir sua reabertura antes de salvar essa alteração.
- REQ-003-16: QUANDO o projeto reabrir, O SISTEMA DEVE preservar a prática de conteúdos que continuem validados por outros projetos concluídos.
- REQ-003-17: QUANDO o usuário escolher um projeto fora da ordem sugerida ou com conhecimentos recomendados ainda pendentes, O SISTEMA DEVE permitir o acesso e o início, mostrando a orientação de estudo.
- REQ-003-18: QUANDO a preparação inicial incluir os projetos, O SISTEMA DEVE disponibilizar os quatro projetos e os 24 critérios do material recebido, sem confirmação de conclusão e sem inferir vínculos com todos os conteúdos de um tópico.
- REQ-003-19: QUANDO a aplicação reabrir ou repetir a preparação inicial, O SISTEMA DEVE preservar projetos, vínculos, estados e confirmações existentes, sem duplicar ou sobrescrever o catálogo.
- REQ-003-20: QUANDO uma gravação ou confirmação falhar, O SISTEMA DEVE informar a falha, permitir nova tentativa e manter como válida a última situação confirmada, sem atribuir prática por uma operação não salva.

## Conteúdo inicial e comprovação

Usar os quatro projetos e seus critérios na fonte indicada. Eles iniciam como Não iniciado, com critérios desmarcados. As referências a tópicos ajudam a selecionar os conteúdos concretos; não criam cobertura prática automática. O cadastro pode começar com vínculos pendentes.

A confirmação é do próprio usuário. Código, documentação, configuração e decisões explicadas podem demonstrar conceitos conforme os critérios. As referências opcionais registram evidências e não exigem integração com um serviço externo nesta feature.

Os itens de IA podem ser vinculados aos projetos quando forem realmente abordados. O catálogo não autoriza o Kaizen a executar agentes nem a implementar automaticamente os projetos de aprendizado.

## Critérios de aceite

- CA-003-01 → REQ-003-01/18/19: Disponibilizar os quatro projetos e seus 24 critérios uma única vez, com estados iniciais e dados do usuário preservados após reabrir.
- CA-003-02 → REQ-003-02/03/04: Cadastrar um projeto válido com conteúdos de dois tópicos; rejeitar campos vazios, critérios duplicados, URLs com protocolo indevido e conteúdos de outro roadmap, mantendo dados para correção.
- CA-003-03 → REQ-003-05/08/10: Deixar os vínculos pendentes e cumprir todos os critérios; mostrar avanço dos critérios completo e impedir a conclusão até selecionar conteúdo concreto.
- CA-003-04 → REQ-003-06/07: Marcar um de quatro critérios deve mostrar Em andamento, 1/4 e 25%, preservados após recarregar.
- CA-003-05 → REQ-003-08/09/11: Cumprir todos os critérios e confirmar manualmente deve registrar Concluído e a data, validar somente os conteúdos vinculados e preservar o estado de estudo.
- CA-003-06 → REQ-003-10/17: Iniciar o projeto avançado com estudo pendente deve ser permitido; concluir com critérios pendentes deve ser impedido.
- CA-003-07 → REQ-003-11: Em um tópico com cinco conteúdos estudados, concluir projetos cobrindo apenas três deve resultar em 60% de prática e tópico pendente; cobrir os cinco deve permitir sua conclusão.
- CA-003-08 → REQ-003-12/13/16: Concluir dois projetos que compartilham um conteúdo e reabrir um deles deve manter a prática do item compartilhado, retirando apenas contribuições sem outra confirmação válida.
- CA-003-09 → REQ-003-14/15: Desmarcar um critério de projeto concluído deve reabri-lo; alterar seu resultado, critérios ou vínculos deve exigir reabertura e nova confirmação.
- CA-003-10 → REQ-003-20: Simular falha ao confirmar ou reabrir deve manter o último estado salvo e os indicadores correspondentes, informando o erro e permitindo nova tentativa.

## Fora de escopo

- Construir ou executar os projetos de estudo, agentes de IA, pipelines e publicações descritos no catálogo.
- Avaliação automática ou externa das competências e anexos de arquivos como comprovação.
- Compartilhamento, revisão por terceiros, projetos entre vários roadmaps e exclusão definitiva.
- Alterar automaticamente o estudo de conteúdos ao concluir um projeto.
- Definir stack, armazenamento ou contratos de API nesta etapa.

## Revisão antes de Plan

Revisar campos de cadastro, a exigência de conteúdo vinculado antes de concluir, a edição de projetos concluídos e o fluxo de confirmação. O design deve definir integridade e persistência das alterações, apresentação de erros e atualização consistente dos indicadores.
