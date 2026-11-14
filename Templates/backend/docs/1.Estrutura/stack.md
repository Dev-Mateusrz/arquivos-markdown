Atualizado: 14/11/2026
# Escolha da stack de tecnologia de um projeto backend

Ao iniciar um projeto backend, siga esta sequência para escolher as tecnologias conforme os requisitos do produto, da equipe e da operação. Produza uma decisão justificada antes de gerar a base do projeto ou provisionar infraestrutura. Os critérios abaixo são a política desta base; não representam uma stack obrigatória para todos os sistemas.

## 1. Levante as quatro dimensões de restrição

Leia os requisitos e as decisões já fornecidas. Em um projeto existente, identifique também a stack atual, os contratos de integração, o modelo de dados e as limitações operacionais antes de propor substituições.

| Dimensão | O que identificar | Como usar na escolha |
|---|---|---|
| Produto, dados e carga | Operações críticas, volume e picos de requisições, latência, concorrência, crescimento dos dados, garantias de consistência, tarefas assíncronas e integrações | Definir o modelo de processamento, a persistência e os requisitos de comunicação |
| Prazo e velocidade de entrega | Data ou janela de entrega, escopo do MVP, integrações prioritárias e disponibilidade para configurar e validar a infraestrutura | Favorecer soluções conhecidas ou integradas quando reduzirem trabalho necessário à entrega |
| Equipe e manutenção | Experiência efetiva, pessoas disponíveis, continuidade, aprendizado e responsáveis pela operação do serviço | Considerar produtividade, legibilidade e capacidade de diagnosticar e recuperar falhas |
| Orçamento e infraestrutura | Ambientes autorizados, serviços existentes, previsão de uso, limites de custo e requisitos conhecidos de privacidade, acesso, localização e retenção dos dados | Excluir opções incompatíveis e estimar o custo completo das alternativas viáveis |

Explicite os objetivos de disponibilidade e recuperação quando forem relevantes. Registre a perda de dados tolerada (**RPO**) e o prazo de recuperação esperado (**RTO**), relacionando-os a backups, restauração e capacidade operacional. Identifique quais operações precisam de resposta imediata e quais podem terminar de forma assíncrona.

Registre fatos, hipóteses e pendências separadamente. Reaproveite respostas já existentes. Quando faltar uma restrição capaz de mudar a decisão, solicite o dado necessário; avance na avaliação das partes independentes sem inventar orçamento, tráfego, prazo ou competências da equipe.

## 2. Separe requisitos eliminatórios de preferências

Antes de pontuar tecnologias, elimine as alternativas que descumprirem uma condição obrigatória. Exemplos de verificações:

- A linguagem, o runtime e suas dependências executam no sistema operacional, na arquitetura de processador e no ambiente de implantação autorizados?
- A persistência atende às garantias necessárias de integridade, durabilidade, concorrência, recuperação e retenção?
- A solução suporta os protocolos exigidos, como HTTP, gRPC, WebSockets, filas ou webhooks, com os limites previstos?
- Há mecanismos adequados para autenticação, autorização de recursos, isolamento de tenants, gestão de segredos, criptografia e auditoria?
- A licença da versão e da distribuição avaliadas, incluindo dependências críticas, é compatível com a política do produto e a forma de oferta do serviço?
- As versões necessárias terão suporte e um caminho viável de atualização durante o período planejado?
- É possível implantar, observar, operar e recuperar o serviço dentro do prazo e do orçamento disponíveis?

Uma pontuação alta em outros critérios não compensa a violação de uma restrição obrigatória. Mantenha requisitos ainda não verificados como pendências, sem apresentá-los como atendidos. Se nenhuma opção passar, registre o conflito e proponha o ajuste necessário no requisito ou nas alternativas.

## 3. Escolha a topologia e o processamento antes do nome do framework

Avalie o perfil das operações, distinguindo espera por I/O, trabalho de CPU, resposta interativa e execução em segundo plano. Um backend pode combinar uma API síncrona com workers e tarefas agendadas; dimensione cada parte conforme sua responsabilidade.

