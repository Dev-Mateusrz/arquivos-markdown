# 001 — Organização dos estudos

Status: Specify — rascunho para revisão. Os detalhamentos desta spec ainda serão revisados pelo usuário antes de Plan.

## Fontes e dependências

- [Organização e regras do produto](../../00-contexto/visao-produto.md#organização-dos-estudos).
- [Conteúdo inicial](../../00-contexto/roadmap.md#conteúdo-inicial) e [material Front-end](../../00-contexto/referencias/roadmap-frontend.md).
- [Glossário](../../00-contexto/glossario.md).
- Dependência funcional: nenhuma. É a base para progresso e projetos.

## Objetivo

Permitir ao ponto focal criar e organizar áreas de atuação, seus tópicos e conteúdos, com dados preservados entre acessos.

O resultado esperado é conseguir abrir uma área, entender suas fases e tópicos e manter os conteúdos que serão estudados e praticados.

## Escopo

- Criar e renomear áreas, com um roadmap por área.
- Criar, renomear e ordenar fases; iniciar novos roadmaps com Base, Profissional e Especialização.
- Criar e renomear tópicos; ordenar e mover tópicos entre fases do mesmo roadmap.
- Adicionar, editar e ordenar conteúdos dentro de um tópico.
- Navegar pela hierarquia, consultar estados vazios e preservar os cadastros após recarregar a aplicação.
- Disponibilizar o conteúdo inicial de estudos recebido.

## Histórias

- US-001-01: Como usuário, quero criar uma área para organizar um novo percurso de aprendizado.
- US-001-02: Como usuário, quero ajustar fases e tópicos para representar a sequência que pretendo estudar.
- US-001-03: Como usuário, quero adicionar e corrigir conteúdos para manter meu checklist.
- US-001-04: Como usuário, quero retomar os cadastros e o conteúdo inicial sem refazer a organização.

## Dados e validações propostas

| Elemento | Preenchimento e vínculo |
| --- | --- |
| Área | Nome obrigatório; possui um roadmap identificado pela área. |
| Fase | Nome obrigatório; pertence a um roadmap e tem posição nesse roadmap. |
| Tópico | Nome obrigatório; pertence a uma fase e tem posição nela. |
| Conteúdo | Título obrigatório; pertence a um tópico e tem posição em seu checklist. |

Remover espaços nas extremidades dos nomes e títulos. Rejeitar valores vazios ou compostos apenas de espaços.

Rejeitar duplicatas ignorando maiúsculas/minúsculas e espaços nas extremidades: áreas no conjunto do usuário, fases no mesmo roadmap, tópicos no mesmo roadmap e conteúdos no mesmo tópico. Permitir o mesmo título de conteúdo em tópicos distintos; são itens distintos para o acompanhamento.

A ordenação organiza a exibição e preserva a identidade dos elementos. Renomear e reordenar não apaga conteúdos ou altera marcações e vínculos que forem adicionados pelas features posteriores.

## Requisitos

- REQ-001-01: QUANDO o usuário confirmar uma área válida, O SISTEMA DEVE criar a área, um único roadmap associado e as fases iniciais Base, Profissional e Especialização.
- REQ-001-02: QUANDO o usuário consultar suas áreas, O SISTEMA DEVE permitir abrir o roadmap, suas fases, tópicos e conteúdos.
- REQ-001-03: QUANDO o usuário cadastrar ou renomear um elemento, O SISTEMA DEVE validar seu preenchimento e a unicidade no escopo definido acima.
- REQ-001-04: QUANDO houver erro de preenchimento, O SISTEMA DEVE indicar o campo e o motivo, preservando os dados informados para correção.
- REQ-001-05: QUANDO o usuário criar um tópico ou conteúdo válido, O SISTEMA DEVE associá-lo ao pai selecionado e apresentá-lo na lista correspondente.
- REQ-001-06: QUANDO o usuário criar um conteúdo, O SISTEMA DEVE iniciá-lo sem marcação de estudo, sem avaliação de facilidade/dificuldade e sem prática validada.
- REQ-001-07: QUANDO o usuário criar, renomear ou ordenar fases, O SISTEMA DEVE preservar os tópicos e conteúdos vinculados.
- REQ-001-08: QUANDO o usuário mover um tópico entre fases do mesmo roadmap, O SISTEMA DEVE preservar seus conteúdos e suas identidades e apresentar o tópico na nova fase.
- REQ-001-09: QUANDO o usuário reordenar tópicos ou conteúdos, O SISTEMA DEVE preservar e reapresentar a ordem confirmada.
- REQ-001-10: QUANDO uma edição for confirmada, O SISTEMA DEVE atualizar o elemento existente, mantendo seus vínculos e sem criar uma cópia.
- REQ-001-11: QUANDO uma área, fase ou tópico estiver vazio, O SISTEMA DEVE informar essa situação e permitir o cadastro do próximo nível.
- REQ-001-12: QUANDO um cadastro ou ajuste for salvo com sucesso, O SISTEMA DEVE preservá-lo após recarregar ou reabrir a aplicação.
- REQ-001-13: ENQUANTO houver gravação em andamento, O SISTEMA DEVE informar a operação e impedir que a mesma confirmação gere cadastros duplicados.
- REQ-001-14: QUANDO uma gravação falhar, O SISTEMA DEVE informar a falha, preservar os dados para nova tentativa e apresentar o último estado confirmado como persistido.
- REQ-001-15: QUANDO a base inicial for preparada, O SISTEMA DEVE disponibilizar a área Desenvolvimento Frontend, seus quinze tópicos e a distribuição em fases definida no roadmap do produto.
- REQ-001-16: QUANDO disponibilizar o tópico 15 inicial, O SISTEMA DEVE incluir os 65 conteúdos de IA recebidos, mantendo seus seis grupos, sem marcações de estudo ou avaliação.
- REQ-001-17: QUANDO a aplicação for reaberta ou a preparação inicial for repetida, O SISTEMA DEVE preservar os dados existentes, sem duplicar o catálogo nem sobrescrever alterações e marcações do usuário.

## Conteúdo inicial

Usar as fontes indicadas, preservando nomes e sequência dentro das fases. Os tópicos 1 a 14 iniciam sem itens individuais até o cadastro pelo usuário. Os seis grupos do tópico 15 organizam a apresentação dos seus conteúdos dentro desse tópico e não criam novas áreas, fases ou tópicos principais.

Os quatro projetos do material de estudo serão disponibilizados pela feature 003. A stack de aprendizagem não estabelece a tecnologia usada para implementar esta feature.

## Critérios de aceite

- CA-001-01 → REQ-001-01/02/12: Criar uma área Backend, recarregar a aplicação e encontrá-la com um roadmap e as três fases iniciais, sem duplicatas.
- CA-001-02 → REQ-001-03/04: Tentar cadastrar nomes em branco e uma área chamada “ backend ” após Backend; apresentar validação e preservar o formulário para correção.
- CA-001-03 → REQ-001-05/06: Criar um tópico Fundamentos e o conteúdo Requisição e resposta; o item deve pertencer ao tópico escolhido e iniciar sem estudo, avaliação ou prática.
- CA-001-04 → REQ-001-03: Repetir um título no mesmo tópico deve falhar; usar esse título em outro tópico deve ser permitido.
- CA-001-05 → REQ-001-07/08/09/10: Renomear e reordenar uma fase, mover um tópico e editar seu conteúdo; preservar a identidade e a associação dos itens após recarregar.
- CA-001-06 → REQ-001-11: Abrir uma fase sem tópicos e um tópico sem conteúdos; exibir estado vazio e acesso ao cadastro correspondente.
- CA-001-07 → REQ-001-13/14: Repetir a confirmação enquanto salva e simular falha de gravação; não duplicar registros nem apresentar como salva uma operação que falhou.
- CA-001-08 → REQ-001-15/16/17: Preparar uma base nova com os quinze tópicos e os 65 itens de IA, alterar um dado e reabrir; manter a alteração e uma única cópia dos dados iniciais.

## Fora de escopo

- Marcar estudo, avaliar facilidade/dificuldade e calcular indicadores: feature 002.
- Cadastrar projetos, associar conteúdos à prática e confirmar entregas: feature 003.
- Exclusão definitiva, arquivamento, transferência entre roadmaps e importação em massa.
- Autenticação, permissões e múltiplos usuários; a estratégia de acesso será tratada no planejamento compartilhado.
- Definir stack, banco, endpoints ou componentes de interface nesta etapa.

## Revisão antes de Plan

Revisar o recorte, os nomes e a unicidade por escopo, as operações de edição e a disponibilização inicial. No planejamento, definir arquitetura, persistência, acesso, fluxos, contratos e comandos reais de verificação antes das tarefas.
