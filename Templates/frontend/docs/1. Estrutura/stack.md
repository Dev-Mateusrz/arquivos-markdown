Atualizado: 10/11/2026
# Escolha da stack de tecnologia de um projeto frontend

Ao iniciar um projeto frontend, siga esta sequência para escolher as tecnologias conforme os requisitos do produto, da equipe e da operação. Produza uma decisão justificada antes de gerar o projeto ou instalar dependências. Os critérios abaixo são a política desta base; não representam uma stack obrigatória para todos os sistemas.

## 1. Levante as quatro dimensões de restrição

Leia os requisitos e as decisões já fornecidas. Em um projeto existente, identifique também a stack, os contratos e as limitações atuais antes de propor substituições.

| Dimensão | O que identificar | Como usar na escolha |
|---|---|---|
| Produto e requisitos de qualidade | Público, rotas indexáveis, interatividade, atualização de conteúdo, dispositivos, acessibilidade, desempenho, integrações e necessidades offline | Determinar a estratégia de renderização e as capacidades necessárias |
| Prazo e velocidade de entrega | Data ou janela de entrega, escopo do MVP, integrações prioritárias e disponibilidade para configurar infraestrutura | Favorecer soluções conhecidas ou integradas quando reduzirem trabalho comprovadamente necessário |
| Equipe e manutenção | Experiência efetiva, pessoas disponíveis, continuidade, treinamento e quem operará a solução | Considerar produtividade, aprendizado e capacidade de manutenção ao longo do projeto |
| Orçamento e infraestrutura | Hospedagem permitida, runtimes disponíveis, limites de operação, serviços existentes e previsão de uso | Excluir opções incompatíveis e estimar o custo completo das alternativas viáveis |

Registre fatos, hipóteses e pendências separadamente. Reaproveite respostas já existentes. Quando faltar uma restrição capaz de mudar a decisão, solicite o dado necessário; avance na avaliação das partes independentes sem inventar orçamento, prazo ou competências da equipe.

## 2. Separe requisitos eliminatórios de preferências

Antes de pontuar tecnologias, elimine as alternativas que descumprirem uma condição obrigatória. Exemplos de verificações:

- A solução executa no ambiente e no runtime autorizados?
- Suporta os navegadores, os dispositivos e as integrações exigidos?
- Atende ao mecanismo de autenticação, aos limites de exposição de dados e às condições de acesso do projeto?
- Sua licença e suas dependências são compatíveis com as políticas aplicáveis?
- Permite entregar o conteúdo e a experiência exigidos para cada rota?
- Há um caminho viável para implantação, manutenção e atualização no prazo disponível?

Uma pontuação alta em outros critérios não compensa a violação de uma restrição obrigatória. Se nenhuma opção passar, registre o conflito e proponha o ajuste necessário no requisito ou nas alternativas.

## 3. Escolha a estratégia de aplicação antes do nome do framework

Avalie as necessidades por área ou rota. Um produto pode reunir páginas públicas pré-renderizadas e uma aplicação autenticada interativa; não force todas as rotas a usar a mesma estratégia.

| Cenário identificado | Prioridade a confirmar | Alternativas a avaliar | Condição de escolha |
|---|---|---|---|
| Dashboard ou aplicação autenticada | Interatividade, integração com serviços e fluxo de acesso | SPA com a biblioteca conhecida pela equipe e Vite; ou framework com roteamento e dados integrados | Escolher SPA quando o funcionamento no cliente e a infraestrutura disponível atenderem ao produto; avaliar o esforço de montar roteamento e dados |
| Portal público, conteúdo editorial ou marketing | Descoberta, conteúdo inicial, metadados e frequência de atualização | SSG/pré-renderização; SSR quando necessário; Next.js ou Nuxt conforme o ecossistema adotado | Relacionar renderização à atualização e à personalização do conteúdo, sem exigir um servidor por padrão |
| E-commerce ou produto com áreas públicas e privadas | Catálogo indexável, atualização, personalização e experiência transacional | Estratégia híbrida com renderização e cache adequados a cada área | Validar catálogo, preço, disponibilidade e checkout separadamente |
| Widget ou ferramenta embutida | Peso do código, integração com a página hospedeira e compatibilidade | Web Components, Svelte ou solução pequena compatível com o host | Medir o artefato real e validar estilos, eventos e dependências na integração |
| Múltiplas aplicações com entregas independentes | Autonomia de equipes, contratos e operação separada | Microfrontends somente quando essa separação justificar a complexidade | Não adotar microfrontends apenas para obter um bundle pequeno |