| Cenário identificado | Prioridade a confirmar | Alternativas a avaliar | Condição de escolha |
|---|---|---|---|
| API transacional e regras centrais do negócio | Consistência, clareza do domínio e velocidade de evolução | Monólito modular em Node.js/TypeScript, Java/Spring, C#/ASP.NET Core, Python/FastAPI ou Go, conforme a equipe | Usar como ponto de partida quando fronteiras de módulos e transações locais atenderem aos requisitos |
| Integrações lentas, notificações ou trabalho que possa terminar depois | Entrega durável, retentativas e capacidade de processamento | Workers com fila de tarefas, serviço de filas ou broker | Adotar quando houver requisito de execução assíncrona e uma política definida de falhas, idempotência e acompanhamento |
| Webhooks e APIs com demanda intermitente | Latência de entrada, escala e custo por execução | Funções orientadas a requisições ou eventos, como AWS Lambda, ou serviços gerenciados, como Cloud Run services | Verificar inicialização, limites de execução, concorrência, rede e conexões com a persistência |
| Processamento em lote ou agendamento com início e fim | Prazo de conclusão, repetição e recuperação de falhas | Jobs gerenciados, como Cloud Run jobs, ou processos agendados dedicados | Verificar duração, paralelismo, sobreposição de execuções e efeitos de retentativas |
| Domínios com equipes, escalas ou ciclos de entrega independentes | Autonomia e isolamento de responsabilidades e falhas | Serviços independentes ou extração gradual de módulos delimitados | Justificar a distribuição com uma necessidade concreta e capacidade para operar dados, rede, contratos e entregas separados |
| Leitura intensiva, relatórios ou busca especializada | Latência, custo das consultas e atualização dos resultados | Banco principal com consultas e índices adequados; cache, projeções ou mecanismo de busca quando necessários | Medir o comportamento e definir atualização, invalidação e defasagem tolerada antes de acrescentar armazenamentos |

Essas opções são candidatas, não resultados automáticos. A organização modular definida no [guia de arquitetura](arquitetura.md) deve orientar as fronteiras do código, enquanto a topologia define como seus processos e dependências serão executados. Acrescente serviços independentes quando o benefício justificar os custos de comunicação, consistência e operação.

### Persistência e garantias de dados

Avalie um banco relacional maduro, como PostgreSQL, como candidato inicial quando predominarem relações estruturadas, integridade e transações. Compare outras formas de persistência quando o modelo de acesso ou as restrições exigirem capacidades diferentes. Justifique cada armazenamento adicional e identifique o módulo dono dos dados.

