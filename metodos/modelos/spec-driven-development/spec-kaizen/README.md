# Kaizen — especificações

Status: contexto inicial registrado e três funcionalidades na etapa Specify, como rascunhos para revisão. A revisão começa pela feature 001.

## Instruções de trabalho

- [AGENTS.md](AGENTS.md): constituição operacional, leitura de contexto, limites e revisões entre etapas.
- [Modelo de feature](_template.md): estrutura de spec.md, design.md e tasks.md.
- As instruções de implementação ficam nos arquivos AGENTS.md dos repositórios frontend-kaizen e backend-kaizen, externos a este acervo.

## Contexto do produto

1. [Visão do produto](00-contexto/visao-produto.md): problema, usuário, organização, progresso e confirmação da prática.
2. [Glossário](00-contexto/glossario.md): linguagem usada no produto.
3. [Roadmap de entregas](00-contexto/roadmap.md): capacidades e conteúdo inicial.
4. [Material de referência Front-end](00-contexto/referencias/roadmap-frontend.md): quatro projetos, trilha de estudo, 65 itens de IA e imagem de orquestração.

## Funcionalidades em ordem

| Ordem | Feature | Dependência | Etapa atual |
| --- | --- | --- | --- |
| 001 | [Organização dos estudos](02-features/001-organizacao-dos-estudos/spec.md) | Nenhuma | Specify — rascunho para revisão. |
| 002 | [Progresso e avaliação](02-features/002-progresso-e-avaliacao/spec.md) | 001; prática integrada por 003. | Specify — rascunho para revisão. |
| 003 | [Projetos e validação prática](02-features/003-projetos-e-validacao-pratica/spec.md) | 001 e 002. | Specify — rascunho para revisão. |

A primeira entrega evolui do cadastro para o estudo e depois para a validação prática. Até a integração dos projetos, a cobertura prática é zero e os tópicos permanecem aguardando essa condição para conclusão.

Revisar a spec da feature selecionada antes de produzir design.md. Depois revisar o design antes de tasks.md e as tarefas antes da implementação. Design e tarefas serão criados quando suas etapas começarem.

## Arquitetura e implementação

A camada 01-arquitetura receberá as decisões compartilhadas de domínio, stack, persistência e acesso durante o planejamento. Os repositórios frontend-kaizen e backend-kaizen ainda estão sem implementação e comandos de aplicação definidos.

A stack e o fluxo de agentes presentes no material de referência descrevem os estudos do usuário. As decisões técnicas da aplicação serão registradas na camada de arquitetura e nos designs das features.

## Manutenção

Manter a regra compartilhada no contexto e os requisitos específicos na feature correspondente. Atualizar design e tarefas quando uma decisão aprovada mudar. Os conteúdos e projetos são dados do aprendizado; imagens e checklists de estudo são referências para o produto.

## Índice da pasta

- [00-contexto](00-contexto/README.md) — Visão do produto, glossário, roadmap e referências compartilhadas das especificações do Kaizen.
- [02-features](02-features/README.md) — Especificações das três funcionalidades do exemplo Kaizen, organizadas por identificador.
- [_template.md](_template.md)
- [AGENTS.md](AGENTS.md)

## Navegação

[Voltar ao índice da pasta anterior](../README.md)
