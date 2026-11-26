# 002 — Progresso e avaliação

Status: Specify — rascunho para revisão. Os detalhamentos desta spec ainda serão revisados pelo usuário antes de Plan.

## Fontes e dependências

- [Progresso e conclusão](../../00-contexto/visao-produto.md#cálculo-do-progresso) e [avaliação pessoal](../../00-contexto/visao-produto.md#facilidade-e-dificuldade).
- [Glossário](../../00-contexto/glossario.md).
- Depende de [001 — Organização dos estudos](../001-organizacao-dos-estudos/spec.md).
- A cobertura prática receberá os resultados de [003 — Projetos e validação prática](../003-projetos-e-validacao-pratica/spec.md). Sem projetos concluídos, a cobertura é zero.

## Objetivo

Permitir registrar o estudo de cada conteúdo, avaliar facilidade ou dificuldade e entender o avanço real do tópico, fase e roadmap.

O usuário deve distinguir conteúdos estudados de competências demonstradas na prática. Concluir o checklist não conclui sozinho o tópico.

## Escopo e histórias

- US-002-01: Como usuário, quero marcar e desmarcar conteúdos na lista para registrar o que estudei.
- US-002-02: Como usuário, quero atribuir, alterar ou remover minha avaliação para orientar revisões.
- US-002-03: Como usuário, quero filtrar o percurso por fase e avaliação sem perder a visão do progresso total do escopo.
- US-002-04: Como usuário, quero consultar quantidades, percentuais e conclusão por tópico, fase e roadmap para entender o que ainda falta.

## Regras de cálculo e apresentação

| Indicador | Cálculo no respectivo tópico, fase ou roadmap |
| --- | --- |
| Estudo | Conteúdos estudados ÷ conteúdos cadastrados × 100. |
| Prática | Conteúdos distintos validados por projetos concluídos ÷ conteúdos cadastrados × 100. |

Cada conteúdo tem peso igual. Agregados usam a soma dos conteúdos do escopo. A mesma identidade de conteúdo conta uma vez na prática mesmo quando vários projetos a validam; títulos iguais em tópicos diferentes continuam representando itens distintos.

Exibir quantidade concluída/total e percentual com até duas casas decimais. Usar as contagens exatas para decidir a conclusão, independentemente do arredondamento exibido.

Um tópico só é concluído se tiver conteúdos, todos estudados e todos com prática validada. Uma fase ou roadmap só é concluído se tiver tópicos e todos estiverem concluídos. Um tópico vazio impede a conclusão do seu conjunto até ser preenchido e concluído.

Escopos sem conteúdos exibem 0% e a indicação de ausência de conteúdos. Quando houver 100% de estudo e prática pendente, apresentar essa pendência, mantendo os indicadores separados.

Avaliações são opcionais: Tenho Dificuldade, Tenho Facilidade ou ausência de avaliação, apresentada como Não avaliado. A avaliação não interfere em cálculo, validação prática ou liberdade de percurso.

## Requisitos

- REQ-002-01: QUANDO o usuário marcar ou desmarcar um conteúdo, O SISTEMA DEVE registrar a mudança na própria lista e atualizar os indicadores afetados.
- REQ-002-02: QUANDO uma marcação ou avaliação for confirmada pela gravação, O SISTEMA DEVE preservá-la após recarregar ou reabrir a aplicação, sem exigir salvar um formulário separado para cada item.
- REQ-002-03: QUANDO o usuário avaliar um conteúdo, O SISTEMA DEVE permitir escolher uma das duas avaliações, alterá-la ou removê-la.
- REQ-002-04: QUANDO a avaliação for removida ou nunca tiver sido preenchida, O SISTEMA DEVE apresentar o conteúdo como Não avaliado.
- REQ-002-05: QUANDO o usuário filtrar por fase ou avaliação, O SISTEMA DEVE apresentar os conteúdos correspondentes e permitir remover os filtros.
- REQ-002-06: ENQUANTO houver filtros ativos, O SISTEMA DEVE manter os indicadores do tópico, fase ou roadmap calculados sobre seu conjunto completo de conteúdos, identificando o escopo apresentado.
- REQ-002-07: QUANDO apresentar o progresso, O SISTEMA DEVE mostrar separadamente estudo e prática, com contagens e percentuais conforme as regras acima.
- REQ-002-08: QUANDO não houver conteúdos no escopo, O SISTEMA DEVE mostrar 0% e estado vazio, sem apresentar conclusão.
- REQ-002-09: QUANDO todos os conteúdos de um tópico estiverem estudados e a prática estiver incompleta, O SISTEMA DEVE mostrar o estudo completo e a prática pendente, sem concluir o tópico.
- REQ-002-10: QUANDO todas as condições exatas de conclusão forem satisfeitas, O SISTEMA DEVE apresentar o tópico, fase ou roadmap correspondente como concluído.
- REQ-002-11: QUANDO uma desmarcação, novo conteúdo ou alteração da prática invalidar uma condição, O SISTEMA DEVE recalcular os valores e retirar a conclusão dos conjuntos afetados.
- REQ-002-12: QUANDO vários projetos concluídos validarem o mesmo conteúdo, O SISTEMA DEVE contá-lo uma única vez no respectivo escopo.
- REQ-002-13: QUANDO o usuário mudar a avaliação de facilidade/dificuldade, O SISTEMA DEVE preservar as marcações de estudo e a validade da prática existentes.
- REQ-002-14: QUANDO uma gravação falhar, O SISTEMA DEVE informar a falha, permitir nova tentativa e refletir o último estado confirmado nos indicadores, sem perder silenciosamente a intenção do usuário.
- REQ-002-15: ENQUANTO não houver prática validada pela feature 003, O SISTEMA DEVE apresentar cobertura prática zero e manter pendente a conclusão que dependa dela.

## Critérios de aceite

- CA-002-01 → REQ-002-01/02/07: Em um tópico de cinco conteúdos, marcar três deve mostrar 3/5 e 60% de estudo, mantendo o resultado após recarregar.
- CA-002-02 → REQ-002-07: Em uma fase com tópicos de dois e oito conteúdos, marcar os dois do primeiro deve mostrar 2/10 e 20% no agregado.
- CA-002-03 → REQ-002-03/04/13: Avaliar, alterar e remover a avaliação deve mudar apenas essa percepção e seus filtros, preservando estudo e prática.
- CA-002-04 → REQ-002-05/06: Filtrar um conteúdo com dificuldade em um tópico de cinco itens deve reduzir a lista visível e manter o denominador de cinco nos indicadores desse tópico.
- CA-002-05 → REQ-002-08/15: Tópicos sem conteúdos mostram estado vazio e zero; tópicos sem projetos concluídos mantêm prática zero e não ficam concluídos.
- CA-002-06 → REQ-002-09/10: Com cinco conteúdos estudados e três validados na prática, mostrar 100% de estudo, 60% de prática e pendência de prática; com os cinco validados, concluir o tópico.
- CA-002-07 → REQ-002-11: Adicionar um conteúdo a um tópico concluído deve reduzir os percentuais e retirar a conclusão até o novo item ser estudado e validado.
- CA-002-08 → REQ-002-12: Após a integração com 003, dois projetos validando o mesmo item devem contribuir com um único conteúdo para a cobertura.
- CA-002-09 → REQ-002-14: Simular falha ao desmarcar um item deve informar o erro e preservar o último resultado confirmado, permitindo repetir a intenção.
- CA-002-10 → REQ-002-10/11: Uma fase com um tópico concluído e outro vazio permanece pendente; alterações na validade da prática devem refletir nos seus tópicos, fases e roadmap.

## Fora de escopo

- Criar ou reorganizar cadastros da hierarquia: feature 001.
- Definir projetos, critérios e confirmação da prática: feature 003.
- Média única combinando estudo e prática, pesos por dificuldade, notas ou avaliações automáticas por IA.
- Histórico analítico, metas de tempo, gamificação e recomendação automática de estudo.
- Escolher tecnologia de gráficos, estado ou persistência nesta etapa.

## Revisão antes de Plan

Revisar as formas de marcação e filtro, a precisão dos percentuais e as mensagens de conclusão. O design deve definir salvamento, falhas e integração com a prática sem duplicar as regras de cálculo.
