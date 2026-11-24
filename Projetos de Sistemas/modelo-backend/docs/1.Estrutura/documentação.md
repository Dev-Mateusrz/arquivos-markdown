Atualizado: 14/11/2026
# Organização Estrutural das Documentações de um Projeto Back-End

Ao criar ou organizar a documentação de um repositório backend, aplique a estrutura e as regras abaixo. Os caminhos apresentados representam o **projeto destino**, conforme suas necessidades reais. Mantenha a documentação coerente com os módulos, contratos, dados e controles definidos no [guia de arquitetura](arquitetura.md), preservando as convenções da stack escolhida.

## 1. Organize os arquivos nesta estrutura

```text
projeto/
├── docs/                           # Central de documentação
│   ├── README.md                   # Índice da documentação detalhada
│   ├── produto/                    # Contexto do domínio, requisitos e regras
│   ├── tutoriais/                  # Experiências guiadas de aprendizado
│   │   └── primeiros-passos.md
│   ├── arquitetura/                # Desenho técnico e decisões
│   │   ├── visao-geral.md          # Contexto, contêineres e relações do sistema
│   │   ├── modelo-dados.md         # Modelo conceitual e propriedade dos dados
│   │   └── adrs/                   # Histórico de decisões arquiteturais
│   │       ├── README.md           # Índice das decisões
│   │       └── 0001-banco-dados.md
│   ├── guias/                      # Manuais de desenvolvimento e operação
│   │   ├── setup-ambiente.md       # Serviço, banco e filas no ambiente local
│   │   ├── padrao-codigo.md        # Git, commits, lint e testes
│   │   └── runbooks.md             # Entrada de operação e links para procedimentos
│   ├── api/                        # Contratos e orientações de integração
│   │   ├── README.md               # Acesso às fontes canônicas e suas versões
│   │   ├── endpoints.md            # Orientações complementares de consumo HTTP
│   │   └── eventos-webhooks.md     # Consumo de eventos e webhooks, quando aplicável
│   └── assets/                     # Evidências e recursos visuais sanitizados
├── .github/workflows/              # Automações de CI/CD
│   ├── docs-check.yml              # Validação de documentação e contratos nos PRs
│   └── docs-deploy.yml             # Publicação, quando houver portal
├── mkdocs.yml                      # Configuração, se o portal usar MkDocs
├── .env.example                    # Exemplo seguro de configuração, se utilizado
├── CONTRIBUTING.md                 # Entrada do fluxo de contribuição
└── README.md                       # Índice principal e porta de entrada
```

Use nomes descritivos em minúsculas e kebab-case, preservando os nomes convencionais `README.md` e `CONTRIBUTING.md`. Substitua os nomes ilustrativos de tarefa e decisão pelo assunto real.

Crie apenas arquivos com conteúdo aplicável. `modelo-dados.md` depende de modelos e relações relevantes para explicar; `eventos-webhooks.md` depende dessas integrações; `runbooks.md` depende de procedimentos operacionais definidos. Prepare os procedimentos necessários antes de colocar um fluxo crítico em operação. O workflow `docs-deploy.yml` só é necessário quando houver publicação de um portal. Em GitLab ou outra plataforma, use a configuração de CI/CD correspondente.

Não crie páginas vazias para completar a árvore. Quando um assunto crescer, divida-o em páginas por responsabilidade e acrescente um índice local, mantendo o caminho de navegação até elas. Preserve os diretórios nativos de contratos, migrações e configuração quando a stack estabelecer outros caminhos.

## 2. Mantenha o README como porta de entrada

No `README.md` da raiz, escreva apenas o nome do serviço, uma apresentação breve de sua responsabilidade no sistema e um sumário com links para a documentação e a contribuição.

Mantenha instalação, comandos de migração, configuração, regras de negócio, decisões e explicações extensas nos arquivos especializados. O README deve direcionar para esses conteúdos, sem reproduzi-los.