Defina a atomicidade necessária por operação e a consistência entre processos e armazenamentos. Transações locais e integração com consistência eventual podem coexistir. Verifique isolamento, restrições e comportamento sob concorrência no banco escolhido; a [documentação de isolamento do PostgreSQL](https://www.postgresql.org/docs/current/transaction-iso.html), por exemplo, distingue as garantias de cada nível. Defina também backup, restauração e evolução do schema conforme os objetivos de recuperação.

### Tarefas, filas e eventos

Compare semântica, clientes e operação das alternativas. Uma biblioteca de tarefas, como [BullMQ](https://docs.bullmq.io/), um serviço de filas, como [SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html), e um broker, como [RabbitMQ](https://www.rabbitmq.com/docs), oferecem mecanismos e responsabilidades operacionais próprios. Avalie [Kafka](https://kafka.apache.org/intro/) quando o requisito envolver fluxos de eventos com retenção e releitura. Verifique os recursos da versão, da modalidade e da configuração efetivamente escolhidas.

Defina necessidade de ordenação, retenção, publicação confirmada, consumo, reprocessamento e tratamento de mensagens não processáveis. Dimensione atrasos e acúmulo de trabalho. Preserve a idempotência dos efeitos e a consistência entre dados e eventos conforme o guia de arquitetura; uma garantia de entrega do transporte precisa ser relacionada ao efeito completo da operação.

### Execução e operação

Confirme a modalidade da hospedagem. [Cloud Run services atende requisições, enquanto jobs executam trabalho até a conclusão](https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run). Em [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html), consulte as quotas da modalidade e da conta avaliadas. Valide a compatibilidade dos consumidores de fila com o modelo de execução e dimensione o total de conexões de banco considerando todas as instâncias e pools.

Escolha o framework conforme os mecanismos necessários. Em uma solução pequena, explicite composição de dependências, validação, tratamento de erros e contratos. Em um framework com essas capacidades integradas, use os recursos nativos preservando o núcleo de negócio independente do transporte e da persistência.

Compare o custo operacional completo: computação, banco, armazenamento, backups, rede, filas, observabilidade, ambientes de teste e trabalho de manutenção. Considere os picos, a retenção e as quotas dos serviços. Relacione as estimativas à carga e ao período avaliados; identifique premissas e incertezas.

## 4. Compare as candidatas com uma matriz ponderada

Quando houver alternativas viáveis e a comparação puder influenciar a decisão, selecione duas ou três que atendam ao mesmo escopo. Identifique os componentes e serviços incluídos em cada candidata para comparar custos e responsabilidades equivalentes. Use os pesos abaixo como ponto de partida e ajuste-os conforme o contexto, registrando a justificativa. A soma deve permanecer em 100.

Se restar uma única alternativa viável ou houver uma escolha organizacional obrigatória, registre a restrição, a evidência e os motivos de descarte das demais e dispense a matriz comparativa. Verifique ainda requisitos eliminatórios, compatibilidade, segurança, suporte, custos e evidências necessárias, e registre a decisão na ADR. Se a escolha obrigatória descumprir uma condição eliminatória, explicite o conflito conforme a etapa 2; a determinação organizacional não comprova a viabilidade técnica.

| Critério | Peso inicial | Evidência a reunir |
|---|---|---|
| Adequação ao domínio, aos dados e à carga | 25 | Garantias de consistência, concorrência, protocolos e limites verificados |
| Domínio e capacidade de manutenção pela equipe | 20 | Experiência real, continuidade, aprendizado e capacidade de diagnóstico |
| Produtividade e aderência à arquitetura modular | 15 | Esforço para implementar regras, contratos, validação, composição e testes |
| Custo e simplicidade operacional | 15 | Hospedagem, consumo de recursos, recuperação, atualização e serviços necessários |
| Risco de ecossistema e evolução | 15 | Governança, correções de segurança, compatibilidade e política de suporte |
| Qualidade demonstrada na validação | 10 | Resultados relevantes de integração, resiliência, latência e consumo de recursos |

Acrescente uma coluna por candidata, com notas de 0 a 5. Use 0 para não atender ao critério, 3 para atender adequadamente e 5 para uma adequação forte sustentada por evidência. Justifique as notas intermediárias. Marque **NE — não avaliado** quando faltar evidência, sem converter a ausência de dados em nota arbitrária.

```text
Pontuação final = soma(peso do critério × nota da candidata ÷ 5)
```

Calcule o resultado somente quando todos os critérios necessários estiverem avaliados. Registre fonte, data, condições e incertezas relevantes das evidências. Não invente benchmarks ou números para confirmar uma preferência prévia.

Use a pontuação para apoiar o julgamento. Se pequenas mudanças de peso inverterem o resultado, trate as opções como próximas e privilegie menor complexidade operacional, familiaridade e reversibilidade, conforme as restrições. Documente a razão da escolha final.

## 5. Audite o ecossistema antes de fechar a escolha

- **Manutenção e governança:** confira responsáveis, documentação, histórico de releases, correções de segurança, participação da comunidade e disponibilidade de suporte. Identifique quais recursos dependem de uma oferta comercial.
- **Ciclo de suporte:** registre versões e datas de fim de suporte de runtime, framework, banco e componentes críticos. Use LTS quando essa política existir e atender ao projeto. Consulte as políticas próprias de [Node.js](https://nodejs.org/en/about/previous-releases), [.NET](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core), [Go](https://go.dev/doc/devel/release), [Python](https://devguide.python.org/versions/) e [PostgreSQL](https://www.postgresql.org/support/versioning/), conforme a escolha. Reserve esforço para atualizações antes do fim do suporte.
- **Estabilidade e compatibilidade:** confira runtime, sistema operacional, arquitetura de processador, drivers, migrações, bibliotecas nativas, instrumentação e clientes das integrações. Diferencie as condições de suporte da comunidade, do fornecedor e da hospedagem contratada. Justifique o uso de recursos experimentais quando forem necessários.
- **Contratação e operação:** avalie o acesso real a profissionais, treinamento e ferramentas de diagnóstico. Considere quem responderá a incidentes e executará restaurações e atualizações.
- **Licenciamento e dependências:** confira o texto e as condições aplicáveis à versão, distribuição e modalidade de uso exatas, incluindo redistribuição e oferta do produto como serviço quando relevantes. Registre a evidência e encaminhe dúvidas à avaliação responsável da organização. Reavalie mudanças de licença ao atualizar componentes críticos.
- **Tipagem e validação:** favoreça contratos verificáveis e configure a checagem estática disponível no ecossistema. Em TypeScript, avalie configuração estrita; em Python, conecte um verificador de tipos ao fluxo de qualidade, pois [anotações não são impostas pelo runtime](https://docs.python.org/3/library/typing.html). Valide dados externos em tempo de execução na fronteira, independentemente da linguagem.

Quando já existir uma stack adequada e conhecida, exija um benefício concreto para substituí-la. Registre o custo de migração de código e dados, treinamento, coexistência e operação. Relacione o ganho esperado ao problema real e valide-o quando for decisivo.

## 6. Complete a stack com o mínimo necessário

Defina somente as responsabilidades aplicáveis. Aproveite as capacidades existentes do framework e da plataforma antes de acrescentar bibliotecas ou serviços:

| Camada | Decisão a tomar | Regra a aplicar |
|---|---|---|
| Linguagem, runtime e toolchain | Versões e ferramentas de compilação ou execução | Usar combinações suportadas, compatíveis com o destino e identificadas no desenvolvimento e no CI |
| Dependências | Gerenciador, resolução de versões e mecanismo de integridade | Usar lockfile, gestão de versões ou mecanismo equivalente do ecossistema, com instalação consistente e atualizações controladas |
| Framework e transporte | Servidor, roteamento e protocolos necessários | Manter adaptadores finos e o núcleo independente dos detalhes do framework |
| Persistência e migrações | Banco, driver, ORM ou query builder e ferramenta de evolução do schema | Versionar alterações, testar aplicação e recuperação e definir transações, concorrência, conexões e backups |
| Validação e contratos | Validador em runtime, descrição canônica e geração de artefatos | Validar na borda e manter uma fonte identificada para OpenAPI, AsyncAPI, schema GraphQL, Protobuf ou outro contrato necessário |
| Identidade e segurança | Provedor, sessão ou tokens, autorização, isolamento e limites de acesso | Escolher mecanismos compatíveis com os clientes e aplicar os controles do guia de arquitetura; gerenciar senhas próprias somente quando necessário |
| Configuração e segredos | Validação de ambiente, identidade de execução e cofre de segredos | Validar configuração na inicialização e injetar valores, com privilégios mínimos e estratégia de rotação |
| Cache e mensageria | Armazenamento temporário, fila, broker ou log de eventos, quando necessários | Definir invalidação, durabilidade, retenção e efeitos de retentativas conforme cada responsabilidade |
| Testes e verificações arquiteturais | Runner, dependências isoladas e ferramenta de fronteiras | Exercitar regras em memória, integrações com dependências reais isoladas e políticas de importação |
| Observabilidade | Logs, métricas, traces, coleta e destino dos dados | Preservar correlação, sanitização, retenção e limites de custo, com instrumentação compatível com a stack |
| Empacotamento e entrega | Pacote ou imagem, hospedagem e CI/CD | Produzir artefatos identificáveis e imutáveis para publicação, com configuração externa, verificações de saúde e encerramento apropriados ao destino |

Avalie a persistência com consultas representativas, incluindo operações críticas e relatórios. Escolha ORM, query builder ou acesso direto ao driver conforme os recursos e o controle necessários, preservando consultas seguras e o isolamento arquitetural. Planeje migrações compatíveis com a estratégia de entrega; evite sincronização automática de schema sem histórico e controle em produção.

Quando usar cache, defina quais dados podem ser descartados, sua defasagem tolerada e a invalidação. Se um armazenamento também sustentar tarefas duráveis, verifique isolamento, políticas de remoção, persistência e recuperação apropriados a essa responsabilidade.

Para testes de integração, avalie [Testcontainers](https://testcontainers.com/) ou dependências efêmeras equivalentes. Confirme o suporte da biblioteca, do runtime de contêineres e do ambiente de CI; mantenha a suíte proporcional ao risco e ao custo de execução.

Para observabilidade, avalie [OpenTelemetry](https://opentelemetry.io/docs/what-is-opentelemetry/) como mecanismo de instrumentação, coleta e exportação dos sinais necessários. Selecione também armazenamento, consulta e alertas. Verifique suporte das instrumentações, propagação de contexto, amostragem, dados sensíveis e custo da telemetria.

Use os princípios de configuração externa, separação entre build e execução e ciclo de vida de processos do [Twelve-Factor App](https://12factor.net/) quando aplicáveis ao modelo escolhido. Selecione a forma de implantação que a equipe consiga operar e recuperar, com os limites e serviços exigidos pelo produto.

Não instale ferramentas concorrentes para a mesma responsabilidade sem uma necessidade definida. Ao escolher um starter, confira manutenção, licença e configurações, remova componentes sem uso e valide a base resultante.

## 7. Faça uma prova curta quando houver risco decisivo

Defina a incerteza, o critério de sucesso e o limite de esforço antes de experimentar. Selecione o menor fluxo capaz de mudar a decisão, por exemplo:

1. Uma escrita e uma leitura passando por entrada, validação, caso de uso, transação e persistência, incluindo migração no banco escolhido.
2. Um fluxo assíncrono necessário ao produto, verificando publicação, retentativas, duplicação e idempotência dos efeitos.
3. Acesso a um recurso protegido, com autenticação, autorização, isolamento entre atores ou tenants e diagnóstico por logs ou traces.
4. Build do artefato de produção, execução em ambiente representativo e implantação de teste no destino previsto, incluindo rede, segredos e conexões.
5. Restauração ou evolução de dados quando recuperação e compatibilidade forem fatores decisivos.
6. Carga focalizada quando latência, throughput, concorrência ou consumo de recursos forem restrições críticas.

Meça os fatores relevantes à escolha, como latência p95/p99, taxa de erros, throughput, CPU, memória e tempo de build. Registre ambiente, volume de dados, duração, concorrência, amostra e metodologia. Quando inicialização afetar o resultado, diferencie execuções frias e aquecidas. Compare cenários equivalentes, com as integrações e garantias necessárias habilitadas.

Considere o comportamento dos pools, consultas, retentativas e limites da hospedagem ao interpretar os resultados. Benchmarks genéricos e exemplos promocionais não substituem a validação do fluxo representativo. Identifique quando a amostra ou o ambiente forem insuficientes para sustentar uma conclusão.

Não transforme toda decisão simples em um projeto de pesquisa. Faça a prova somente quando sua conclusão puder mudar a escolha e registre as limitações do que foi testado.

## 8. Registre o resultado antes de implementar a base

No projeto destino, registre uma ADR em `docs/arquitetura/adrs/NNNN-escolha-stack-backend.md`, respeitando a numeração existente e o [guia de documentação](documentação.md). Use esta composição:

```markdown
# ADR NNNN — Escolha da stack backend

- Status: [Proposta / Aceita, conforme a decisão real]
- Data e responsáveis: [Informações conhecidas]

## Contexto e restrições
[Produto, dados, carga, prazo, equipe, infraestrutura, recuperação e requisitos eliminatórios.]

## Alternativas avaliadas
[Candidatas viáveis, componentes incluídos, matriz quando aplicável, evidências e motivos de descarte das demais.]
[Quando houver uma única alternativa ou escolha obrigatória, registrar a restrição e a justificativa da decisão direta.]

## Decisão
[Linguagem, runtime, framework, persistência, contratos, segurança e hospedagem.]
[Cache, mensageria e demais componentes necessários, com versões e responsabilidades.]

## Consequências
[Custos e suas premissas, aprendizado, suporte, riscos, limites e estratégia de saída.]
[Impactos em dados, operação, atualizações e dependências de plataforma.]

## Validação e revisão
[Verificações executadas, resultados, fontes, datas, pendências e condições de revisão.]
```

Não marque uma proposta como aceita sem a decisão correspondente. Se houver uma escolha condicionada, explicite o dado pendente, a responsabilidade pela validação e o impacto no escopo. Identifique componentes adiados ou opcionais sem apresentá-los como já adotados. No resumo técnico do projeto, vincule a ADR em vez de repetir toda a avaliação.

## 9. Confira a decisão entregue

Antes de gerar a base do projeto, confirme que:

- Todas as restrições obrigatórias foram atendidas ou os conflitos e impedimentos estão explicitados.
- Cada tecnologia escolhida tem uma responsabilidade e uma justificativa verificável.
- Topologia, processamento, persistência e comunicação atendem às garantias do domínio e aos limites de operação.
- Linguagem, runtime, framework, drivers, migrações, contratos e instrumentação são compatíveis entre si e com a hospedagem.
- Versões, licenças, suporte e caminho de atualização foram conferidos na data da decisão.
- Autorização, isolamento, gestão de segredos e demais controles de segurança têm mecanismos definidos.
- Custos, recuperação e capacidade de manutenção são compatíveis com o contexto informado.
- Evidências, testes realizados, hipóteses e pendências estão identificados na ADR.
- A decisão permite aplicar os guias de [arquitetura](arquitetura.md) e [documentação](documentação.md), com as adaptações da stack registradas.

Após a decisão, gere somente a base necessária e configure seus comandos reais de desenvolvimento, tipagem ou compilação, lint, testes, migrações e build. Conecte os checks aplicáveis de arquitetura, segurança e documentação ao CI e à política de merge. Identifique os artefatos e as versões entregues; mantenha o fluxo de atualização de dependências e recuperação documentado.

## Referências de manutenção

As regras acima permitem aplicar o guia diretamente. Use as fontes oficiais para conferir capacidades, compatibilidade e ciclos de suporte no momento da escolha, sem tratar esta lista como um ranking de mercado.

- [Twelve-Factor App — princípios para aplicações executadas como serviço](https://12factor.net/)
- [PostgreSQL — política de versões e suporte](https://www.postgresql.org/support/versioning/)
- [PostgreSQL — níveis de isolamento transacional](https://www.postgresql.org/docs/current/transaction-iso.html)
- [OpenTelemetry — instrumentação, coleta e exportação de telemetria](https://opentelemetry.io/docs/what-is-opentelemetry/)
- [OWASP — Cheat Sheet Series para controles de segurança](https://cheatsheetseries.owasp.org/)
- [Testcontainers — dependências de teste em contêineres](https://testcontainers.com/)
- [Node.js — versões e política de releases](https://nodejs.org/en/about/previous-releases)
- [Spring Boot — requisitos de runtime e ferramentas](https://docs.spring.io/spring-boot/system-requirements.html)
- [.NET — política de suporte](https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core)
- [FastAPI — documentação oficial](https://fastapi.tiangolo.com/)
- [Python — situação de suporte das versões](https://devguide.python.org/versions/)
- [Python — anotações e verificação de tipos](https://docs.python.org/3/library/typing.html)
- [Go — releases e política de suporte](https://go.dev/doc/devel/release)
- [Cloud Run — serviços, jobs e modelos de execução](https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run)
- [AWS Lambda — quotas de execução e concorrência](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html)
