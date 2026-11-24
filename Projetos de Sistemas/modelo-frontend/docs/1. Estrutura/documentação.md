Atualizado: 09/11/2026
# Organização Estrutural das Documentações de um Projeto Front-End

Ao criar ou organizar a documentação de um repositório frontend, aplique a estrutura e as regras abaixo. Os caminhos apresentados correspondem a um exemplo de como as documentações deverão ser organizadas no projeto, conforme suas necessidades reais.

## 1. Organize os arquivos nesta estrutura

```text
projeto/
├── docs/                           # Central de documentação
│   ├── README.md                   # Índice da documentação detalhada
│   ├── produto/                    # Separe o contexto do produto das regras
│   ├── tutoriais/                  # Experiências guiadas de aprendizado
│   │   └── primeiros-passos.md
│   ├── arquitetura/                # Desenho técnico e decisões
│   │   ├── visao-geral.md          # Diagramas Mermaid (C4 Model)
│   │   ├── modelo-dados.md
│   │   └── adrs/                   # Histórico de Decisões Arquiteturais
│   │       ├── README.md           # Índice das decisões
│   │       └── 0001-banco-dados.md
│   ├── guias/                      # Manuais de execução
│   │   ├── setup-ambiente.md       # Como rodar o projeto localmente
│   │   └── padrao-codigo.md        # Regras de Git, Commits e Lint
│   ├── api/                        # Contratos e integrações
│   │   ├── README.md               # Acesso à fonte canônica do contrato
│   │   └── endpoints.md            # Referência local, quando necessária
│   └── assets/
├── .github/workflows/              # Automações de CI/CD
│   ├── docs-check.yml              # Validador de links nos Pull Requests
│   └── docs-deploy.yml             # Publicação, quando houver portal
├── mkdocs.yml                      # Configuração, se o portal usar MkDocs
├── CONTRIBUTING.md                 # Entrada do fluxo de contribuição
└── README.md                       # Índice principal (porta de entrada)
```

Use nomes descritivos em minúsculas e kebab-case, preservando os nomes convencionais `README.md` e `CONTRIBUTING.md`. Substitua os nomes ilustrativos de tarefa e decisão pelo assunto real.

Crie apenas arquivos com conteúdo aplicável. `modelo-dados.md` depende de modelos relevantes para explicar; `webhooks.md` depende dessa integração; `deploy.md` depende de uma estratégia de entrega definida. O workflow `docs-deploy.yml` só é necessário quando houver publicação de um portal. Em GitLab, use a configuração de CI/CD correspondente.

Não crie páginas vazias para completar a árvore. Quando um assunto crescer, divida-o em páginas por responsabilidade e acrescente um índice local, mantendo o caminho de navegação até elas.

## 2. Mantenha o README como porta de entrada

No `README.md` da raiz, escreva apenas o nome do projeto, uma apresentação breve de sua finalidade e um sumário com links para a documentação e a contribuição.

Mantenha instalação, comandos, regras de negócio, decisões e explicações extensas nos arquivos especializados. O README deve direcionar para esses conteúdos, sem reproduzi-los.

Use `docs/README.md` como índice detalhado, agrupando os links pelas necessidades do leitor. Nos conjuntos que precisarem de índice próprio, como decisões ou manuais, use o README local para listar as páginas existentes. Toda página deve ser alcançável pelo índice adequado e oferecer um caminho de retorno.

Exemplos de links no README da raiz:

```markdown
- [Documentação](docs/README.md)
- [Preparar o ambiente](docs/guias/setup-ambiente.md)
- [Contribuir](CONTRIBUTING.md)
- [Visão da arquitetura](docs/arquitetura/visao-geral.md)
```

Inclua somente links cujos destinos existam. Dentro de uma página em `docs/guias/`, o retorno ao índice documental será relativo àquela localização, por exemplo `../README.md`.

## 3. Separe os conteúdos por responsabilidade e finalidade

| Local no projeto | Conteúdo a manter | Forma de organizar a página |
|---|---|---|
| `docs/tutoriais/` | Primeiros passos de uso ou desenvolvimento | Experiência guiada para aprender: objetivo, preparação, etapas e resultado de cada etapa |
| `docs/guias/` | Setup, padrões de desenvolvimento e procedimentos de deploy | Uma tarefa por página: pré-requisitos, passos, verificação e problemas frequentes |
| `docs/arquitetura/` | Visão técnica, responsabilidades, integrações e modelos relevantes | Explicação do desenho, de seus limites e da relação entre suas partes |
| `docs/arquitetura/adrs/` | Decisões arquiteturais e seus motivos | Um registro por decisão, com contexto, alternativas, escolha e consequências |
| `docs/produto/` | Visão do produto, requisitos e regras de negócio | Separe o contexto do produto das regras e cenários verificáveis |
| `docs/api/` | Contratos consumidos ou oferecidos e orientações de integração | Referência ao contrato canônico e detalhes próprios do consumidor |
| `CONTRIBUTING.md` | Entrada do fluxo de contribuição | Resumo do fluxo e links para os procedimentos, padrões e verificações existentes |