Essas opções são candidatas, não resultados automáticos. Uma aplicação autenticada pode ter páginas públicas que exigem indexação; um site público pode ser atendido por conteúdo estático. SEO e desempenho dependem também de conteúdo, metadados, carregamento e configuração, não apenas do nome do framework.

Na avaliação de React, inclua as opções de framework recomendadas pela [documentação oficial](https://react.dev/learn/creating-a-react-app). Vite é uma ferramenta de build e desenvolvimento: ao usá-lo como base de uma SPA, explicite as escolhas adicionais de roteamento, dados e testes.

Confirme os recursos de cada opção na versão avaliada. [Next.js permite exportação estática](https://nextjs.org/docs/app/guides/static-exports) com limitações para recursos que dependem de execução dinâmica; [Nuxt oferece modos de renderização distintos](https://nuxt.com/docs/4.x/guide/concepts/rendering). Renderização híbrida não significa que ambos ofereçam os mesmos recursos específicos de React Server Components.

Se houver apenas hospedagem estática, não escolha uma solução que dependa de SSR por requisição ou de um BFF nesse mesmo destino. Se houver execução dinâmica, confirme runtime, adaptador, cache e serviços suportados. Compare também custos de build, armazenamento, tráfego, APIs, autenticação, observabilidade e manutenção; não presuma um custo fixo ou irrelevante.

## 4. Compare as candidatas com uma matriz ponderada

Selecione duas ou três alternativas viáveis. Use os pesos abaixo como ponto de partida e ajuste-os conforme o contexto, registrando a justificativa. A soma deve permanecer em 100.

| Critério | Peso inicial | Evidência a reunir |
|---|---|---|
| Adequação ao produto e à renderização necessária | 25 | Requisitos, limitações e capacidades verificadas |
| Domínio e capacidade de manutenção pela equipe | 20 | Experiência real, disponibilidade e treinamento necessário |
| Esforço para entregar o escopo | 15 | Funcionalidades integradas, lacunas e trabalho de configuração |
| Custo e viabilidade operacional | 15 | Modelo de implantação, previsão de uso e serviços necessários |
| Risco de ecossistema e evolução | 15 | Suporte, compatibilidade, governança e estratégia de atualização |
| Qualidade demonstrada na validação | 10 | Compatibilidade, acessibilidade, desempenho e resultados relevantes ao caso |

Acrescente uma coluna por candidata, com notas de 0 a 5. Use 0 para não atender ao critério, 3 para atender adequadamente e 5 para uma adequação forte sustentada por evidência. Justifique as notas intermediárias. Marque **NE — não avaliado** quando faltar evidência, sem converter a ausência de dados em nota arbitrária.

```text
Pontuação final = soma(peso do critério × nota da candidata ÷ 5)
```

Calcule o resultado somente quando todos os critérios necessários estiverem avaliados. Registre a fonte, a data e as incertezas relevantes das evidências. Não invente números para confirmar uma preferência prévia.

Use a pontuação para apoiar o julgamento. Se pequenas mudanças de peso inverterem o resultado, trate as opções como próximas e privilegie menor complexidade, familiaridade e reversibilidade, conforme as restrições do projeto. Documente a razão da escolha final.

## 5. Audite o ecossistema antes de fechar a escolha

- **Manutenção e governança:** confira atividade, histórico de versões, documentação, responsáveis, contribuição, suporte e tratamento de problemas. Patrocínio corporativo é um sinal, não uma garantia de continuidade.
- **Estabilidade e compatibilidade:** confira releases suportadas, requisitos de runtime, plugins necessários, histórico de mudanças incompatíveis e caminho de atualização. Não adote uma versão experimental sem justificar o risco.
- **Contratação e aprendizado:** avalie o acesso real a profissionais e treinamento no contexto da organização. Não use rankings genéricos de popularidade para presumir disponibilidade ou custo de contratação.
- **Licenciamento e dependências:** confirme condições de uso, dependências críticas e compatibilidade com o projeto. Registre dúvidas que precisem de avaliação da organização.
- **Tipagem:** adote TypeScript como padrão desta base, com verificação estrita compatível com a stack. Prefira ferramentas com tipos mantidos e APIs bem definidas; avalie o custo de adaptar ou isolar uma dependência sem boa tipagem antes de incorporá-la.

Quando já existir uma base tecnológica adequada e conhecida, exija um benefício concreto para substituí-la. Registre também o custo de migração e de coexistência. Uma tecnologia diferente pode ser escolhida quando resolver uma necessidade relevante que compense esse custo.

## 6. Complete a stack com o mínimo necessário

| Camada | Decisão a tomar | Regra a aplicar |
|---|---|---|
| Linguagem e tipos | TypeScript, suas configurações e geração de contratos | Habilitar checagem de tipos no fluxo de qualidade e validar dados externos em tempo de execução quando necessário |
| Framework e roteamento | Solução compatível com a renderização e a experiência da equipe | Usar os mecanismos nativos antes de adicionar um segundo roteador ou modelo de execução |
| Build e desenvolvimento | Ferramenta suportada pelo framework e pelos plugins necessários | Usar a integração oficial; comparar Vite, Turbopack ou Rspack apenas quando forem alternativas reais para aquela stack |
| Runtime de execução | Necessidade de servidor e runtime suportado pela hospedagem | Separar o runtime usado para construir o projeto daquele necessário para executar a aplicação publicada |
| Dependências | Gerenciador e lockfile | Usar uma escolha consistente entre desenvolvimento e CI, com instalação reproduzível e versões identificadas |
| Estilização e componentes | Abordagem de CSS, tokens, tema e biblioteca visual | Considerar experiência da equipe, acessibilidade, encapsulamento, licença e compatibilidade com a renderização |
| Dados e estado | Mecanismo do framework, cache de dados e estado de cliente | Acrescentar bibliotecas somente para responsabilidades necessárias, respeitando o guia de arquitetura |
| Formulários e validação | Recursos nativos e ferramentas adicionais, quando justificadas | Compatibilizar experiência do usuário, validação de dados e tipos sem duplicar regras |
| Qualidade e operação | Lint, tipagem, testes, build e observabilidade | Escolher ferramentas que funcionem juntas no ambiente de desenvolvimento e no CI |

Adote o bundler suportado pelo framework antes de propor uma troca. Não substitua uma configuração de Webpack apenas pela idade da ferramenta: avalie os problemas existentes, o ganho medido e o custo da migração. Não prometa um tempo de build sem medir o projeto representativo.

Para um repositório novo sem política de dependências, avalie pnpm como candidato para instalação e workspaces. npm continua sendo uma opção válida, inclusive com instalação reproduzível por `npm ci`. Se considerar Bun, avalie separadamente seu uso como gerenciador e como runtime, verificando a compatibilidade necessária em cada papel. Não presuma que pnpm e Bun tenham a mesma implementação de armazenamento.

Tailwind e CSS Modules são candidatas de estilização; escolha a que atender aos requisitos e à manutenção do produto. Compare o CSS efetivamente produzido, o compartilhamento de tokens, os temas e a integração com a biblioteca visual. Nenhuma abordagem garante, sozinha, um bundle mínimo, boa acessibilidade ou ausência de conflitos.

Não instale simultaneamente ferramentas concorrentes para a mesma responsabilidade sem uma necessidade definida. Ao escolher um boilerplate, confira manutenção, licença, dependências e configurações; remova módulos desnecessários e valide o resultado.

## 7. Faça uma prova curta quando houver risco decisivo

Defina o objetivo e o limite de esforço antes de experimentar. Valide o menor fluxo capaz de resolver a incerteza, por exemplo:

1. Uma rota pública ou autenticada com a estratégia de renderização pretendida.
2. Uma integração real ou representativa, incluindo carregamento e falha.
3. Um formulário ou interação relevante para validar a biblioteca visual e a tipagem.
4. Build e publicação de teste no destino previsto, com as condições de acesso adequadas.
5. Uma verificação dos navegadores, do teclado e das métricas que forem decisivas para o projeto.

Meça inicialização, recarregamento, build e tamanho dos artefatos quando esses fatores influenciarem a escolha. Compare cenários equivalentes, indicando ambiente e metodologia. Exemplos promocionais e benchmarks de terceiros não substituem a validação da integração necessária.

Não transforme toda decisão simples em um projeto de pesquisa. Faça a prova somente quando sua conclusão puder mudar a escolha e registre as limitações do que foi testado.

## 8. Registre o resultado antes de implementar a base

No projeto destino, registre uma ADR em `docs/arquitetura/adrs/NNNN-escolha-stack-frontend.md`, respeitando a numeração existente. Use esta composição:

```markdown
# ADR NNNN — Escolha da stack frontend

- Status: [Proposta / Aceita, conforme a decisão real]
- Data e responsáveis: [Informações conhecidas]

## Contexto e restrições
[Produto, prazo, equipe, infraestrutura e requisitos eliminatórios.]

## Alternativas avaliadas
[Candidatas viáveis, matriz, evidências e motivos de descarte das demais.]

## Decisão
[Framework, linguagem, renderização por área, build, runtime e ferramentas necessárias.]

## Consequências
[Custos, aprendizado, riscos, limitações, dependências de plataforma e alternativas de saída.]

## Validação e revisão
[Verificações executadas, pendências e condições que justificariam revisar a escolha.]
```

Não marque uma proposta como aceita sem a decisão correspondente. Se houver uma escolha ainda condicionada, explicite o dado pendente e o impacto. No resumo técnico do projeto, vincule a ADR em vez de repetir toda a avaliação.

## 9. Confira a decisão entregue

Antes de gerar a base do projeto, confirme que:

- Todas as restrições obrigatórias foram atendidas ou os conflitos foram explicitados.
- Cada tecnologia escolhida tem uma responsabilidade e uma justificativa verificável.
- A estratégia de renderização funciona no ambiente de implantação previsto.
- Framework, build, runtime, bibliotecas e gerenciador são compatíveis entre si.
- Versões e suporte foram conferidos no momento da decisão; não foram copiados sem revisão de uma recomendação antiga.
- As estimativas, os testes realizados e as incertezas estão identificados.
- A decisão permite aplicar os guias de [arquitetura](arquitetura.md) e [documentação](documentação.md).

Após a decisão, gere somente a base necessária e configure seus comandos reais de desenvolvimento, tipagem, lint, testes e build. No Vite, transpilar TypeScript não substitui a checagem de tipos: configure a verificação correspondente no fluxo de qualidade.

## Referências de manutenção

As regras acima permitem aplicar o guia diretamente. Use as fontes oficiais para verificar capacidades e compatibilidade das versões avaliadas, sem tratar esta lista como um ranking de mercado.

- [React — opções para criar aplicações](https://react.dev/learn/creating-a-react-app)
- [Next.js — exportação estática e limitações](https://nextjs.org/docs/app/guides/static-exports)
- [Nuxt — modos de renderização](https://nuxt.com/docs/4.x/guide/concepts/rendering)
- [Vite — ferramenta de desenvolvimento e build](https://vite.dev/guide/)
- [Vite — TypeScript e checagem de tipos](https://vite.dev/guide/features#typescript)
- [TypeScript — configuração strict](https://www.typescriptlang.org/tsconfig/strict.html)
- [pnpm — motivação e armazenamento](https://pnpm.io/motivation)
- [npm — instalação reproduzível com npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci/)
- [Bun — compatibilidade do runtime com Node.js](https://bun.sh/docs/runtime/nodejs-compat)
- [Web Components — recursos da plataforma](https://developer.mozilla.org/en-US/docs/Web/API/Web_components)
