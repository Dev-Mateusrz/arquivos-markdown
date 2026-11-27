Metodologia de engenharia de software que usam especificações estruturadas como única fonte da verdade e que guiam todo o ciclo de vida do sistema - desde o planejamento até a geração e validação do código.

`Spec-First` É criada antes do código para guiar a implementação inicial, mas depois o código passa a ser a referência principal. É usada em protótipos avançados, MVPs rápidos ou features isoladas.

`Spec-Anchored` Permanece sincronizada com o código ao longo do tempo. Qualquer alteração de regra exige atualizar a spec antes. É o padrão ouro atual para sistemas em produção e equipes médias/grandes.

`Spec-as-Source` Humanos editam apenas as especificações; o código-fonte é tratado como um artefato compilado/gerado 100% por agentes. É usado em domínios altamente padronizados (ex: CRUDs, microsserviços simples, integrações).

## Forma Eficiente de Usar

Deve combinar Engenharia de Contexto, Divisão de Responsabilidades Entre Agentes e Validação Automatizada em CI/CD.

Frameworks Modernos:  
- GitHub Spec Kit https://github.com/github/spec-kit
- OpenSpec https://github.com/Fission-AI/OpenSpec

### Fluxo de Trabalho

1. Constitution (Regras Globais): Define-se uma única vez as leis imutáveis do projeto (stack, padrões de arquitetura, regras de segurança, estilo de código e convenções de teste)

2. Specify (O "O Quê" e "Por Quê"): Descreve-se o problema de negócio, histórias de usuário, fluxos, estados de borda (edge cases) e critérios de aceite (formato Given/When/Then), sem citar detalhes de implementação.

3. Clarify & Plan (O "Como"): O agente analisa a spec em busca de ambiguidades, faz perguntas ao desenvolvedor e gera um plano técnico (plan.md) contendo modelagem de dados, contratos de API e decisões arquiteturais.

4. Tasks (Decomposição Atômica): O plano é quebrado em tarefas pequenas e independentes (tasks.md), onde cada tarefa altera poucos arquivos e possui seu próprio critério de validação.

5. Implement & Converge (Execução e Auditoria): Um agente implementa tarefa por tarefa enquanto testes automatizados (unitários, de contrato e E2E) validam se o código final converge 100% com a especificação.

## Entradas e Saídas

Input do SDD: Problema de negócio, restrições arquiteturais (constitution.md) e requisitos funcionais/não funcionais.

Output do SDD: Contratos formais (openapi.yaml, schemas), critérios de aceite testáveis (spec.md) e planos atômicos (tasks.md) prontos para serem consumidos por agentes.

## Boas Práticas Eficientes

- Separe intenção de implementação: Nunca misture regras de negócio com escolhas de framework no mesmo arquivo de spec. Se você trocar o banco de dados amanhã, a spec de negócio continua intacta.

- Use o padrão de Agentes Especializados (Coordinator / Implementor / Verifier): Evite usar o mesmo chat para planejar e codar. Use um modelo mais robusto (raciocínio profundo) para gerar a spec e o plano, limpe o contexto, e use um agente executor focado apenas na tarefa atual.

- Progressive Disclosure (Carregamento sob demanda): Não jogue 50 arquivos de documentação no prompt. Mantenha um índice curto na raiz (CLAUDE.md ou .cursorrules) que aponta para as specs específicas de cada domínio apenas quando o agente for mexer naquela pasta.

- Contrato como Gate de CI/CD: Configure linters (como Spectral) e testes de contrato (como Pact ou Specmatic) na esteira de Pull Request para bloquear merges que violem a spec.

- Architecture Decision Records (ADRs): Documentos curtos que registram o porquê de escolhas técnicas (ex.: "Por que usamos Redis para filas e não RabbitMQ"), servindo de memória arquitetural permanente para o agente durante a fase de planejamento.

## Limitações / Quando NÃO usar

- Exploração visual / UI altamente experimental: Onde o usuário precisa "ver e sentir" a interface antes de conseguir especificar regras rígidas.

- Hotfixes triviais de 1 linha: Onde o custo de atualizar spec -> plan -> tasks é maior que a própria correção.

## Organização Estrutural

Para evitar que as especificações fiquem espalhadas ou desatualizadas entre equipes, o mercado adota uma arquitetura centrada em contratos compartilhados, seja em um Monorepo ou em repositórios separados.

No mundo multi-agente, a spec não serve apenas para alinhar humanos, mas para isolar o contexto de agentes paralelos.

Enquanto um agente trabalha no Backend e outro no Frontend (ou em microsserviços distintos), nenhum precisa ler o código do outro — ambos leem apenas o .specs/contracts/.

```
meu-projeto/
├── .specs/                          # Fonte única de verdade do sistema
│   ├── constitution.md              # Padrões globais, stack, segurança e arquitetura
│   ├── architecture/                # ADRs (Architecture Decision Records) e diagramas
│   ├── contracts/                   # Contratos executáveis (Front <-> Back)
│   │   ├── openapi.yaml             # Especificação REST unificada
│   │   ├── asyncapi.yaml            # Eventos/WebSockets (se houver)
│   │   └── schemas/                 # JSON Schemas / Zod compartilhados
│   └── features/                    # Especificações organizadas por domínio/feature
│       └── 001-checkout/
│           ├── spec.md              # Requisitos, regras de negócio e critérios de aceite
│           ├── plan.md              # Decisões técnicas e fluxo de estado
│           └── tasks.md             # Checklist atômico de implementação
│
├── backend/
│   ├── src/
│   └── tests/
│       └── contract/                # Testes que validam rotas reais contra o openapi.yaml
│
├── frontend/
│   ├── src/
│   │   └── api/generated/           # Tipos TS, hooks (React Query) e mocks gerados da spec
│   └── tests/
│       └── e2e/                     # Testes baseados nos cenários Given/When/Then da spec.md
│
├── CLAUDE.md / AGENTS.md            # Instruções curtas ensinando os agentes a lerem .specs/
└── .github/workflows/
    └── spec-validation.yml          # Valida lint do OpenAPI e sincronia antes do merge
```

O Contrato é o Ponto de Encontro (contracts/openapi.yaml):

> Antes de escrever uma linha de controller no backend ou de tela no frontend, o arquivo OpenAPI/GraphQL é atualizado e validado.

 Desenvolvimento Paralelo Real no Frontend: 

> Ferramentas de codegen (como Orval ou openapi-typescript) leem o openapi.yaml e geram automaticamente as interfaces TypeScript, clientes HTTP e até servidores mockados (MSW).
      
> O frontend não precisa esperar o backend ficar pronto nem escrever tipos manualmente; o agente de IA do frontend consome os tipos gerados e as regras visuais descritas em features/001-checkout/spec.md.

Implementação Blindada no Backend:

> O agente do backend lê constitution.md, features/001-checkout/spec.md e o openapi.yaml.

> Ele gera os DTOs/Schemas de validação diretamente do contrato, implementa as regras de negócio e roda testes de contrato automatizados para provar que os status codes (200, 400, 422) e payloads batem exatamente com o que foi prometido ao frontend.