Essa separação já aplica o Diátaxis: aprendizado nos tutoriais, execução nos guias, consulta nas referências e compreensão nas explicações. Não mantenha cópias do mesmo conteúdo para classificá-lo por público e por formato.

Uma página deve atender a um objetivo principal. Quando um procedimento precisar de uma justificativa arquitetural ou de uma tabela extensa de configuração, vincule os documentos responsáveis por essas informações.

## 4. Preserve uma fonte de verdade

- Quando existir OpenAPI/Swagger, vincule o contrato em `docs/api/README.md`. Não reescreva manualmente os endpoints e payloads em uma referência concorrente.
- Use `endpoints.md` somente quando essa referência precisar ser mantida no próprio repositório e não houver outra fonte canônica. Registre `webhooks.md` apenas quando aplicável e respeite o mesmo princípio.
- Se o projeto utilizar Storybook ou ferramenta similar como catálogo de componentes visuais, mantenha nesse catálogo a referência de propriedades, estados e exemplos de uso. Nos arquivos Markdown, aponte para a instância correspondente, sem duplicar essa documentação.
- Se Jira ou Confluence concentrar requisitos e histórias, mantenha no repositório o contexto necessário e os links com identificadores; evite espelhar descrições e status que exigiriam sincronização manual.
- Mantenha cada procedimento completo em uma única página. Os índices e demais documentos devem apontar para ela.
- No frontend, documente os modelos e mapeamentos utilizados pela interface. Vincule o schema do backend em sua fonte original em vez de duplicar sua documentação de banco.

## 5. Coloque arquitetura e decisões nos arquivos próprios

Em `docs/arquitetura/visao-geral.md`, represente o contexto do sistema e suas relações. Acrescente a visão de contêineres quando precisar mostrar aplicações, serviços, armazenamentos e suas tecnologias. Detalhe componentes e código somente quando isso ajudar a compreensão. Mantenha os níveis separados e coerentes com o desenho real.

Escreva diagramas arquiteturais e de fluxo em blocos Mermaid versionados junto ao Markdown, com relações identificadas e uma explicação textual. Verifique sua renderização nas ferramentas adotadas. Não use imagens PNG/JPEG como fonte.

Para decisões relevantes, crie um arquivo em `docs/arquitetura/adrs/`, com numeração sequencial e título descritivo. Registre status, data conhecida, contexto, alternativas, decisão e consequências. Atualize o índice de decisões com número, título, status e link.

Preserve o conteúdo histórico das decisões aceitas. Se uma decisão mudar, crie uma nova ADR, ligue-a à anterior e atualize o status da antiga para “Superada por ADR NNNN”, com link relativo. Atualizar status e relações não deve reescrever o raciocínio original.

## 6. Escreva páginas curtas e conectadas

- Use títulos específicos, frases diretas e linguagem adequada ao público.
- Use passos numerados para sequências, listas para itens independentes e tabelas para informações de consulta.
- Identifique a linguagem dos blocos de código e o diretório de execução dos comandos. Informe o resultado esperado.
- Use links relativos entre arquivos, imagens e seções do mesmo repositório. Preserve a capitalização dos caminhos.
- Use URLs HTTPS para fontes externas, como contratos publicados e ferramentas de produto. A navegação interna deve continuar relativa.
- Armazene capturas úteis da interface em `docs/assets/`, com texto alternativo e dados sanitizados. Atualize-as quando a interface mudar.
- Divida páginas quando passarem a atender assuntos ou objetivos independentes; não transforme um documento em depósito de todas as informações do sistema.

## 7. Inclua validação e manutenção no fluxo do projeto

Versione os Markdown, as fontes dos diagramas e as configurações de validação junto com o código. No projeto destino, configure Markdownlint para os padrões de escrita e Lychee ou ferramenta equivalente para links e âncoras.

Em `docs-check.yml`, ou no job equivalente, execute as verificações nos PRs e faça falhas reais de documentação resultarem em falha do check. Configure a proteção da branch e a dependência da publicação para impedir a entrega de documentação inválida. Criar o workflow, sozinho, não torna o check obrigatório.

Quando houver portal, mantenha a configuração de geração e publicação separada das fontes e publique somente o conteúdo validado. A criação e a operação do portal dependem da ferramenta e da hospedagem escolhidas.

Atualize os documentos afetados no mesmo PR da mudança de código, comportamento, contrato ou configuração. Inclua a avaliação do impacto documental na definição de pronto. Ao encontrar uma instrução desatualizada durante o trabalho, corrija-a ou registre a pendência com sua localização.

Defina responsáveis pela revisão dos conjuntos documentais conforme o projeto. Ao mover, renomear ou remover páginas, atualize os índices, os links e a navegação de publicação relacionados.

Se uma página antiga precisar permanecer disponível por histórico, coloque um aviso no topo e indique a substituta:

```markdown
> **AVISO:** Esta documentação está legada e mantida apenas para fins de histórico técnico.
> Conteúdo vigente: [Título da página](caminho-relativo-da-substituta.md).
```

Antes de concluir, confira a árvore, a navegação, os links e os comandos documentados. Use informações reais do projeto, identifique propostas ou pendências e não apresente verificações não executadas como aprovadas.
