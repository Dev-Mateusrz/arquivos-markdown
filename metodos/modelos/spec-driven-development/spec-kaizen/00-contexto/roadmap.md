# Roadmap de entregas do produto

Status: capacidades e regras gerais definidas; catálogo de quatro projetos e checklist de IA recebidos.

Este documento trata da evolução do Kaizen. A organização e as regras do aprendizado estão na [visão do produto](visao-produto.md); o catálogo de estudo e prática está no [material de referência Front-end](referencias/roadmap-frontend.md).

## Primeira entrega

**Objetivo:** permitir ao ponto focal organizar o próprio percurso de estudos e acompanhar separadamente o estudo e a prática necessários para concluir os tópicos.

- Criar áreas de atuação, tópicos e conteúdos, com um roadmap por área.
- Organizar os tópicos em fases de aprendizado, inicialmente Base, Profissional e Especialização, permitindo ajustar essa organização.
- Marcar os conteúdos estudados e visualizar quantidade e percentual de estudo e cobertura prática por tópico, fase e roadmap.
- Avaliar opcionalmente facilidade ou dificuldade, podendo alterar ou remover a avaliação, e filtrar conteúdos com base nessa percepção.
- Consultar projetos do roadmap, identificar conhecimentos necessários e conteúdos abordados e acompanhar os critérios do resultado esperado.
- Registrar o andamento dos projetos, confirmar manualmente sua conclusão e incluir links ou observações opcionais.
- Concluir os tópicos somente após completar o estudo e a prática de todos os seus conteúdos.

As fórmulas, a confirmação dos resultados e a relação entre conteúdos e projetos são definidas na [visão do produto](visao-produto.md#cálculo-do-progresso).

## Conteúdo inicial

O roadmap de Desenvolvimento Frontend terá como base os quinze tópicos já fornecidos, preservando seus nomes e ordem na [lista de referência](visao-produto.md#roadmap-de-referência--desenvolvimento-frontend).

Distribuição inicial dos tópicos nas fases, ajustável pelo usuário:

| Fase | Números dos tópicos na lista de referência |
| --- | --- |
| Base | 1 e 2 |
| Profissional | 3, 4, 5, 6, 7, 8, 9, 12, 14 e 15 |
| Especialização | 10, 11 e 13 |

O tópico 15 já possui 65 itens fornecidos, todos sem marcação de conclusão no material recebido. Seu conteúdo e a prioridade de estudo estão no [checklist de IA](referencias/roadmap-frontend.md#15-inteligência-artificial-aplicada-ao-desenvolvimento-front-end). O estudo é transversal às práticas, mantendo a organização do tópico na fase Profissional.

Os conteúdos dos tópicos 1 a 14 serão cadastrados pelo usuário. Tópicos sem conteúdos mostram essa ausência e 0% de progresso.

## Catálogo inicial de projetos

Os quatro projetos recebidos estão reunidos no [catálogo Front-end](referencias/roadmap-frontend.md#projetos-progressivos), com progressão de Base para Profissional e Especialização. Os critérios de conclusão foram estruturados a partir das entregas descritas pelo ponto focal.

No cadastro, cada projeto será associado aos conteúdos concretos que aborda. A lista de tópicos do catálogo orienta essa associação, sem validar a prática automaticamente. Os checklists de critérios são modelos e não indicam projetos já concluídos pelo usuário.

## Evoluções posteriores

Novas entregas serão definidas conforme as necessidades identificadas durante o uso. As definições atuais orientam a especificação das funcionalidades da primeira versão.

## Próximo passo de especificação

As três funcionalidades iniciais estão detalhadas em spec.md na [ordem de trabalho do índice](../README.md#funcionalidades-em-ordem): organização dos estudos, progresso e avaliação, projetos e validação prática. As specs são rascunhos para revisão.

O próximo passo é revisar a feature 001 e, então, seguir Plan → Tasks → Implement, com revisão do usuário entre as etapas. As decisões técnicas compartilhadas serão registradas em 01-arquitetura durante o planejamento. O conteúdo disponível e o tratamento dos vínculos permanecem na [visão do produto](visao-produto.md#situação-do-conteúdo-e-vínculos).
