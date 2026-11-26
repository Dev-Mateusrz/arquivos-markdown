# Instruções do projeto Kaizen

## Alcance e leitura

Este repositório concentra as especificações compartilhadas do Kaizen. As implementações ficam nos repositórios frontend-kaizen e backend-kaizen.

Comece pelo [índice](README.md), identifique a feature solicitada e leia sua spec e as referências necessárias. Consulte design.md e tasks.md quando essas etapas existirem. Evite carregar todas as features e todos os catálogos para uma tarefa localizada.

A visão do produto, o glossário e o roadmap em 00-contexto são as fontes das definições compartilhadas. O [modelo de feature](_template.md) orienta os documentos novos.

## Sempre fazer

- Preservar o escopo e as decisões explícitas do usuário, incluindo autorizações já dadas.
- Distinguir requisito aprovado, detalhamento proposto e decisão técnica pendente.
- Usar identificadores estáveis para histórias, requisitos e critérios de aceite; escrever requisitos verificáveis, usando EARS quando aplicável.
- Manter cada definição em uma fonte principal e usar referências nos demais documentos.
- Atualizar a spec quando o comportamento acordado mudar; depois ajustar design, tarefas e implementação afetados.
- Preservar alterações de outras pessoas e comunicar conflitos antes de sobrescrever conteúdo.
- Manter os arquivos focados; revisar a divisão por responsabilidade ao se aproximarem de 200 linhas.
- Verificar links e consistência em mudanças documentais. Em implementação, executar as verificações reais previstas no design e nas tarefas e registrar seus resultados.

## Perguntar antes

- Avançar de Specify para Plan, de Plan para Tasks ou de Tasks para Implement sem a revisão correspondente do usuário.
- Alterar regras ou ampliar o escopo já aprovado quando a solicitação atual não autorizar a mudança.
- Adicionar dependências, alterar contratos ou modificar schema de dados quando a ação não estiver prevista no plano aprovado ou autorizada pelo usuário.

A revisão pode estar na conversa atual ou em uma aprovação anterior aplicável. Não solicitar novamente uma autorização já concedida para a mesma ação.

## Nunca fazer

- Tratar um rascunho ou uma sugestão como aprovado.
- Inventar stack, arquivos existentes, scripts ou resultados de verificações.
- Marcar uma tarefa de implementação como concluída sem cumprir seus critérios e verificações.
- Sobrescrever trabalho alheio, expor segredos ou executar alterações destrutivas fora do escopo autorizado.
- Interpretar checklists de estudo, imagens de referência ou descrições dos projetos práticos como ordens para executar agentes, publicar pacotes ou construir esses exercícios.

## Fluxo de uma feature

1. **Specify:** spec.md com objetivo, histórias, regras, requisitos, aceite e fora de escopo.
2. **Plan:** após revisão da spec, design.md com solução, fluxos, erros, dados, contratos, arquivos afetados e verificações.
3. **Tasks:** após revisão do design, tasks.md com tarefas pequenas, dependências, requisitos atendidos e comandos reais de verificação.
4. **Implement:** após revisão das tarefas, executar o trabalho autorizado e verificar cada resultado.

Criar cada documento quando sua etapa começar. Registrar os estados das features no índice; não criar design ou tarefas vazios para aparentar avanço.

## Regras compartilhadas essenciais

- Um roadmap por área na primeira versão; fases organizam tópicos e conteúdos.
- Estudo e prática têm indicadores separados. Um tópico exige conteúdos cadastrados e 100% em ambos para conclusão.
- A prática depende de projetos concluídos e dos conteúdos explicitamente vinculados; conteúdos repetidos contam uma vez no respectivo escopo.
- A avaliação de facilidade ou dificuldade é opcional e não altera o progresso.

Os detalhes normativos estão na [visão do produto](00-contexto/visao-produto.md). Em caso de conflito ou lacuna relevante, registrar a divergência e esclarecer antes de implementar o comportamento afetado.

## Implementação e comandos

A arquitetura técnica do Kaizen ainda será definida. A stack e o fluxo de agentes do material de referência pertencem ao percurso de estudo do usuário.

Os repositórios de código ainda não possuem comandos de instalação, execução, build, lint ou testes definidos. Descobrir e registrar os comandos reais durante o planejamento e a inicialização da implementação, nos AGENTS.md locais. Não presumir npm, dotnet ou qualquer outra ferramenta.