Use `docs/README.md` como índice detalhado, agrupando os links pelas necessidades do leitor: desenvolvimento local, contexto do domínio, arquitetura, contratos e operação. Nos conjuntos que precisarem de índice próprio, como decisões ou procedimentos operacionais, use o README local para listar as páginas existentes. Toda página deve ser alcançável pelo índice adequado e oferecer um caminho de retorno.

Exemplos de links no README da raiz do projeto destino:

```markdown
- [Documentação](docs/README.md)
- [Preparar o ambiente](docs/guias/setup-ambiente.md)
- [Contratos da API](docs/api/README.md)
- [Visão da arquitetura](docs/arquitetura/visao-geral.md)
- [Contribuir](CONTRIBUTING.md)
```

Inclua somente links cujos destinos existam. Dentro de uma página em `docs/guias/`, o retorno ao índice documental será relativo àquela localização, por exemplo `../README.md`.

## 3. Separe os conteúdos por responsabilidade e finalidade

| Local no projeto | Conteúdo a manter | Forma de organizar a página |
|---|---|---|
| `docs/tutoriais/` | Primeiros passos de integração ou desenvolvimento no serviço | Experiência guiada para aprender: objetivo, preparação, etapas e resultado de cada etapa |
| `docs/guias/` | Setup local, migrações, padrões de código, deploy e procedimentos operacionais | Uma tarefa por página: pré-requisitos, passos, verificação e problemas frequentes |
| `docs/arquitetura/` | Visão técnica, módulos, propriedade dos dados, integrações e limites de confiança | Explicação do desenho, de seus limites e da relação entre suas partes |
| `docs/arquitetura/adrs/` | Decisões arquiteturais e seus motivos | Um registro por decisão, com contexto, alternativas, escolha e consequências |
| `docs/produto/` | Contexto do domínio, requisitos e regras de negócio | Separe o contexto do produto das invariantes e dos cenários verificáveis |
| `docs/api/` | Contratos HTTP, GraphQL, gRPC, eventos e webhooks utilizados pelo serviço | Referência à fonte canônica e orientações de autenticação, erros, limites e evolução |
| `CONTRIBUTING.md` | Entrada do fluxo de contribuição | Resumo do fluxo e links para os procedimentos, padrões e verificações existentes |

