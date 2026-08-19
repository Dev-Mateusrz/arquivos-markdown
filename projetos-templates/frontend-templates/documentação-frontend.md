# Documentação Técnica do Front-End — {{NOME_DO_SISTEMA}}

## Aspectos Tecnológicos da Interface do Usuário

> **Template reutilizável.** Copie este arquivo para `docs/DOCUMENTACAO_FRONTEND.md`, substitua os `{{PLACEHOLDERS}}` e apague os blocos `<!-- guia: ... -->` e a seção "Como adaptar este template" ao final. Seções que não se aplicam ao projeto devem ser **removidas**, não deixadas vazias — e o Sumário renumerado.

---

## Sumário

1. [Introdução](#1-introdução)
2. [Arquitetura Geral do Front-End](#2-arquitetura-geral-do-front-end)
3. [Stack Tecnológica](#3-stack-tecnológica)
   - 3.1 [Biblioteca de UI e Linguagem](#31-biblioteca-de-ui-e-linguagem)
   - 3.2 [Bundler e Dev Server](#32-bundler-e-dev-server)
   - 3.3 [Estilização e Sistema de Design](#33-estilização-e-sistema-de-design)
   - 3.4 [Biblioteca de Componentes](#34-biblioteca-de-componentes)
4. [Estrutura de Diretórios e Organização do Código](#4-estrutura-de-diretórios-e-organização-do-código)
5. [Sistema de Roteamento](#5-sistema-de-roteamento)
   - 5.1 [Configuração de Rotas](#51-configuração-de-rotas)
   - 5.2 [Rotas Protegidas e Controle de Acesso](#52-rotas-protegidas-e-controle-de-acesso)
6. [Gerenciamento de Estado](#6-gerenciamento-de-estado)
   - 6.1 [Estado Global](#61-estado-global)
   - 6.2 [Estado do Servidor](#62-estado-do-servidor)
   - 6.3 [Estado de Contexto](#63-estado-de-contexto)
7. [Sistema de Autenticação e Segurança](#7-sistema-de-autenticação-e-segurança)
   - 7.1 [Fluxo de Autenticação](#71-fluxo-de-autenticação)
   - 7.2 [Gerenciamento de Tokens](#72-gerenciamento-de-tokens)
   - 7.3 [Armazenamento de Credenciais no Cliente](#73-armazenamento-de-credenciais-no-cliente)
   - 7.4 [Renovação Automática de Tokens](#74-renovação-automática-de-tokens)
   - 7.5 [Sistema de Permissões](#75-sistema-de-permissões)
8. [Camada de Serviços e Comunicação com API](#8-camada-de-serviços-e-comunicação-com-api)
   - 8.1 [Configuração do Cliente HTTP](#81-configuração-do-cliente-http)
   - 8.2 [Interceptadores de Requisição e Resposta](#82-interceptadores-de-requisição-e-resposta)
   - 8.3 [Serviço de Autenticação](#83-serviço-de-autenticação)
   - 8.4 [Serviços de Domínio](#84-serviços-de-domínio)
9. [Tipagem e Contratos de Dados](#9-tipagem-e-contratos-de-dados)
10. [Componentes e Interface do Usuário](#10-componentes-e-interface-do-usuário)
    - 10.1 [Componentes de Layout](#101-componentes-de-layout)
    - 10.2 [Sistema de Navegação](#102-sistema-de-navegação)
    - 10.3 [Biblioteca de Componentes UI](#103-biblioteca-de-componentes-ui)
    - 10.4 [Componentes Personalizados](#104-componentes-personalizados)
11. [Páginas da Aplicação](#11-páginas-da-aplicação)
12. [Validação de Formulários](#12-validação-de-formulários)
13. [Sistema de Logging](#13-sistema-de-logging)
14. [Responsividade e Experiência Mobile](#14-responsividade-e-experiência-mobile)
15. [Containerização e Deploy](#15-containerização-e-deploy)
    - 15.1 [Docker e Multi-Stage Build](#151-docker-e-multi-stage-build)
    - 15.2 [Servidor Web de Produção](#152-servidor-web-de-produção)
    - 15.3 [Orquestração de Containers](#153-orquestração-de-containers)
16. [Variáveis de Ambiente e Configuração](#16-variáveis-de-ambiente-e-configuração)
17. [Qualidade de Código e Ferramentas de Desenvolvimento](#17-qualidade-de-código-e-ferramentas-de-desenvolvimento)
18. [Considerações Finais](#18-considerações-finais)
19. [Serviços de Backend Consumidos](#19-serviços-de-backend-consumidos)
    - 19.1 [Visão Geral do Serviço](#191-visão-geral-do-serviço)
    - 19.2 [Endpoints e Recursos Expostos](#192-endpoints-e-recursos-expostos)
    - 19.3 [Modelo de Permissões](#193-modelo-de-permissões)
    - 19.4 [Estrutura de Respostas da API](#194-estrutura-de-respostas-da-api)
    - 19.5 [Tokens e Sessões](#195-tokens-e-sessões)
20. [Relação entre o Front-End e os Backends](#20-relação-entre-o-front-end-e-os-backends)
    - 20.1 [Arquitetura de Comunicação](#201-arquitetura-de-comunicação)
    - 20.2 [Instâncias de Cliente HTTP Separadas](#202-instâncias-de-cliente-http-separadas)
    - 20.3 [Fluxo Completo de Registro e Provisionamento](#203-fluxo-completo-de-registro-e-provisionamento)
    - 20.4 [Fluxo Completo de Login e Sincronização](#204-fluxo-completo-de-login-e-sincronização)
    - 20.5 [Mapeamento de Dados entre Backends](#205-mapeamento-de-dados-entre-backends)
    - 20.6 [Sincronização de Entidades (Upsert)](#206-sincronização-de-entidades-upsert)
    - 20.7 [Renovação de Tokens e Propagação](#207-renovação-de-tokens-e-propagação)
    - 20.8 [Operações com Escrita Dupla](#208-operações-com-escrita-dupla)

---

<details>
<summary><b>Placeholders deste template</b> (apagar depois de preencher)</summary>

| Placeholder | Significado |
|---|---|
| `{{NOME_DO_SISTEMA}}` | Nome do sistema |
| `{{ORGANIZACAO}}` | Organização/área responsável |
| `{{OBJETIVO_DO_SISTEMA}}` | O que o sistema faz, em uma frase |
| `{{LIB_UI}}` / `{{VERSAO_LIB_UI}}` | Biblioteca de UI e versão |
| `{{LINGUAGEM}}` | Linguagem principal do front-end |
| `{{BUNDLER}}` | Ferramenta de build/dev server |
| `{{FRAMEWORK_CSS}}` | Framework/estratégia de estilização |
| `{{LIB_COMPONENTES}}` / `{{LIB_PRIMITIVOS}}` | Sistema de componentes e primitivos |
| `{{LIB_ROTEAMENTO}}` | Biblioteca de roteamento |
| `{{LIB_ESTADO_GLOBAL}}` / `{{LIB_ESTADO_SERVIDOR}}` | Gerenciamento de estado |
| `{{CLIENTE_HTTP}}` | Cliente HTTP |
| `{{LIB_FORMULARIO}}` / `{{LIB_VALIDACAO}}` | Formulários e validação |
| `{{PROVEDOR_AUTH}}` | Provedor de identidade |
| `{{ENTIDADE_PRINCIPAL}}` | Entidade central do domínio |
| `{{PREFIXO_VAR_AMBIENTE}}` | Prefixo das variáveis expostas ao cliente |
| `{{SERVIDOR_WEB}}` | Servidor de arquivos estáticos em produção |
| `{{GERENCIADOR_PACOTES}}` | Gerenciador de pacotes |

</details>

---

## 1. Introdução

O **{{NOME_DO_SISTEMA}}** é uma aplicação web para {{OBJETIVO_DO_SISTEMA}}, desenvolvida no contexto da {{ORGANIZACAO}}. O front-end da aplicação foi construído como uma *{{TIPO_APLICACAO}}* (ex: Single Page Application — SPA), utilizando tecnologias amplamente adotadas pelo mercado e pela comunidade de desenvolvimento web.

Este documento descreve, de forma técnica e detalhada, os aspectos tecnológicos que compõem a camada de interface do usuário (*front-end*) do sistema {{NOME_DO_SISTEMA}}, abordando a arquitetura de software, as bibliotecas e frameworks empregados, os padrões de projeto adotados, os mecanismos de segurança implementados e a infraestrutura de deploy.

<!-- guia: este documento descreve o que existe, não o que se pretende construir. Se uma seção descreve um plano, marque explicitamente como "Previsto" ou remova. -->

---

## 2. Arquitetura Geral do Front-End

A arquitetura do front-end do {{NOME_DO_SISTEMA}} segue o modelo de **{{TIPO_APLICACAO}}**, na qual {{DESCRICAO_MODELO_RENDERIZACAO}}.

A aplicação adota uma **arquitetura em camadas**, organizada da seguinte forma:

```
┌──────────────────────────────────────────────────────┐
│                    Camada de Apresentação             │
│          (Páginas, Componentes, Layout, UI)           │
├──────────────────────────────────────────────────────┤
│                  Camada de Gerenciamento de Estado    │
│      ({{LIB_ESTADO_GLOBAL}}, {{LIB_ESTADO_SERVIDOR}}) │
├──────────────────────────────────────────────────────┤
│                    Camada de Serviços                 │
│        ({{CLIENTE_HTTP}}, Auth Service, API Service)  │
├──────────────────────────────────────────────────────┤
│                    Camada de Tipos                    │
│              (Interfaces e Contratos)                 │
├──────────────────────────────────────────────────────┤
│                Camada de Utilitários                  │
│           (Logger, Cookies, Formatação)               │
└──────────────────────────────────────────────────────┘
```

O ponto de entrada da aplicação (`{{ARQUIVO_ENTRADA}}`) estabelece a hierarquia de provedores (*providers*) que envolvem toda a árvore de componentes:

```
{{PROVIDER_RAIZ}}
  └── {{PROVIDER_ROTEAMENTO}}      (Roteamento)
       └── {{PROVIDER_CACHE}}        (Cache de dados do servidor)
            └── {{PROVIDER_AUTH}}      (Contexto de autenticação)
                 └── App                (Componente raiz com rotas)
```

Essa hierarquia garante que todos os componentes da aplicação tenham acesso ao sistema de roteamento, ao cache de dados do servidor e ao contexto de autenticação do usuário.

---

## 3. Stack Tecnológica

### 3.1 Biblioteca de UI e Linguagem

O front-end é construído sobre o **{{LIB_UI}}** (`{{PACOTE_LIB_UI}}: {{VERSAO_LIB_UI}}`) com **{{LINGUAGEM}}**.

<!-- guia: descreva o paradigma real (componentes funcionais + hooks, componentes de classe, composition API, signals) e liste os recursos mais usados no projeto. -->

O projeto utiliza {{PARADIGMA_COMPONENTES}}. Os recursos mais utilizados na aplicação incluem:

- **`{{RECURSO_1}}`**: {{DESCRICAO_RECURSO_1}}
- **`{{RECURSO_2}}`**: {{DESCRICAO_RECURSO_2}}
- **`{{RECURSO_3}}`**: {{DESCRICAO_RECURSO_3}}

A configuração de {{LINGUAGEM}} adota **modo estrito**, garantindo verificação de tipos em tempo de compilação e reduzindo a classe de erros que chega a produção.

### 3.2 Bundler e Dev Server

O **{{BUNDLER}}** (`{{VERSAO_BUNDLER}}`) é responsável pelo build e pelo servidor de desenvolvimento, oferecendo:

- **{{BENEFICIO_BUNDLER_1}}**;
- **{{BENEFICIO_BUNDLER_2}}**;
- **Hot Module Replacement (HMR)**: atualização de módulos sem recarregar a página;
- **Build de produção otimizado**: minificação, *tree-shaking* e *code splitting*.

### 3.3 Estilização e Sistema de Design

A estilização utiliza **{{FRAMEWORK_CSS}}** (`{{VERSAO_FRAMEWORK_CSS}}`), com {{ESTRATEGIA_DESIGN_TOKENS}}.

<!-- guia: registre aqui as decisões que um novo dev não descobriria lendo o código: onde ficam os tokens de cor, o que é permitido sobrescrever, se há dark mode. -->

### 3.4 Biblioteca de Componentes

O projeto utiliza o **{{LIB_COMPONENTES}}** como sistema de componentes. Os componentes são baseados no **{{LIB_PRIMITIVOS}}**, uma biblioteca de primitivos de interface (*headless UI*) que fornece:

- **Acessibilidade nativa**: os componentes seguem as especificações WAI-ARIA.
- **Comportamento sem estilo**: os componentes fornecem apenas a lógica de interação, deixando a estilização livre.
- **Composição**: componentes são construídos por composição de primitivos menores.

A aplicação utiliza os seguintes primitivos:

| Primitivo | Finalidade |
|-----------|------------|
| `{{PRIMITIVO_1}}` | {{USO_PRIMITIVO_1}} |
| `{{PRIMITIVO_2}}` | {{USO_PRIMITIVO_2}} |
| `{{PRIMITIVO_3}}` | {{USO_PRIMITIVO_3}} |

---

## 4. Estrutura de Diretórios e Organização do Código

O código-fonte do front-end está organizado dentro do diretório `{{PASTA_SRC}}`, seguindo uma estrutura baseada em **separação por responsabilidade funcional**:

```
src/
├── {{ARQUIVO_ENTRADA}}       # Ponto de entrada da aplicação
├── App.{{EXT}}               # Definição de rotas e componente raiz
├── index.css                 # Estilos globais e variáveis CSS
│
├── assets/                   # Recursos estáticos
│
├── components/               # Componentes reutilizáveis
│   ├── layout.{{EXT}}        # Layout principal
│   ├── ...
│   └── ui/                   # Componentes de base do design system
│
├── hooks/                    # Hooks/composables customizados
│
├── lib/                      # Bibliotecas e utilitários transversais
│   ├── utils.{{EXT}}         # Helpers genéricos
│   ├── logger.{{EXT}}        # Sistema de logging estruturado
│   └── auth/                 # Módulo de autenticação
│
├── pages/                    # Páginas/telas da aplicação
│
├── routes/                   # Definições e guardas de rota
│
├── services/                 # Serviços de comunicação com APIs
│
├── types/                    # Definições de tipos e contratos
│
└── utils/                    # Funções utilitárias de domínio
```

<!-- guia: cole a árvore real (ex: `tree -L 2 src`) e comente apenas as pastas cuja finalidade não é óbvia pelo nome. -->

---

## 5. Sistema de Roteamento

### 5.1 Configuração de Rotas

O roteamento é implementado com o **{{LIB_ROTEAMENTO}}** (`{{VERSAO_LIB_ROTEAMENTO}}`).

A aplicação define as seguintes rotas:

| Rota | Componente | Proteção | Descrição |
|------|-----------|----------|-----------|
| `/` | `{{COMPONENTE_RAIZ}}` | — | Redirecionamento automático |
| `{{ROTA_1}}` | `{{COMPONENTE_1}}` | Autenticado | {{DESCRICAO_ROTA_1}} |
| `{{ROTA_2}}` | `{{COMPONENTE_2}}` | Autenticado + {{PAPEL}} | {{DESCRICAO_ROTA_2}} |
| `{{ROTA_LOGIN}}` | `{{COMPONENTE_LOGIN}}` | Pública | Formulário de login |
| `{{ROTA_REGISTRO}}` | `{{COMPONENTE_REGISTRO}}` | Pública | Formulário de registro |

As rotas protegidas são envolvidas pelo componente `{{COMPONENTE_ROTA_PRIVADA}}` e pelo layout padrão, que fornece a estrutura visual com navegação e cabeçalho.

### 5.2 Rotas Protegidas e Controle de Acesso

O componente `{{COMPONENTE_ROTA_PRIVADA}}` implementa um mecanismo de **controle de acesso baseado em papéis** (RBAC — *Role-Based Access Control*). A cada requisição de navegação, o componente:

1. **Verifica a existência de um token válido** no armazenamento do navegador.
2. **Decodifica o payload do token** para extrair o nível de permissão do usuário.
3. **Aplica regras de acesso** baseadas no papel do usuário:

| Permissão | Código | Acesso |
|-----------|--------|--------|
| {{PAPEL_1}} | {{CODIGO_1}} | {{ACESSO_1}} |
| {{PAPEL_2}} | {{CODIGO_2}} | {{ACESSO_2}} |
| {{PAPEL_3}} | {{CODIGO_3}} | {{ACESSO_3}} |

Caso o usuário não possua token válido, é redirecionado para `{{ROTA_LOGIN}}`. Caso possua token, mas sem permissão para a rota, é redirecionado para `{{ROTA_PADRAO_AUTENTICADO}}`.

> **Nota de segurança:** o controle de acesso no front-end é uma conveniência de navegação, **não** um mecanismo de segurança. Toda regra de permissão precisa ser reaplicada e validada no backend.

---

## 6. Gerenciamento de Estado

A aplicação adota uma estratégia de **gerenciamento de estado distribuído**, utilizando mecanismos complementares conforme a natureza dos dados.

### 6.1 Estado Global

O **{{LIB_ESTADO_GLOBAL}}** (`{{VERSAO_LIB_ESTADO_GLOBAL}}`) é utilizado para gerenciar o estado global da aplicação, particularmente no módulo de autenticação. Foi escolhido por:

- **{{MOTIVO_ESCOLHA_1}}**;
- **{{MOTIVO_ESCOLHA_2}}**;
- **Reatividade seletiva**: componentes re-renderizam apenas quando a fatia de estado que consomem é alterada.

O store principal gerencia: dados do usuário autenticado, estado de carregamento, erros e as ações de login, logout e renovação de token.

### 6.2 Estado do Servidor

O **{{LIB_ESTADO_SERVIDOR}}** (`{{VERSAO_LIB_ESTADO_SERVIDOR}}`) é utilizado para gerenciar o **estado do servidor** — dados que residem na API e precisam ser buscados, cacheados e sincronizados. Os benefícios incluem:

- **Cache automático**: dados buscados são armazenados em memória e reutilizados.
- **Invalidação inteligente**: o cache pode ser invalidado seletivamente quando dados são modificados.
- **Stale-while-revalidate**: dados obsoletos são exibidos imediatamente enquanto novos dados são buscados em segundo plano.
- **Gerenciamento de mutations**: operações de escrita são gerenciadas com feedback de carregamento e erro.

Hooks definidos no módulo de autenticação:

| Hook | Tipo | Finalidade |
|------|------|-----------|
| `{{HOOK_1}}` | Query | {{FINALIDADE_HOOK_1}} |
| `{{HOOK_2}}` | Mutation | {{FINALIDADE_HOOK_2}} |
| `{{HOOK_3}}` | Mutation | {{FINALIDADE_HOOK_3}} |

Registre aqui as configurações de cache relevantes (ex: `staleTime`, `gcTime`) e a razão dos valores escolhidos.

### 6.3 Estado de Contexto

O contexto de autenticação provê o estado de sessão a toda a árvore de componentes, combinando:

- **Verificação do armazenamento local**: monitora a existência de tokens válidos.
- **Reação a invalidações**: observa mudanças no cache de dados do servidor.

O hook `{{HOOK_AUTH}}()` expõe:
- `{{CAMPO_USUARIO}}`: dados do usuário autenticado (ou `null`).
- `{{CAMPO_AUTENTICADO}}`: booleano indicando se o usuário está autenticado.
- `{{CAMPO_CARREGANDO}}`: booleano indicando se a verificação está em andamento.

---

## 7. Sistema de Autenticação e Segurança

### 7.1 Fluxo de Autenticação

<!-- guia: se o projeto não tem 2FA, simplifique o diagrama para uma etapa só. Não mantenha caixas que não existem. -->

```
┌─────────┐    {{ETAPA_1}}     ┌────────────┐    {{ETAPA_2}}   ┌──────────────┐
│  Login  │ ─────────────────► │ {{TELA_2}} │ ───────────────► │ Autenticado  │
└─────────┘                    └────────────┘                  └──────────────┘
      │                              │
      │ ({{FLUXO_ALTERNATIVO_1}})    │ ({{FLUXO_ALTERNATIVO_2}})
      ▼                              ▼
┌─────────────┐              ┌──────────────┐
│ {{TELA_A}}  │              │ {{TELA_B}}   │
└─────────────┘              └──────────────┘
```

1. **Etapa 1 — {{NOME_ETAPA_1}}**: {{DESCRICAO_ETAPA_1}}
2. **Etapa 2 — {{NOME_ETAPA_2}}**: {{DESCRICAO_ETAPA_2}}

Fluxos especiais tratados:
- **{{FLUXO_ESPECIAL_1}}**: {{TRATAMENTO_1}}
- **{{FLUXO_ESPECIAL_2}}**: {{TRATAMENTO_2}}

### 7.2 Gerenciamento de Tokens

- **`{{NOME_ACCESS_TOKEN}}`** (Access Token): validade de {{VALIDADE_ACCESS_TOKEN}}, utilizado para autorizar requisições à API.
- **`{{NOME_REFRESH_TOKEN}}`** (Refresh Token): validade de {{VALIDADE_REFRESH_TOKEN}}, utilizado para renovar o access token.

A função `{{FUNCAO_DECODE_TOKEN}}()` decodifica o payload do token (sem verificação de assinatura no front-end — a verificação ocorre no backend) e extrai informações de identidade e permissão.

> Atenção a codificação: decodificação de base64 no navegador exige tratamento explícito de UTF-8 para nomes com acentuação.

### 7.3 Armazenamento de Credenciais no Cliente

Os tokens são armazenados em **{{MECANISMO_ARMAZENAMENTO}}**, com as seguintes características de segurança:

- **Configuração**: {{ATRIBUTOS_SEGURANCA}} (ex: `SameSite`, `Secure`, `Path`, `MaxAge`).
- **Codificação**: nomes e valores são codificados antes da escrita.
- **Operações**: {{OPERACOES_DISPONIVEIS}}.
- **Validação de formato**: verifica se o token armazenado tem o formato esperado antes de usar.

<!-- guia: explique a decisão. Cookie vs localStorage é a pergunta que todo revisor de segurança faz — deixe o raciocínio registrado. -->

### 7.4 Renovação Automática de Tokens

A renovação de tokens é implementada em duas camadas:

1. **Renovação proativa** (interceptador de requisição): antes de cada requisição, verifica se o token está próximo de expirar (menos de {{JANELA_RENOVACAO}}). Caso esteja, o token é renovado **antes** de enviar a requisição, evitando erros 401.
2. **Renovação reativa** (interceptador de resposta): ao receber um 401, tenta renovar o token e refazer a requisição original uma única vez. Uma flag de retry evita loops infinitos.

Um mecanismo de **exclusão mútua** impede múltiplas chamadas simultâneas de renovação quando várias requisições detectam o token expirado ao mesmo tempo.

### 7.5 Sistema de Permissões

{{DESCRICAO_MODELO_PERMISSOES}}

Quando um usuário possui **múltiplas permissões**, o front-end aplica a regra de {{REGRA_DESEMPATE_PERMISSAO}}.

---

## 8. Camada de Serviços e Comunicação com API

### 8.1 Configuração do Cliente HTTP

O **{{CLIENTE_HTTP}}** (`{{VERSAO_CLIENTE_HTTP}}`) é o cliente HTTP da aplicação. A instância principal é configurada com:

- **Base URL**: `{{PREFIXO_VAR_AMBIENTE}}_API_BASE_URL`, com fallback para `/api` quando servida atrás de proxy.
- **Timeout**: {{TIMEOUT_PADRAO}}.
- **Headers padrão**: `Content-Type: application/json`.

### 8.2 Interceptadores de Requisição e Resposta

- **Interceptador de requisição**: injeta o header `Authorization: Bearer <token>` e dispara a renovação proativa.
- **Interceptador de resposta**: trata 401 com renovação e retry; padroniza o formato dos erros para as camadas superiores.

### 8.3 Serviço de Autenticação

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `{{METODO_1}}` | `{{ENDPOINT_1}}` | {{DESCRICAO_METODO_1}} |
| `{{METODO_2}}` | `{{ENDPOINT_2}}` | {{DESCRICAO_METODO_2}} |
| `{{METODO_3}}` | `{{ENDPOINT_3}}` | {{DESCRICAO_METODO_3}} |

Todos os métodos tratam erros da API, retornando respostas estruturadas ou lançando exceções.

### 8.4 Serviços de Domínio

O `{{SERVICO_DOMINIO}}` gerencia as operações sobre `{{ENTIDADE_PRINCIPAL}}`:

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `buscarPorId` | `GET {{ROTA_ENTIDADE}}/:id` | Busca por identificador |
| `criar` | `POST {{ROTA_ENTIDADE}}` | Cria novo registro |
| `atualizar` | `PUT {{ROTA_ENTIDADE}}/:id` | Atualiza registro existente |
| `sincronizar` | Composto | Busca ou cria/atualiza automaticamente |

---

## 9. Tipagem e Contratos de Dados

Os tipos são utilizados extensivamente para definir **contratos de dados** que espelham as estruturas retornadas pelas APIs. Os principais são:

**Autenticação (`types/auth.{{EXT}}`)**:
- `{{TIPO_USUARIO}}`: representa o usuário autenticado.
- `{{TIPO_LOGIN_REQUEST}}` / `{{TIPO_LOGIN_RESPONSE}}`: contrato de login.
- `{{TIPO_PAYLOAD_TOKEN}}`: estrutura do payload decodificado do token.

**Domínio (`types/{{ENTIDADE_PRINCIPAL}}.{{EXT}}`)**:
- `{{TIPO_ENTIDADE_REQUEST}}`: dados para criar/atualizar a entidade.
- `{{TIPO_ENTIDADE_RESPONSE}}`: resposta completa da entidade.

A tipagem garante que incompatibilidades entre o front-end e o back-end sejam detectadas em tempo de compilação.

---

## 10. Componentes e Interface do Usuário

### 10.1 Componentes de Layout

O componente `{{COMPONENTE_LAYOUT}}` define a estrutura visual padrão para todas as páginas autenticadas:

```
┌──────────────────────────────────────────────────┐
│ ┌──────────┐ ┌──────────────────────────────────┐│
│ │          │ │        Header / Breadcrumb       ││
│ │          │ ├──────────────────────────────────┤│
│ │ Sidebar  │ │                                  ││
│ │          │ │        Conteúdo (children)       ││
│ │          │ │                                  ││
│ └──────────┘ └──────────────────────────────────┘│
└──────────────────────────────────────────────────┘
```

O layout adapta automaticamente os itens de navegação com base no nível de permissão do usuário.

### 10.2 Sistema de Navegação

- **`{{COMPONENTE_SIDEBAR}}`**: monta o layout da navegação lateral.
- **`{{COMPONENTE_NAV}}`**: renderiza os itens de navegação e detecta a rota ativa.
- **`{{COMPONENTE_NAV_USUARIO}}`**: exibe avatar e menu do usuário com opção de logout.
- **`{{COMPONENTE_BREADCRUMB}}`**: gera a trilha de navegação com base na rota atual.
- **`{{COMPONENTE_RODAPE}}`**: exibe informações de versão e metadata de build.

### 10.3 Biblioteca de Componentes UI

O diretório `components/ui/` contém aproximadamente **{{QTD_COMPONENTES_UI}} componentes** reutilizáveis. Cada componente segue o padrão de composição (*compound component pattern*):

```{{EXT_CODIGO}}
<{{COMPONENTE_EXEMPLO}}>
  <{{COMPONENTE_EXEMPLO}}Trigger>
    <{{COMPONENTE_EXEMPLO}}Value placeholder="Selecione" />
  </{{COMPONENTE_EXEMPLO}}Trigger>
  <{{COMPONENTE_EXEMPLO}}Content>
    <{{COMPONENTE_EXEMPLO}}Item value="opcao1">Opção 1</{{COMPONENTE_EXEMPLO}}Item>
  </{{COMPONENTE_EXEMPLO}}Content>
</{{COMPONENTE_EXEMPLO}}>
```

A função utilitária `{{FUNCAO_CLASSES}}()` combina e resolve conflitos de classes CSS automaticamente.

### 10.4 Componentes Personalizados

- **`{{COMPONENTE_CUSTOM_1}}`**: {{DESCRICAO_CUSTOM_1}}
- **`{{COMPONENTE_CUSTOM_2}}`**: {{DESCRICAO_CUSTOM_2}}
- **`{{COMPONENTE_SKELETON}}`**: representação visual de carregamento da tela principal.

---

## 11. Páginas da Aplicação

<!-- guia: uma subseção por página relevante. Para cada uma, registre o tamanho aproximado e as decisões técnicas não óbvias (cache, persistência local, timers, guardas de concorrência). Páginas triviais podem ser agrupadas em uma tabela. -->

### 11.1 {{PAGINA_PRINCIPAL}}

A página `{{ARQUIVO_PAGINA_PRINCIPAL}}` (~{{LINHAS}} linhas) é a tela principal da aplicação.

**Funcionalidades técnicas notáveis**:
- **Cache de dados**: {{ESTRATEGIA_CACHE}}
- **Filtros**: {{DESCRICAO_FILTROS}}
- **Persistência de estado**: {{ESTRATEGIA_PERSISTENCIA}}
- **Regras de visibilidade**: {{REGRAS_VISIBILIDADE}}

### 11.2 {{PAGINA_CRIACAO}}

A página `{{ARQUIVO_PAGINA_CRIACAO}}` (~{{LINHAS}} linhas) implementa o formulário de criação com:

- **Persistência de rascunho**: {{ESTRATEGIA_RASCUNHO}}
- **Validações de negócio**: {{VALIDACOES}}
- **Verificação de conflitos**: {{VERIFICACAO_CONFLITOS}}

### 11.3 {{PAGINA_ADMINISTRATIVA}}

A página `{{ARQUIVO_PAGINA_ADMIN}}` (~{{LINHAS}} linhas) é a tela administrativa:

- **Tabela paginada server-side**.
- **Múltiplos filtros**.
- **Ações em massa**.
- **Guardas de concorrência**: antes de executar uma ação, busca o estado atual do registro para evitar conflito.

### 11.4 Páginas de Autenticação

- **Login**: {{DESCRICAO_LOGIN}}
- **Registro**: {{DESCRICAO_REGISTRO}}
- **Recuperação de senha**: {{DESCRICAO_RECUPERACAO}}
- **Redefinição de senha**: medidor de força e checklist de requisitos.

---

## 12. Validação de Formulários

A aplicação utiliza **{{LIB_FORMULARIO}}** (`{{VERSAO_LIB_FORMULARIO}}`) e **{{LIB_VALIDACAO}}** (`{{VERSAO_LIB_VALIDACAO}}`):

- **{{LIB_FORMULARIO}}**: gerencia o estado do formulário com performance otimizada.
- **{{LIB_VALIDACAO}}**: define schemas de validação tipados, garantindo correspondência entre validação em runtime e tipos em compilação.
- **Resolvers**: conectam os schemas à biblioteca de formulário.

Validações específicas implementadas:
- **{{VALIDACAO_1}}**: {{REGRA_1}}
- **{{VALIDACAO_2}}**: {{REGRA_2}}
- **{{VALIDACAO_3}}**: {{REGRA_3}}

> Toda validação de formulário é replicada no backend. A validação no cliente existe para experiência do usuário, não para integridade dos dados.

---

## 13. Sistema de Logging

O módulo `logger.{{EXT}}` implementa um **sistema de logging estruturado**:

- **Níveis de log**: `trace`, `debug`, `info`, `warn`, `error`.
- **Prefixos contextuais**: cada logger é criado com um nome de serviço, componente ou hook.
- **Logging condicional**: `trace` e `debug` só emitem saída em ambiente de desenvolvimento.
- **Contexto estruturado**: suporte a objetos de contexto serializados em JSON.
- **Fábricas especializadas**:
  - `createServiceLogger('auth')` → `[auth] mensagem`
  - `createComponentLogger('{{COMPONENTE}}')` → `[component:{{COMPONENTE}}] mensagem`
  - `createHookLogger('{{HOOK}}')` → `[hook:{{HOOK}}] mensagem`
- **Função `logError`**: captura nome, mensagem e stack trace de erros.

> Nunca logar tokens, senhas, documentos de identificação ou dados pessoais completos.

---

## 14. Responsividade e Experiência Mobile

- **Utilitários responsivos**: prefixos de breakpoint para adaptar layouts.
- **Hook `{{HOOK_MOBILE}}`**: detecta dispositivos abaixo de {{BREAKPOINT_MOBILE}} via `window.matchMedia`.
- **Navegação responsiva**: colapsa automaticamente em telas menores.
- **Padrões mobile**: diálogos são substituídos por *drawers* deslizantes em telas pequenas.
- **Animações**: {{LIB_ANIMACAO}} (`{{VERSAO_LIB_ANIMACAO}}`) para transições de entrada e saída.

---

## 15. Containerização e Deploy

### 15.1 Docker e Multi-Stage Build

**Estágio 1 — Build** (`{{IMAGEM_BUILD}}`):
1. Instala o gerenciador de pacotes **{{GERENCIADOR_PACOTES}}** (`{{VERSAO_GERENCIADOR}}`).
2. Copia o lockfile e o manifesto para otimizar o cache de camadas Docker.
3. Instala dependências com lockfile congelado (garante reprodutibilidade).
4. Copia o código-fonte e executa o build.
5. Variáveis de ambiente públicas são injetadas como **build args**, sendo incorporadas ao bundle em tempo de compilação.

> **Consequência importante:** variáveis injetadas no build ficam visíveis no bundle entregue ao navegador. Nunca injete segredos por essa via.

**Estágio 2 — Runtime** (`{{IMAGEM_RUNTIME}}`):
1. Copia apenas os artefatos estáticos gerados.
2. Aplica a configuração customizada do servidor web.
3. Expõe a porta {{PORTA_CONTAINER}}.

### 15.2 Servidor Web de Produção

O **{{SERVIDOR_WEB}}** (`{{VERSAO_SERVIDOR_WEB}}`) serve os arquivos estáticos, configurado com:

- **SPA Fallback**: garante que todas as rotas do roteador client-side sejam servidas pelo `index.html`.
- **Compressão gzip**: habilitada para conteúdo textual.
- **Cache de assets**: arquivos com hash no nome recebem cache longo e imutável.
- **Proxy reverso** (opcional): redireciona chamadas `/api/` para o backend, quando necessário.

### 15.3 Orquestração de Containers

O `docker-compose.yml` orquestra o serviço de front-end:

- **Porta**: mapeia `{{PORTA_HOST}}:{{PORTA_CONTAINER}}`.
- **Restart policy**: `unless-stopped`.
- **Timezone**: `{{TIMEZONE}}`.
- **Rede**: rede bridge dedicada para isolamento.

---

## 16. Variáveis de Ambiente e Configuração

Variáveis prefixadas com `{{PREFIXO_VAR_AMBIENTE}}` são expostas ao código client-side:

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `{{PREFIXO_VAR_AMBIENTE}}_API_BASE_URL` | URL base da API principal | `http://host:porta/api` |
| `{{PREFIXO_VAR_AMBIENTE}}_API_URL_AUTH` | URL base da API de autenticação | `http://host:porta` |
| `{{PREFIXO_VAR_AMBIENTE}}_SYSTEM_ID` | Identificador do sistema | `uuid` |
| `{{PREFIXO_VAR_AMBIENTE}}_APP_VERSION` | Versão da aplicação | `1.0.0` |
| `{{PREFIXO_VAR_AMBIENTE}}_BUILD_NUMBER` | Número do build | `42` |
| `{{PREFIXO_VAR_AMBIENTE}}_COMMIT_SHA` | SHA do commit | `abc1234` |
| `{{PREFIXO_VAR_AMBIENTE}}_AMBIENTE` | Ambiente de execução | `production` |

---

## 17. Qualidade de Código e Ferramentas de Desenvolvimento

### Linter e Formatação

O **{{LINTER}}** (`{{VERSAO_LINTER}}`) é configurado com {{FORMATO_CONFIG_LINTER}}, incluindo regras recomendadas da linguagem, do framework e dos hooks.

### Gerenciador de Pacotes

O **{{GERENCIADOR_PACOTES}}** é o gerenciador utilizado, com lockfile determinístico garantindo reprodutibilidade de builds.

### Scripts de Desenvolvimento

| Script | Comando | Descrição |
|--------|---------|-----------|
| `dev` | `{{CMD_DEV}}` | Inicia o servidor de desenvolvimento com HMR |
| `build` | `{{CMD_BUILD}}` | Compila e gera bundle de produção |
| `lint` | `{{CMD_LINT}}` | Executa análise estática do código |
| `preview` | `{{CMD_PREVIEW}}` | Serve o build de produção localmente |
| `test` | `{{CMD_TEST}}` | Executa a suíte de testes |

---

## 18. Considerações Finais

O front-end do {{NOME_DO_SISTEMA}} foi desenvolvido com foco em **manutenibilidade**, **segurança** e **experiência do usuário**. A escolha das tecnologias reflete {{JUSTIFICATIVA_STACK}}:

- **{{LIB_UI}}** como paradigma de desenvolvimento de interface.
- **{{LINGUAGEM}}** com modo estrito para segurança de tipos.
- **{{BUNDLER}}** para builds rápidos e experiência de desenvolvimento otimizada.
- **{{FRAMEWORK_CSS}}** com {{LIB_COMPONENTES}} para estilização consistente e acessível.
- **{{LIB_ESTADO_GLOBAL}} + {{LIB_ESTADO_SERVIDOR}}** como solução de gerenciamento de estado.
- **Autenticação** com renovação automática de tokens e RBAC.
- **Docker + {{SERVIDOR_WEB}}** para deploy containerizado e reprodutível.

A arquitetura modular e a separação clara de responsabilidades entre camadas permitem que novos desenvolvedores compreendam e contribuam com o projeto de forma produtiva.

---

## 19. Serviços de Backend Consumidos

<!-- guia: use as seções 19 e 20 apenas quando o front-end conversa com mais de um backend, ou com um backend que ele não controla. Em projeto de backend único e próprio, apague ambas e mantenha só a seção 8. -->

O {{NOME_DO_SISTEMA}} opera com **{{QTD_BACKENDS}} backends**. Esta seção descreve as características do backend de {{NOME_BACKEND_SECUNDARIO}} conforme observadas pelo front-end.

### 19.1 Visão Geral do Serviço

O serviço é acessível via a variável `{{PREFIXO_VAR_AMBIENTE}}_API_URL_AUTH` e atua como **plataforma de identidade centralizada (Identity Provider)** compartilhada por múltiplos sistemas, gerenciando:

- cadastro de usuários;
- autenticação (incluindo segundo fator, quando aplicável);
- gerenciamento de sessões simultâneas;
- emissão e renovação de tokens;
- controle de acesso por sistema, via identificador único de sistema;
- políticas de senha (expiração, troca obrigatória, complexidade mínima).

### 19.2 Endpoints e Recursos Expostos

| Método HTTP | Endpoint | Finalidade | Payload Principal |
|:-----------:|----------|------------|-------------------|
| POST | `{{ENDPOINT_REGISTRO}}` | Cadastro de novo usuário | `{ ... }` |
| POST | `{{ENDPOINT_LOGIN}}` | Autenticação | `{ ... }` |
| POST | `{{ENDPOINT_REFRESH}}` | Renova access token | `{ ... }` |
| POST | `{{ENDPOINT_LOGOUT}}` | Encerra a sessão atual | `{ ... }` |

### 19.3 Modelo de Permissões

Cada relação `usuário ↔ sistema` possui um registro próprio:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `{{CAMPO_ID_VINCULO}}` | UUID | Identificador único da vinculação |
| `{{CAMPO_ID_USUARIO}}` | UUID | ID do usuário no provedor de identidade |
| `{{CAMPO_ID_SISTEMA}}` | UUID | ID do sistema |
| `{{CAMPO_ID_PERMISSAO}}` | int | Nível de permissão numérico |

Níveis de permissão e o significado de cada um **no contexto deste sistema**:

| Código | Nome | Significado para o {{NOME_DO_SISTEMA}} |
|:---:|:---:|---|
| {{CODIGO_1}} | {{PAPEL_1}} | {{SIGNIFICADO_1}} |
| {{CODIGO_2}} | {{PAPEL_2}} | {{SIGNIFICADO_2}} |
| {{CODIGO_3}} | {{PAPEL_3}} | {{SIGNIFICADO_3}} |

### 19.4 Estrutura de Respostas da API

Todas as respostas seguem um **envelope padronizado**:

```json
{
  "sucesso": true,
  "dados": { },
  "mensagem": "Descrição opcional"
}
```

Para **endpoints paginados**, o campo `dados` inclui metadados de paginação:

```json
{
  "sucesso": true,
  "dados": {
    "items": [],
    "totalItems": 50,
    "pageNumber": 1,
    "pageSize": 10,
    "totalPages": 5,
    "hasPreviousPage": false,
    "hasNextPage": true
  }
}
```

### 19.5 Tokens e Sessões

- **Access Token**: assinado, contendo claims do usuário. Validade de {{VALIDADE_ACCESS_TOKEN}}.
- **Refresh Token**: opaco, controlado pelo servidor. Validade de {{VALIDADE_REFRESH_TOKEN}}.

Claims presentes no payload:

| Claim | Tipo | Descrição |
|-------|------|-----------|
| `sub` | string | Identificador do sujeito |
| `{{CLAIM_1}}` | {{TIPO_CLAIM_1}} | {{DESCRICAO_CLAIM_1}} |
| `{{CLAIM_2}}` | {{TIPO_CLAIM_2}} | {{DESCRICAO_CLAIM_2}} |
| `exp` | number | Timestamp Unix de expiração |
| `iss` | string | Emissor do token |
| `aud` | string | Audiência do token |

---

## 20. Relação entre o Front-End e os Backends

### 20.1 Arquitetura de Comunicação

```
┌─────────────────────────────────────┐
│          Front-End (SPA)            │
│                                     │
│  ┌─────────────┐ ┌───────────────┐  │
│  │   authApi   │ │      api      │  │
│  └──────┬──────┘ └───────┬───────┘  │
│         │                │          │
└─────────┼────────────────┼──────────┘
          │                │
          ▼                ▼
┌─────────────────┐ ┌─────────────────┐
│  API de         │ │  API de         │
│  Autenticação   │ │  {{DOMINIO}}    │
│                 │ │                 │
│  • Identidade   │ │  • {{RECURSO_1}}│
│  • Permissões   │ │  • {{RECURSO_2}}│
│  • Sessões      │ │  • {{RECURSO_3}}│
└─────────────────┘ └─────────────────┘
```

As duas APIs são **independentes** e não se comunicam diretamente. O front-end atua como **orquestrador**, traduzindo dados de identidade para o modelo de dados do domínio.

> Essa orquestração no cliente é uma decisão arquitetural com custo: falhas parciais (uma API responde, a outra não) precisam ser tratadas explicitamente. Registre abaixo como cada fluxo lida com isso.

### 20.2 Instâncias de Cliente HTTP Separadas

| Instância | Arquivo | Base URL | Timeout | Interceptadores |
|-----------|---------|----------|---------|------------------|
| `authApi` | `{{ARQUIVO_AUTH_SERVICE}}` | `{{BASE_URL_AUTH}}` | {{TIMEOUT_AUTH}} | Nenhum (endpoints públicos) |
| `api` | `{{ARQUIVO_API_SERVICE}}` | `{{BASE_URL_API}}` | {{TIMEOUT_API}} | Request (injeta token) + Response (renova em 401) |

### 20.3 Fluxo Completo de Registro e Provisionamento

```
┌───────────────────────────────────────────────────────────────┐
│                    FLUXO DE REGISTRO                          │
├───────────────────────────────────────────────────────────────┤
│  1. POST {{ENDPOINT_REGISTRO}}     → API Auth                 │
│     Resultado: {{RESULTADO_1}}                                │
│                                                               │
│  2. POST {{ENDPOINT_PERMISSAO}}    → API Auth                 │
│     Resultado: {{RESULTADO_2}}                                │
│                                                               │
│  3. GET  {{ENDPOINT_PERMISSAO}}    → API Auth                 │
│     Resultado: {{RESULTADO_3}}                                │
│                                                               │
│  ───── Após o primeiro login ─────                            │
│                                                               │
│  4. POST {{ROTA_ENTIDADE}}         → API de {{DOMINIO}}       │
│     Resultado: entidade criada no sistema de domínio          │
└───────────────────────────────────────────────────────────────┘
```

**Tratamento de usuários já existentes**: {{TRATAMENTO_USUARIO_EXISTENTE}}

**Dados transitórios**: {{DADOS_TRANSITORIOS}} são salvos temporariamente no cliente durante o registro e consumidos no primeiro login, sendo removidos após a sincronização bem-sucedida.

### 20.4 Fluxo Completo de Login e Sincronização

```
┌────────────────────────────────────────────────────────────┐
│                     FLUXO DE LOGIN                         │
├────────────────────────────────────────────────────────────┤
│  Etapa 1 — Credenciais        → API Auth                  │
│  Etapa 2 — Segundo fator      → API Auth                  │
│           → Tokens salvos no cliente                       │
│  Etapa 3 — Decodificação do token                          │
│  Etapa 4 — Obtenção do vínculo usuário↔sistema             │
│  Etapa 5 — Sincronização da entidade de domínio           │
│  Etapa 6 — Invalidação de cache                            │
└────────────────────────────────────────────────────────────┘
```

**Fluxos alternativos**: {{FLUXOS_ALTERNATIVOS_LOGIN}}

### 20.5 Mapeamento de Dados entre Backends

Os backends utilizam **codificações diferentes** para o mesmo conceito. O front-end traduz entre eles:

```
   API de Autenticação            Front-End            API de {{DOMINIO}}
┌──────────────────────┐   ┌───────────────────┐   ┌──────────────────────┐
│ {{ORIGEM_1}}         │──►│ {{TRADUCAO_1}}    │──►│ {{DESTINO_1}}        │
├──────────────────────┤   ├───────────────────┤   ├──────────────────────┤
│ {{ORIGEM_2}}         │──►│ {{TRADUCAO_2}}    │──►│ {{DESTINO_2}}        │
└──────────────────────┘   └───────────────────┘   └──────────────────────┘
```

Esse mapeamento é executado em {{PONTOS_MAPEAMENTO}}.

<!-- guia: mapeamentos duplicados em pontos diferentes do código são fonte recorrente de bug. Se houver mais de um ponto, considere extrair para uma função única e documente aqui onde ela vive. -->

### 20.6 Sincronização de Entidades (Upsert)

A cada login, o front-end executa um **upsert** que vincula a identidade do provedor de autenticação ao registro correspondente na API de domínio:

```
              ┌────────────────────────────────┐
              │  {{SERVICO_DOMINIO}}.sincronizar│
              ├────────────────────────────────┤
              │ 1. Busca pelo ID externo       │
              │ 2. Fallback: busca por email   │
              │ 3. Se não existe → POST criar  │
              │    Se existe e diverge → PUT   │
              │    Se existe e igual → retorna │
              └────────────────────────────────┘
```

**Campos sincronizados**: {{CAMPOS_SINCRONIZADOS}}.

**Critérios de atualização**: {{CRITERIOS_ATUALIZACAO}}.

### 20.7 Renovação de Tokens e Propagação

O access token emitido pela API de autenticação é utilizado para **ambos os backends**. A renovação ocorre via API de autenticação, e o novo token é automaticamente propagado.

```
┌──────────────────────────────────────────────────────────┐
│              FLUXO DE RENOVAÇÃO DE TOKEN                 │
├──────────────────────────────────────────────────────────┤
│  1. Interceptor de request detecta token expirando       │
│  2. POST {{ENDPOINT_REFRESH}} → API Auth                 │
│  3. Novos tokens salvos e reutilizados pela instância    │
│     de domínio automaticamente                           │
│  4. Em 401, o interceptor de response renova e refaz     │
│     a request uma única vez (flag de retry)              │
└──────────────────────────────────────────────────────────┘
```

### 20.8 Operações com Escrita Dupla

Operações administrativas que alteram permissões executam **escritas em ambos os backends**:

1. **API de Autenticação**: `{{OPERACAO_AUTH}}`
2. **API de {{DOMINIO}}**: `{{OPERACAO_DOMINIO}}`

A escrita dupla garante consistência entre os dois backends. O front-end é responsável por executar ambas as operações e **tratar falhas parciais** — descreva aqui o comportamento real em caso de falha na segunda escrita.

---

## Como adaptar este template a um novo projeto

<!-- guia: apague esta seção inteira depois de preencher. -->

1. **Remova antes de preencher.** Comece cortando as seções que não existem no projeto (2FA, dual-backend, Docker, mobile). Um documento com metade das seções preenchidas de verdade vale mais do que vinte seções genéricas.
2. **Renumere o Sumário** depois de remover seções. Links quebrados em documentação técnica corroem a confiança no resto do arquivo.
3. **Descreva o que existe, não o que se pretende fazer.** Onde houver intenção futura, marque explicitamente como "Previsto" ou "Não implementado".
4. **Mantenha os avisos de segurança.** Os blocos sobre validação no cliente, build args e logging de dados sensíveis valem para qualquer projeto — não os apague junto com o conteúdo específico.
5. **Prefira tabela a prosa** para endpoints, rotas, permissões, variáveis e scripts. Prosa serve para explicar decisão; tabela serve para consultar.
6. **Registre a decisão, não só a escolha.** "Usamos {{LIB_ESTADO_GLOBAL}}" é inútil daqui a seis meses; "usamos {{LIB_ESTADO_GLOBAL}} porque X" evita que alguém desfaça a escolha sem saber o custo.
7. **Datar e versionar.** Feche o documento com a data de geração e a versão do sistema documentado, como no rodapé abaixo.

---

*Documento gerado em {{MES_ANO}}.*
*Versão do sistema documentada: {{NOME_DO_SISTEMA}} Front-End v{{VERSAO}}.*
