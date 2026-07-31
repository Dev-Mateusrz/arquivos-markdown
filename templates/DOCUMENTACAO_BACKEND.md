# Documentação Técnica do Back-End — {{NOME_DO_SISTEMA}}

## Aspectos Tecnológicos da API e da Camada de Domínio

> **Para que serve:** documentar em profundidade a arquitetura técnica do back-end — camadas, domínio, persistência, autenticação, integrações e deploy — para que um novo desenvolvedor (ou o próprio Claude) entenda o sistema sem precisar ler o código inteiro. Complementa o `README_PROJETO.md` (que é onboarding rápido) com o nível de detalhe de uma referência técnica. Segue a mesma estrutura de `DOCUMENTACAO_FRONTEND.md`, adaptada para o lado do servidor.
>
> **Template reutilizável.** Copie este arquivo para `docs/DOCUMENTACAO_BACKEND.md`, substitua os `{{PLACEHOLDERS}}` e apague os blocos `<!-- guia: ... -->` e a seção "Como adaptar este template" ao final. Seções que não se aplicam ao projeto devem ser **removidas**, não deixadas vazias — e o Sumário renumerado.

---

## Sumário

1. [Introdução](#1-introdução)
2. [Arquitetura Geral do Back-End](#2-arquitetura-geral-do-back-end)
3. [Stack Tecnológica](#3-stack-tecnológica)
   - 3.1 [Linguagem e Framework](#31-linguagem-e-framework)
   - 3.2 [ORM e Banco de Dados](#32-orm-e-banco-de-dados)
   - 3.3 [Mensageria e Processamento Assíncrono](#33-mensageria-e-processamento-assíncrono)
   - 3.4 [Documentação de API](#34-documentação-de-api)
4. [Estrutura de Diretórios e Organização do Código](#4-estrutura-de-diretórios-e-organização-do-código)
5. [Camada de Apresentação (API)](#5-camada-de-apresentação-api)
   - 5.1 [Definição de Rotas e Controllers](#51-definição-de-rotas-e-controllers)
   - 5.2 [Versionamento de API](#52-versionamento-de-api)
   - 5.3 [Documentação Interativa](#53-documentação-interativa)
6. [Camada de Domínio e Regras de Negócio](#6-camada-de-domínio-e-regras-de-negócio)
   - 6.1 [Entidades e Agregados](#61-entidades-e-agregados)
   - 6.2 [Casos de Uso / Services](#62-casos-de-uso--services)
   - 6.3 [Máquinas de Estado](#63-máquinas-de-estado)
7. [Persistência de Dados](#7-persistência-de-dados)
   - 7.1 [Configuração do ORM](#71-configuração-do-orm)
   - 7.2 [Migrations](#72-migrations)
   - 7.3 [Repositórios e Consultas](#73-repositórios-e-consultas)
   - 7.4 [Transações](#74-transações)
8. [Autenticação e Autorização](#8-autenticação-e-autorização)
   - 8.1 [Fluxo de Autenticação](#81-fluxo-de-autenticação)
   - 8.2 [Emissão e Validação de Tokens](#82-emissão-e-validação-de-tokens)
   - 8.3 [Armazenamento de Credenciais](#83-armazenamento-de-credenciais)
   - 8.4 [Controle de Acesso (RBAC/Permissões)](#84-controle-de-acesso-rbacpermissões)
   - 8.5 [Middlewares e Guards de Segurança](#85-middlewares-e-guards-de-segurança)
9. [Contratos de Dados e Validação de Entrada](#9-contratos-de-dados-e-validação-de-entrada)
10. [Tratamento de Erros e Exceções](#10-tratamento-de-erros-e-exceções)
11. [Sistema de Logging e Observabilidade](#11-sistema-de-logging-e-observabilidade)
12. [Integrações Externas](#12-integrações-externas)
13. [Jobs Agendados e Processos em Background](#13-jobs-agendados-e-processos-em-background)
14. [Testes](#14-testes)
    - 14.1 [Testes Unitários](#141-testes-unitários)
    - 14.2 [Testes de Integração](#142-testes-de-integração)
    - 14.3 [Cobertura](#143-cobertura)
15. [Containerização e Deploy](#15-containerização-e-deploy)
    - 15.1 [Docker e Multi-Stage Build](#151-docker-e-multi-stage-build)
    - 15.2 [Orquestração de Containers](#152-orquestração-de-containers)
    - 15.3 [Migrations em Produção](#153-migrations-em-produção)
16. [Variáveis de Ambiente e Configuração](#16-variáveis-de-ambiente-e-configuração)
17. [Qualidade de Código e Ferramentas de Desenvolvimento](#17-qualidade-de-código-e-ferramentas-de-desenvolvimento)
18. [Considerações Finais](#18-considerações-finais)
19. [Serviços Externos Consumidos](#19-serviços-externos-consumidos)
    - 19.1 [Visão Geral do Serviço](#191-visão-geral-do-serviço)
    - 19.2 [Endpoints e Recursos Consumidos](#192-endpoints-e-recursos-consumidos)
    - 19.3 [Autenticação com o Serviço Externo](#193-autenticação-com-o-serviço-externo)
20. [Relação entre Este Back-End e Outros Serviços](#20-relação-entre-este-back-end-e-outros-serviços)
    - 20.1 [Arquitetura de Comunicação](#201-arquitetura-de-comunicação)
    - 20.2 [Consistência entre Serviços](#202-consistência-entre-serviços)
    - 20.3 [Tratamento de Falhas Parciais](#203-tratamento-de-falhas-parciais)

---

<details>
<summary><b>Placeholders deste template</b> (apagar depois de preencher)</summary>

| Placeholder | Significado |
|---|---|
| `{{NOME_DO_SISTEMA}}` | Nome do sistema |
| `{{ORGANIZACAO}}` | Organização/área responsável |
| `{{OBJETIVO_DO_SISTEMA}}` | O que o sistema faz, em uma frase |
| `{{LINGUAGEM}}` / `{{VERSAO_LINGUAGEM}}` | Linguagem principal do back-end e versão |
| `{{FRAMEWORK}}` / `{{VERSAO_FRAMEWORK}}` | Framework web/API e versão |
| `{{ORM}}` | Framework de acesso a dados/ORM |
| `{{BANCO_DE_DADOS}}` | Banco de dados relacional/não relacional usado |
| `{{FILA_MENSAGERIA}}` | Sistema de filas/mensageria, se houver |
| `{{FERRAMENTA_DOC_API}}` | Ferramenta de documentação de API (ex: Swagger/OpenAPI) |
| `{{ENTIDADE_PRINCIPAL}}` | Entidade central do domínio |
| `{{PROVEDOR_AUTH}}` | Provedor de identidade/autenticação |
| `{{ALGORITMO_HASH_SENHA}}` | Algoritmo de hashing de senha |
| `{{FERRAMENTA_TESTE}}` | Framework de testes |
| `{{FERRAMENTA_COBERTURA}}` | Ferramenta de cobertura de testes |
| `{{GERENCIADOR_PACOTES}}` | Gerenciador de pacotes/dependências |
| `{{LINTER}}` | Linter/formatador de código |
| `{{PREFIXO_VAR_AMBIENTE}}` | Prefixo das variáveis de ambiente da aplicação |

</details>

---

## 1. Introdução

O **{{NOME_DO_SISTEMA}}** é uma aplicação para {{OBJETIVO_DO_SISTEMA}}, desenvolvida no contexto da {{ORGANIZACAO}}. O back-end expõe uma **API {{ESTILO_API}}** (ex: REST, GraphQL) construída em **{{LINGUAGEM}} / {{FRAMEWORK}}**, responsável por regras de negócio, persistência de dados e integração com serviços externos.

Este documento descreve, de forma técnica e detalhada, os aspectos que compõem o back-end do sistema {{NOME_DO_SISTEMA}}: arquitetura em camadas, modelagem de domínio, persistência, segurança, tratamento de erros, observabilidade e infraestrutura de deploy.

<!-- guia: este documento descreve o que existe, não o que se pretende construir. Se uma seção descreve um plano, marque explicitamente como "Previsto" ou remova. -->

---

## 2. Arquitetura Geral do Back-End

O back-end do {{NOME_DO_SISTEMA}} segue uma **arquitetura em camadas**, separando a exposição HTTP da regra de negócio e da persistência:

```
┌──────────────────────────────────────────────────────┐
│                 Camada de Apresentação                │
│         (Controllers/Routers, Middlewares, DTOs)      │
├──────────────────────────────────────────────────────┤
│                  Camada de Aplicação                  │
│        (Casos de uso, orquestração, validação)        │
├──────────────────────────────────────────────────────┤
│                   Camada de Domínio                   │
│      (Entidades, regras de negócio, invariantes)      │
├──────────────────────────────────────────────────────┤
│                Camada de Infraestrutura                │
│   (Repositórios, ORM, clientes HTTP externos, filas)   │
└──────────────────────────────────────────────────────┘
```

<!-- guia: se o projeto não separa aplicação/domínio explicitamente (comum em CRUDs simples), documente a arquitetura real em vez de forçar este modelo — por exemplo "Controller -> Service -> Repository" sem camada de domínio isolada. -->

A regra que atravessa todas as camadas: **camadas internas não conhecem camadas externas**. O domínio não importa nada de infraestrutura ou apresentação; a infraestrutura implementa contratos definidos pelo domínio, nunca o contrário.

O ponto de entrada da aplicação (`{{ARQUIVO_ENTRADA}}`) registra, nesta ordem: configuração/variáveis de ambiente, conexão com banco de dados, middlewares globais (CORS, autenticação, tratamento de erro), rotas e, por fim, sobe o servidor HTTP.

---

## 3. Stack Tecnológica

### 3.1 Linguagem e Framework

O back-end é construído em **{{LINGUAGEM}}** (`{{VERSAO_LINGUAGEM}}`) com o framework **{{FRAMEWORK}}** (`{{VERSAO_FRAMEWORK}}`).

<!-- guia: descreva o motivo real da escolha, se souber (ex: já era o padrão do time, exigência do cliente, familiaridade). "Registrar a decisão, não só a escolha" vale aqui como no front-end. -->

### 3.2 ORM e Banco de Dados

Persistência via **{{ORM}}** sobre **{{BANCO_DE_DADOS}}**. Motivos da escolha do ORM:

- **{{MOTIVO_ESCOLHA_ORM_1}}**;
- **{{MOTIVO_ESCOLHA_ORM_2}}**;
- **Migrations versionadas**: todo o histórico de mudanças de schema é rastreável e reproduzível.

### 3.3 Mensageria e Processamento Assíncrono

<!-- guia: apague esta subseção inteira se o backend não usa filas nem processamento assíncrono. -->

O sistema usa **{{FILA_MENSAGERIA}}** para {{FINALIDADE_FILA}} (ex: desacoplar operações lentas, garantir entrega de eventos entre serviços). Filas/tópicos em uso:

| Fila/Tópico | Produtor | Consumidor | Finalidade |
|---|---|---|---|
| `{{FILA_1}}` | {{PRODUTOR_1}} | {{CONSUMIDOR_1}} | {{FINALIDADE_1}} |
| `{{FILA_2}}` | {{PRODUTOR_2}} | {{CONSUMIDOR_2}} | {{FINALIDADE_2}} |

### 3.4 Documentação de API

A API é documentada via **{{FERRAMENTA_DOC_API}}**, gerada {{ORIGEM_DOC_API}} (ex: a partir de anotações no código, de um arquivo OpenAPI mantido manualmente).

---

## 4. Estrutura de Diretórios e Organização do Código

O código-fonte do back-end está organizado dentro de `{{PASTA_SRC}}`, seguindo separação por responsabilidade:

```
src/
├── {{ARQUIVO_ENTRADA}}         # Ponto de entrada / bootstrap da aplicação
│
├── controllers/                # Camada de apresentação — recebe requisição, devolve resposta
│   └── ...
│
├── services/                   # Casos de uso — orquestram regra de negócio
│   └── ...
│
├── domain/                     # Entidades, agregados, regras e invariantes de negócio
│   └── ...
│
├── repositories/                # Acesso a dados — implementa contratos do domínio
│   └── ...
│
├── dtos/                        # Contratos de entrada/saída da API
│   └── ...
│
├── middlewares/                 # Autenticação, tratamento de erro, logging de requisição
│   └── ...
│
├── migrations/                  # Histórico versionado de mudanças de schema
│   └── ...
│
├── jobs/                        # Processos agendados / background workers
│   └── ...
│
├── integrations/                # Clientes para APIs externas
│   └── ...
│
├── lib/                         # Utilitários transversais (logger, helpers)
│   └── ...
│
└── config/                      # Configuração e variáveis de ambiente
    └── ...
```

<!-- guia: cole a árvore real (ex: `tree -L 2 src`) e comente apenas as pastas cuja finalidade não é óbvia pelo nome. -->

---

## 5. Camada de Apresentação (API)

### 5.1 Definição de Rotas e Controllers

A API expõe os seguintes grupos de recursos:

| Recurso | Prefixo | Proteção | Descrição |
|---|---|---|---|
| `{{RECURSO_1}}` | `{{PREFIXO_ROTA_1}}` | Autenticado | {{DESCRICAO_RECURSO_1}} |
| `{{RECURSO_2}}` | `{{PREFIXO_ROTA_2}}` | Autenticado + {{PAPEL}} | {{DESCRICAO_RECURSO_2}} |
| Autenticação | `{{PREFIXO_ROTA_AUTH}}` | Pública | Login, registro, refresh de token |
| Health check | `{{ROTA_HEALTH}}` | Pública | Verificação de disponibilidade do serviço |

Cada controller é responsável apenas por: validar o contrato de entrada (DTO), chamar o caso de uso correspondente e traduzir o resultado em resposta HTTP. Regra de negócio **não** vive no controller.

### 5.2 Versionamento de API

<!-- guia: se a API não é versionada, diga isso explicitamente em vez de apagar a seção — é uma decisão relevante para quem for consumir a API. -->

{{ESTRATEGIA_VERSIONAMENTO}} (ex: prefixo de URL `/v1`, header `Accept-Version`, sem versionamento formal ainda).

### 5.3 Documentação Interativa

A documentação interativa fica disponível em:

```text
http://localhost:{{PORTA_BACKEND}}/{{ROTA_DOC_API}}
```

Gerada via **{{FERRAMENTA_DOC_API}}**, refletindo os DTOs e anotações descritos na seção 9.

---

## 6. Camada de Domínio e Regras de Negócio

<!-- guia: esta é a seção mais específica do projeto. Mantenha a estrutura (entidades -> casos de uso -> máquina de estados) e troque o conteúdo pelo domínio real. -->

### 6.1 Entidades e Agregados

A entidade central do domínio é **{{ENTIDADE_PRINCIPAL}}**. Invariantes que o domínio garante, independente de quem chama:

- {{INVARIANTE_1}};
- {{INVARIANTE_2}};
- dados históricos (ex: valor no momento da operação) ficam gravados no próprio registro, e não devem ser inferidos depois a partir do estado atual de entidades relacionadas.

### 6.2 Casos de Uso / Services

| Caso de uso | Entrada | Regra principal | Saída |
|---|---|---|---|
| `{{CASO_DE_USO_1}}` | {{ENTRADA_1}} | {{REGRA_1}} | {{SAIDA_1}} |
| `{{CASO_DE_USO_2}}` | {{ENTRADA_2}} | {{REGRA_2}} | {{SAIDA_2}} |

Cada caso de uso é a unidade de transação: ou tudo dentro dele é persistido, ou nada é (ver 7.4 Transações).

### 6.3 Máquinas de Estado

```mermaid
stateDiagram-v2
    [*] --> PENDENTE: criação
    PENDENTE --> APROVADO: aprovação
    PENDENTE --> RECUSADO: recusa
    APROVADO --> CANCELADO: cancelamento
    APROVADO --> [*]
    RECUSADO --> [*]
    CANCELADO --> [*]
```

Regras de transição:

- {{REGRA_TRANSICAO_1}};
- {{REGRA_TRANSICAO_2}};
- transições não previstas no diagrama devem ser rejeitadas pelo domínio, não silenciosamente ignoradas.

---

## 7. Persistência de Dados

### 7.1 Configuração do ORM

O **{{ORM}}** é configurado para conectar em `{{BANCO_DE_DADOS}}` via a variável `{{VAR_CONNECTION_STRING}}`. Pool de conexões: {{CONFIG_POOL}}.

### 7.2 Migrations

Toda mudança de schema é feita via migration versionada, nunca alterando o banco manualmente.

```{{SHELL_PADRAO}}
{{CMD_CRIAR_MIGRATION}}
{{CMD_APLICAR_MIGRATION}}
```

> Migrations que alteram tabelas com dados em produção precisam ser revisadas com atenção redobrada — ver "Boas práticas" no `README_PROJETO.md`.

### 7.3 Repositórios e Consultas

O domínio define contratos de repositório (interfaces); a infraestrutura os implementa. Isso permite trocar o mecanismo de persistência sem alterar regra de negócio.

| Repositório | Entidade | Consultas notáveis |
|---|---|---|
| `{{REPOSITORIO_1}}` | {{ENTIDADE_1}} | {{CONSULTA_NOTAVEL_1}} |

### 7.4 Transações

Operações que escrevem em mais de uma tabela/agregado usam transação explícita — se uma etapa falha, tudo é revertido. {{ESTRATEGIA_TRANSACAO}} (ex: unit of work, transação gerenciada pelo ORM por caso de uso).

---

## 8. Autenticação e Autorização

### 8.1 Fluxo de Autenticação

<!-- guia: se o projeto não tem 2FA, simplifique o diagrama para uma etapa só. Não mantenha caixas que não existem. -->

```
┌─────────┐   credenciais   ┌────────────┐   {{ETAPA_2}}   ┌──────────────┐
│  Login  │ ──────────────► │ {{TELA_2}} │ ──────────────► │ Autenticado  │
└─────────┘                 └────────────┘                 └──────────────┘
```

O back-end delega a identidade a **{{PROVEDOR_AUTH}}** ou gerencia autenticação própria — descreva o fluxo real.

### 8.2 Emissão e Validação de Tokens

- **Access Token**: {{TIPO_ACCESS_TOKEN}} (ex: JWT assinado), validade de {{VALIDADE_ACCESS_TOKEN}}.
- **Refresh Token**: {{TIPO_REFRESH_TOKEN}}, validade de {{VALIDADE_REFRESH_TOKEN}}.
- **Validação**: assinatura verificada em {{PONTO_VALIDACAO_ASSINATURA}} a cada requisição autenticada.

### 8.3 Armazenamento de Credenciais

Senhas nunca são armazenadas em texto puro. Hash via **{{ALGORITMO_HASH_SENHA}}**, com {{CONFIG_HASH}} (ex: fator de custo, salt automático).

> Nunca logar senha, token completo ou hash em texto de log — ver seção 11.

### 8.4 Controle de Acesso (RBAC/Permissões)

| Papel | Código | Pode fazer |
|---|---|---|
| {{PAPEL_1}} | {{CODIGO_1}} | {{PERMISSOES_1}} |
| {{PAPEL_2}} | {{CODIGO_2}} | {{PERMISSOES_2}} |

> **Nota de segurança:** toda regra de permissão validada no front-end precisa ser **reaplicada** aqui. O back-end é a fonte de verdade de autorização — nunca confie em uma checagem feita só no cliente.

### 8.5 Middlewares e Guards de Segurança

- **{{MIDDLEWARE_AUTH}}**: valida o token e injeta o usuário autenticado no contexto da requisição.
- **{{MIDDLEWARE_PERMISSAO}}**: bloqueia a rota se o papel do usuário não tiver a permissão exigida.
- **{{MIDDLEWARE_RATE_LIMIT}}**: limita requisições por origem/usuário, se aplicável.

---

## 9. Contratos de Dados e Validação de Entrada

Todo endpoint define um DTO de entrada e um DTO de saída, validados com **{{LIB_VALIDACAO}}** antes de chegar à camada de aplicação.

```{{EXT_CODIGO}}
{{EXEMPLO_DTO}}
```

Validações aplicadas na borda da API:

- **{{VALIDACAO_1}}**: {{REGRA_1}}
- **{{VALIDACAO_2}}**: {{REGRA_2}}

> Toda validação replicada no front-end existe para experiência do usuário. A validação aqui é a que garante integridade dos dados — nunca é opcional.

---

## 10. Tratamento de Erros e Exceções

O back-end usa um **formato padronizado de erro**, retornado por um middleware/handler central em vez de cada endpoint tratar exceção individualmente:

```json
{
  "sucesso": false,
  "erro": {
    "codigo": "{{CODIGO_ERRO}}",
    "mensagem": "Descrição segura para o cliente",
    "detalhes": []
  }
}
```

| Tipo de erro | HTTP Status | Exemplo |
|---|---|---|
| Validação de entrada | 400 | Campo obrigatório ausente |
| Não autenticado | 401 | Token ausente ou expirado |
| Sem permissão | 403 | Papel sem acesso ao recurso |
| Recurso não encontrado | 404 | ID inexistente |
| Conflito de regra de negócio | 409 | Estado não permite a transição |
| Erro interno | 500 | Exceção não tratada |

> Mensagens de erro voltadas ao cliente nunca expõem stack trace, query SQL ou detalhes internos — isso vai para o log (seção 11), não para a resposta.

---

## 11. Sistema de Logging e Observabilidade

O módulo `{{ARQUIVO_LOGGER}}` implementa logging estruturado:

- **Níveis de log**: `trace`, `debug`, `info`, `warn`, `error`.
- **Contexto por requisição**: cada log carrega um identificador de correlação (`{{CAMPO_REQUEST_ID}}`) que permite rastrear uma requisição inteira através das camadas.
- **Logging condicional**: `trace`/`debug` só emitem saída fora de produção.

> Nunca logar senha, token, documento de identificação ou dado pessoal completo — ver 8.3.

<!-- guia: se o projeto tem métricas/tracing (Prometheus, OpenTelemetry, APM), documente aqui o que é coletado e onde é visualizado. -->

---

## 12. Integrações Externas

<!-- guia: uma linha por integração real. Remova a tabela se o backend não integra com nada externo. -->

| Integração | Protocolo | Finalidade | Tratamento de falha |
|---|---|---|---|
| `{{INTEGRACAO_1}}` | {{PROTOCOLO_1}} | {{FINALIDADE_1}} | {{TRATAMENTO_FALHA_1}} |
| `{{INTEGRACAO_2}}` | {{PROTOCOLO_2}} | {{FINALIDADE_2}} | {{TRATAMENTO_FALHA_2}} |

Timeout e retry: {{POLITICA_TIMEOUT_RETRY}}.

---

## 13. Jobs Agendados e Processos em Background

<!-- guia: apague esta seção se o backend não tem nenhum processo assíncrono/agendado. -->

| Job | Frequência | Finalidade | Idempotente? |
|---|---|---|---|
| `{{JOB_1}}` | {{FREQUENCIA_1}} | {{FINALIDADE_JOB_1}} | {{IDEMPOTENTE_1}} |

> Job que roda mais de uma vez (retry, deploy duplo, execução manual) precisa produzir o mesmo resultado — se não for idempotente, documente explicitamente o risco.

---

## 14. Testes

### 14.1 Testes Unitários

Cobrem regra de negócio isolada (domínio, casos de uso), sem tocar banco ou rede real. Framework: **{{FERRAMENTA_TESTE}}**.

```{{SHELL_PADRAO}}
{{CMD_TEST_UNITARIO}}
```

### 14.2 Testes de Integração

Cobrem a integração real com banco de dados (geralmente em container descartável) e, quando aplicável, endpoints completos.

```{{SHELL_PADRAO}}
{{CMD_TEST_INTEGRACAO}}
```

### 14.3 Cobertura

Meta mínima de cobertura: **{{COBERTURA_MINIMA}}%**, medida via **{{FERRAMENTA_COBERTURA}}** e verificada em CI (ver `ci-cd.yml`).

| Mudança | Teste esperado |
|---|---|
| Regra de negócio no domínio | Teste unitário cobrindo sucesso e falha |
| Permissão/status/acesso | Teste cobrindo usuário permitido e usuário bloqueado |
| Endpoint novo ou contrato alterado | Teste de integração do endpoint |
| Migration | Teste de integração validando o schema resultante |
| Bug corrigido | Teste que reproduz o bug antes do fix |

---

## 15. Containerização e Deploy

### 15.1 Docker e Multi-Stage Build

**Estágio 1 — Build** (`{{IMAGEM_BUILD}}`):
1. Instala o gerenciador de pacotes **{{GERENCIADOR_PACOTES}}**.
2. Copia lockfile/manifesto e instala dependências com versão travada (reprodutibilidade).
3. Copia o código-fonte e compila/publica, quando a linguagem exigir build.

**Estágio 2 — Runtime** (`{{IMAGEM_RUNTIME}}`):
1. Copia apenas os artefatos necessários para rodar (sem ferramentas de build).
2. Expõe a porta {{PORTA_CONTAINER}}.
3. Roda com usuário não-root, quando suportado pela imagem base.

### 15.2 Orquestração de Containers

O `docker-compose.yml` orquestra o serviço de back-end:

- **Porta**: mapeia `{{PORTA_HOST}}:{{PORTA_CONTAINER}}`.
- **Restart policy**: `unless-stopped`.
- **Dependências**: aguarda o banco de dados ficar saudável antes de subir.

### 15.3 Migrations em Produção

{{ESTRATEGIA_MIGRATION_PRODUCAO}} (ex: rodadas automaticamente no start do container, ou como um step manual/separado no pipeline de deploy — decisão relevante o suficiente para registrar aqui, não deixar implícita).

---

## 16. Variáveis de Ambiente e Configuração

| Variável | Descrição | Exemplo |
|---|---|---|
| `{{VAR_CONNECTION_STRING}}` | String de conexão com o banco | `postgresql://user:pass@host:porta/db` |
| `{{PREFIXO_VAR_AMBIENTE}}_PORT` | Porta em que a API sobe | `3000` |
| `{{PREFIXO_VAR_AMBIENTE}}_JWT_SECRET` | Segredo de assinatura de token | — |
| `{{PREFIXO_VAR_AMBIENTE}}_AMBIENTE` | Ambiente de execução | `production` |
| `{{PREFIXO_VAR_AMBIENTE}}_LOG_LEVEL` | Nível mínimo de log | `info` |

> Segredos reais nunca vão neste documento nem no repositório — apenas o nome da variável e um exemplo de formato.

---

## 17. Qualidade de Código e Ferramentas de Desenvolvimento

### Linter e Formatação

O **{{LINTER}}** garante estilo consistente e captura erros comuns antes do build.

### Scripts de Desenvolvimento

| Script | Comando | Descrição |
|---|---|---|
| `dev` | `{{CMD_DEV}}` | Sobe a API em modo desenvolvimento, com hot-reload |
| `build` | `{{CMD_BUILD}}` | Compila/publica para produção |
| `lint` | `{{CMD_LINT}}` | Executa análise estática |
| `test` | `{{CMD_TEST}}` | Executa a suíte de testes |
| `migrate` | `{{CMD_APLICAR_MIGRATION}}` | Aplica migrations pendentes |

---

## 18. Considerações Finais

O back-end do {{NOME_DO_SISTEMA}} foi desenvolvido com foco em **integridade de dados**, **segurança** e **rastreabilidade**. A escolha das tecnologias reflete {{JUSTIFICATIVA_STACK}}:

- **{{LINGUAGEM}} / {{FRAMEWORK}}** como base da API.
- **{{ORM}}** com migrations versionadas para persistência confiável.
- **Autenticação e RBAC** aplicados na borda e reforçados em toda camada de domínio.
- **Tratamento de erro centralizado** e logging estruturado com correlação por requisição.
- **Docker** para deploy reprodutível.

A separação entre domínio e infraestrutura permite trocar detalhes de implementação (banco, fila, provedor externo) sem reescrever regra de negócio.

---

## 19. Serviços Externos Consumidos

<!-- guia: use as seções 19 e 20 apenas quando este backend depende de outro serviço que ele não controla (ex: provedor de identidade externo, backend de domínio irmão). Em arquitetura monolítica e autocontida, apague ambas. -->

O {{NOME_DO_SISTEMA}} depende de **{{QTD_SERVICOS_EXTERNOS}} serviço(s) externo(s)**. Esta seção descreve o serviço de {{NOME_SERVICO_EXTERNO}}.

### 19.1 Visão Geral do Serviço

Acessível via `{{PREFIXO_VAR_AMBIENTE}}_URL_SERVICO_EXTERNO`, responsável por {{RESPONSABILIDADE_SERVICO_EXTERNO}}.

### 19.2 Endpoints e Recursos Consumidos

| Método HTTP | Endpoint | Finalidade |
|:---:|---|---|
| POST | `{{ENDPOINT_1}}` | {{FINALIDADE_ENDPOINT_1}} |
| GET | `{{ENDPOINT_2}}` | {{FINALIDADE_ENDPOINT_2}} |

### 19.3 Autenticação com o Serviço Externo

{{MECANISMO_AUTH_SERVICO_EXTERNO}} (ex: API key em header, mTLS, OAuth client credentials).

---

## 20. Relação entre Este Back-End e Outros Serviços

### 20.1 Arquitetura de Comunicação

```
┌──────────────────────┐        ┌──────────────────────┐
│   {{NOME_DO_SISTEMA}} │───────►│  {{SERVICO_EXTERNO}} │
│   (este back-end)     │◄───────│                       │
└──────────────────────┘        └──────────────────────┘
```

> Descreva se a comunicação é síncrona (HTTP) ou assíncrona (eventos/fila), e quem é dono de qual dado.

### 20.2 Consistência entre Serviços

{{ESTRATEGIA_CONSISTENCIA}} (ex: escrita dupla com compensação manual, evento publicado após commit local, saga).

### 20.3 Tratamento de Falhas Parciais

Descreva o comportamento real quando uma escrita local sucede mas a chamada ao serviço externo falha (ou vice-versa): retry automático, fila de reprocessamento, ou intervenção manual registrada em log.

---

## Como adaptar este template a um novo projeto

<!-- guia: apague esta seção inteira depois de preencher. -->

1. **Remova antes de preencher.** Corte as seções que não existem no projeto (mensageria, jobs, multi-serviço) antes de começar a escrever — evita ficar arrastando placeholder de algo que nunca vai existir.
2. **Renumere o Sumário** depois de remover seções.
3. **Descreva o que existe, não o que se pretende fazer.** Onde houver intenção futura, marque como "Previsto" ou "Não implementado".
4. **Mantenha os avisos de segurança.** Os blocos sobre revalidação de permissão no back-end, hashing de senha e logging de dados sensíveis valem para qualquer projeto.
5. **Prefira tabela a prosa** para rotas, permissões, variáveis e integrações.
6. **Registre a decisão, não só a escolha.** "Usamos {{ORM}}" é inútil daqui a seis meses; "usamos {{ORM}} porque X" evita que alguém desfaça a escolha sem saber o custo.
7. **Mantenha alinhado com `DOCUMENTACAO_FRONTEND.md`.** Se o front-end tem uma seção 19/20 descrevendo este backend do ponto de vista do cliente, confirme que as duas versões não se contradizem.
8. **Datar e versionar** ao fechar o documento, como no rodapé abaixo.

---

*Documento gerado em {{MES_ANO}}.*
*Versão do sistema documentada: {{NOME_DO_SISTEMA}} Back-End v{{VERSAO}}.*