Essa separação aplica o [Diátaxis](https://diataxis.fr/): aprendizado nos tutoriais, execução nos guias, consulta nas referências e compreensão nas explicações. Classifique pelo objetivo do leitor; uma introdução guiada e um procedimento de recuperação atendem necessidades diferentes, mesmo quando tratam do mesmo serviço.

Uma página deve atender a um objetivo principal. Quando um procedimento precisar de uma justificativa arquitetural ou de uma referência extensa de configuração, vincule os documentos responsáveis. Mantenha cada conteúdo completo em um único lugar e conecte as páginas pelos índices apropriados.

### Procedimentos operacionais e runbooks

Use `docs/guias/runbooks.md` como entrada operacional curta, com links para procedimentos por tarefa. Quando houver um conjunto maior, organize-o em `docs/guias/runbooks/`, com `README.md` local e nomes específicos, como `reprocessar-mensagens.md` ou `restaurar-backup.md`. Atualize os índices e os links ao fazer essa mudança.

Em cada procedimento, registre:

- Objetivo, sinais que justificam o uso, responsável e permissões necessárias.
- Ambiente e versão aplicáveis, dependências, pré-condições e escopo dos dados afetados.
- Passos e comandos reais, com diretório de execução, parâmetros e resultados esperados.
- Verificações de saúde, logs e métricas que confirmam o resultado, com limites definidos pelo projeto.
- Impactos, condições de parada, recuperação ou reversão disponível e caminho de escalonamento.
- Data e ambiente da última validação, com limitações ou etapas ainda pendentes.

Em reprocessamentos, explique seleção das mensagens, escopo do tenant, idempotência e efeitos de duplicação. Em migrações e restaurações, documente a estratégia realmente suportada, incluindo correção posterior quando não houver reversão segura. Exercite os procedimentos em ambiente apropriado antes de apresentá-los como validados e mantenha as evidências sanitizadas.

## 4. Preserve uma fonte de verdade

### Contratos de API e integração

Identifique a fonte canônica de cada contrato e vincule-a em `docs/api/README.md`. Registre protocolo, módulo ou serviço responsável, versão e localização do arquivo ou processo que a produz:

| Contrato | Fonte canônica a vincular | Orientação de manutenção |
|---|---|---|
| API HTTP | Descrição [OpenAPI](https://spec.openapis.org/oas/latest.html) versionada ou gerada pelo projeto | Gerar a referência de rotas, payloads, autenticação e respostas a partir dessa descrição |
| API GraphQL | Schema conforme o [sistema de tipos GraphQL](https://graphql.org/learn/schema/), mantido em SDL ou produzido pelas definições do código | Gerar a referência de tipos, campos, argumentos e operações a partir do schema da versão correspondente |
| Eventos e canais de mensagens | Descrição [AsyncAPI](https://www.asyncapi.com/docs/reference/specification/latest) e schemas referenciados | Identificar operações de envio e recebimento, canais, mensagens e contratos públicos |
| API gRPC | Arquivos `.proto` e suas dependências, conforme o modelo de [definição de serviços gRPC](https://grpc.io/docs/what-is-grpc/core-concepts/) | Gerar referências e clientes a partir dos mesmos contratos utilizados pelo serviço |

Escolha como cada contrato será mantido. Em uma abordagem orientada à especificação, altere a descrição e gere os artefatos correspondentes. Em uma abordagem orientada ao código, altere as definições do código e gere a descrição de forma reproduzível. Identifique arquivos gerados e o comando de geração; mantenha a saída publicada rastreável à versão ou ao commit que a produziu.

Vincule a fonte e, quando existir, sua visualização navegável. Swagger UI, portais e referências geradas devem refletir a mesma descrição. Evite cópias manuais de rotas, schemas e códigos de status em páginas concorrentes.

Para GraphQL, identifique se o schema é mantido em SDL ou gerado pelo código. Registre o comando e as versões das ferramentas de geração e vincule o schema publicado ao commit ou à versão do serviço. Use SDL exportado ou um artefato de introspecção quando necessário à distribuição, identificando-o como derivado da origem canônica. A descrição OpenAPI do transporte HTTP, quando existir, não substitui o schema GraphQL. Gere a documentação de forma reproduzível a partir dessa mesma origem, sem depender de introspecção pública do serviço de produção.

Use `endpoints.md` e `eventos-webhooks.md` para orientações complementares: fluxo de autenticação, autorização, paginação, idempotência, assinatura de webhooks, retentativas, ordem e duplicação de eventos, erros e política de descontinuação. Mantenha os detalhes no contrato quando o formato permitir representá-los e vincule-os na explicação complementar. Uma referência Markdown mantida manualmente pode ser canônica quando não houver outra descrição; identifique essa condição e seu responsável.

Escolha a descrição de webhooks conforme o protocolo e as ferramentas adotadas. OpenAPI oferece mecanismos para webhooks e callbacks HTTP nas versões que os suportam; AsyncAPI descreve APIs orientadas a mensagens. Quando houver schemas compartilhados, referencie ou gere a partir da origem escolhida, preservando a consistência entre contratos.

### Dados, configuração e contexto do negócio

- **Persistência:** vincule as migrações e o schema declarativo nos caminhos reais, como `database/`. Identifique a fonte usada para gerar e aplicar mudanças conforme a ferramenta. As entidades do domínio representam regras e comportamento; sua estrutura pode diferir do modelo persistido. Em `docs/arquitetura/modelo-dados.md`, explique o modelo conceitual, a propriedade dos dados por módulo e as relações críticas, vinculando as definições físicas em vez de copiar listas exaustivas de colunas.
- **Configuração:** mantenha a validação e os padrões efetivos no código, como `src/config/`, e um `.env.example` seguro quando esse mecanismo for utilizado. Gere referências a partir dessas definições quando possível. Nos guias, explique finalidade, obrigatoriedade, origem dos valores e dependências habilitadas, evitando uma segunda lista manual que divirja da configuração real.
- **Requisitos e regras:** se Jira, Linear ou Confluence concentrar histórias e requisitos, mantenha no repositório o contexto técnico necessário e links com identificadores. Documente invariantes e cenários necessários à manutenção sem espelhar descrições e status que exijam sincronização manual.
- **Procedimentos:** mantenha cada sequência operacional em uma página responsável. Tutoriais, índices, ADRs e explicações devem apontar para ela quando precisarem dessa execução.

## 5. Coloque arquitetura e decisões nos arquivos próprios

Em `docs/arquitetura/visao-geral.md`, represente o contexto do sistema e suas relações externas usando o [C4 Model](https://c4model.com/diagrams). Acrescente a visão de contêineres quando precisar mostrar aplicações, workers executados separadamente, bancos, caches e mensageria. Use o nível de componentes para detalhar módulos internos quando isso ajudar a compreensão. Mantenha cada nível coerente com a execução real e identifique propósito, limites e relações.

Escreva diagramas arquiteturais, de sequência e de estados em blocos Mermaid versionados junto ao Markdown, com relações identificadas e explicação textual. Use a sintaxe suportada pelo renderizador adotado; ao empregar a [sintaxe C4 do Mermaid](https://mermaid.js.org/syntax/c4.html), confira a compatibilidade da versão. Preserve a fonte textual editável e verifique a renderização no repositório e no portal, quando houver publicação.

Explique as fronteiras públicas dos módulos, a propriedade dos dados e os fluxos críticos de consistência. Documente também limites de confiança, responsabilidades de autenticação e autorização e referências para os controles de segurança efetivamente adotados. Vincule contratos e runbooks para os detalhes de integração e operação, evitando duplicar seu conteúdo.

Para decisões relevantes, como banco, mensageria, autenticação ou separação de módulos, crie uma ADR em `docs/arquitetura/adrs/`, conforme a prática de [Architecture Decision Records](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions). Use numeração sequencial, sem reutilizar números, e título descritivo. Registre status, data conhecida, responsáveis, contexto, alternativas, decisão e consequências. Atualize o índice com número, título, status e link.

Mantenha propostas identificadas como propostas até haver uma decisão. Preserve o raciocínio histórico das decisões aceitas. Se uma decisão mudar, crie uma nova ADR, ligue-a à anterior e atualize o status da antiga para “Superada por ADR NNNN”, com link relativo. Atualizar status e relações não deve reescrever a justificativa original.

## 6. Escreva páginas curtas e conectadas

- Use títulos específicos, frases diretas e linguagem adequada ao público. Explicite pré-requisitos de conhecimento nos tutoriais e de execução nos guias.
- Use passos numerados para sequências, listas para itens independentes e tabelas para informações de consulta.
- Identifique a linguagem dos blocos de código, como `bash`, `powershell`, `sql`, `json`, `http` ou `yaml`, e o diretório de execução dos comandos. Informe ambiente, parâmetros, resultado esperado e efeitos persistentes quando aplicáveis.
- Use links relativos entre arquivos, diagramas e seções do mesmo repositório. Preserve capitalização e confira âncoras após renomear títulos.
- Use URLs HTTPS para fontes externas, contratos publicados e painéis de observabilidade. A navegação interna deve continuar relativa.
- Use dados sintéticos e placeholders identificados em exemplos. Mantenha tokens, chaves, senhas, strings de conexão sensíveis e dados pessoais reais fora de comandos, payloads, logs e capturas publicados.
- Armazene evidências visuais em `docs/assets/`, com texto alternativo e dados sanitizados. Preserve diagramas como texto; capturas devem complementar uma explicação ou evidenciar uma verificação.
- Divida páginas quando passarem a atender objetivos independentes. Acrescente o índice necessário e mantenha cada fonte acessível pela navegação adequada.

Classifique o acesso ao conteúdo conforme o público. Preserve as restrições de documentos internos, contratos privados, procedimentos e painéis ao configurar o portal ou compartilhar artefatos. Separe o conteúdo destinado aos consumidores externos e publique apenas as informações autorizadas para esse público.

## 7. Inclua validação e manutenção no fluxo do projeto

Aplique **Docs-as-Code**: versione Markdown, fontes dos diagramas, contratos mantidos no repositório e configurações de validação; revise-os por PR junto das alterações correspondentes. Identifique como obter ou gerar contratos canônicos que pertençam a outro repositório ou provedor, preservando sua rastreabilidade.

No projeto destino, configure verificações proporcionais aos formatos utilizados:

| Conteúdo | Ferramenta ou mecanismo a avaliar | O que verificar |
|---|---|---|
| Markdown | [markdownlint](https://github.com/DavidAnson/markdownlint) | Padrões de escrita e estrutura, com regras compatíveis com a convenção de metadados adotada |
| Links, arquivos e âncoras | [Lychee](https://github.com/lycheeverse/lychee) ou equivalente | Caminhos locais, destinos externos e fragmentos, habilitando a verificação correspondente |
| Diagramas e portal | Renderizador Mermaid e build da ferramenta de publicação | Sintaxe, compatibilidade, navegação e apresentação final |
| OpenAPI | [Redocly CLI](https://redocly.com/docs/cli/commands/lint) ou [Spectral](https://github.com/stoplightio/spectral), com suporte à versão adotada | Estrutura do contrato, referências e regras de qualidade configuradas |
| GraphQL, quando utilizado | Validação do schema e das operações com implementação compatível com a especificação e comparação com o schema publicado | Definições válidas, operações utilizadas pelos consumidores e mudanças incompatíveis em campos, argumentos e tipos |
| AsyncAPI | [AsyncAPI CLI](https://www.asyncapi.com/docs/tools/cli), com lint adicional compatível quando necessário | Validade do documento, schemas e referências conforme a versão adotada |
| Protobuf, quando utilizado | Compilador e verificações de lint e compatibilidade, como [Buf](https://buf.build/docs/breaking/) | Definições válidas e alterações incompatíveis em relação à versão de referência |

Confirme a versão suportada, configure os conjuntos de regras e mantenha ferramentas e dependências reproduzíveis. A análise de âncoras depende do formato e do renderizador; em links cujos fragmentos surgem apenas por JavaScript, complemente a verificação conforme necessário. Trate destinos privados com acesso apropriado e exceções específicas, justificadas e revisáveis, preservando os checks dos demais links.

Valide contratos gerados a partir da origem real antes de gerar o portal ou compará-los com uma versão publicada. Separe a checagem de estrutura da avaliação de compatibilidade e da conformidade do comportamento: para mudanças de contrato, compare com a versão consumida e execute os testes relevantes. Registre mudanças incompatíveis, estratégia de migração e prazos reais de descontinuação quando aplicáveis.

Em GraphQL, gere ou carregue o schema da revisão avaliada e valide as operações disponíveis dos consumidores contra ele. Compare-o com a versão publicada segundo a política de compatibilidade do projeto. Cubra uma operação válida e uma operação invalidada por remoção ou alteração incompatível; verifique também que o artefato usado pelo portal corresponde à mesma revisão. Uma comparação de schema não demonstra, sozinha, a compatibilidade do comportamento dos resolvers.

Em `docs-check.yml`, ou no job equivalente, execute as verificações nos PRs e faça falhas reais resultarem em falha do check. Inclua os caminhos reais dos documentos e das fontes que os afetam, como código de contratos, schemas e configuração. Configure os checks obrigatórios na política de merge e faça a publicação depender da validação correspondente. Criar um workflow, sozinho, não torna o check obrigatório.

Quando houver portal, mantenha a configuração de geração e publicação separada das fontes. Publique o conteúdo validado da revisão correspondente, com os controles de acesso previstos. Configure a verificação de exemplos e procedimentos em ambiente isolado e apropriado; evite que a validação documental dispare efeitos em produção.

Atualize os documentos afetados no mesmo PR da mudança de código, comportamento, contrato, migração ou configuração, conforme as [boas práticas de manutenção documental](https://google.github.io/styleguide/docguide/best_practices.html). Inclua a avaliação do impacto na definição de pronto. Ao encontrar uma instrução desatualizada, corrija-a ou registre a pendência com sua localização e responsável.

Defina responsáveis pela revisão dos conjuntos documentais. Atualize runbooks quando mudarem dependências, permissões, alertas ou formas de recuperação. Registre o que foi validado e as limitações encontradas. Ao mover, renomear ou remover páginas, atualize os índices, os links e a navegação de publicação relacionados.

Se uma página antiga precisar permanecer disponível por histórico, coloque um aviso no topo e indique uma substituta existente:

```markdown
> **AVISO:** Esta documentação está legada e mantida apenas para fins de histórico técnico.
> Conteúdo vigente: [Título da página](caminho-relativo-da-substituta.md).
```

Antes de concluir, confira que:

- A árvore contém apenas páginas aplicáveis e a navegação permite localizar e retornar de cada conteúdo.
- Contratos, configuração e definições de dados têm fontes identificadas e referências coerentes com a versão do serviço.
- Comandos, exemplos e procedimentos utilizam informações verificadas, dados sintéticos e ambientes apropriados.
- Diagramas e páginas renderizam nas ferramentas adotadas, e os checks cobrem os arquivos afetados.
- Decisões, responsáveis, restrições de acesso e procedimentos de recuperação estão registrados quando necessários.
- Propostas, pendências e verificações não executadas estão identificadas, sem serem apresentadas como aprovadas.

## Referências de manutenção

As regras acima aplicam a organização documental desta base ao backend. Use as fontes para conferir os métodos e as capacidades das ferramentas na versão adotada pelo projeto.

- [Diátaxis — tutoriais, guias, referências e explicações](https://diataxis.fr/)
- [Google — boas práticas de documentação](https://google.github.io/styleguide/docguide/best_practices.html)
- [C4 Model — níveis de diagramas arquiteturais](https://c4model.com/diagrams)
- [Mermaid — diagramas C4](https://mermaid.js.org/syntax/c4.html)
- [Michael Nygard — Architecture Decision Records](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [OpenAPI — especificação de APIs HTTP](https://spec.openapis.org/oas/latest.html)
- [GraphQL — schema, tipos e formas de definição](https://graphql.org/learn/schema/)
- [AsyncAPI — especificação de APIs orientadas a mensagens](https://www.asyncapi.com/docs/reference/specification/latest)
- [gRPC — contratos e definição dos serviços](https://grpc.io/docs/what-is-grpc/core-concepts/)
- [markdownlint — validação estrutural de Markdown](https://github.com/DavidAnson/markdownlint)
- [Lychee — verificação de links e fragmentos](https://github.com/lycheeverse/lychee)
- [Redocly CLI — lint de contratos](https://redocly.com/docs/cli/commands/lint)
- [Spectral — conjuntos de regras para contratos](https://github.com/stoplightio/spectral)
- [AsyncAPI CLI — ferramentas de validação e geração](https://www.asyncapi.com/docs/tools/cli)
- [Buf — detecção de mudanças incompatíveis em Protobuf](https://buf.build/docs/breaking/)
