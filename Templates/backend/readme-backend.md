<!--
Template reutilizável. Copie para `README.md` na raiz do repositório de
backend, substitua os {{PLACEHOLDERS}} e apague este comentário e a seção
"Como adaptar" ao final. Usa os mesmos placeholders dos demais arquivos deste
docs-template.

Placeholders adicionais deste arquivo:
  {{REPO_SLUG}}          nome do repositório no GitHub                (ex.: backend-gipe)
  {{NOME_SISTEMA_TESTES}} variável de ambiente com a connection string de testes (ex.: GIPE_TEST_POSTGRES)
-->

# {{REPO_SLUG}}

Backend do **{{NOME_DO_SISTEMA}} — {{NOME_POR_EXTENSO}}**, {{OBJETIVO_DO_SISTEMA}}.

<!-- guia: se houver algo que o sistema explicitamente NÃO é (ferramenta de outra coisa,
etapa que antecede outro processo), diga aqui — é a frase que mais evita mal-entendido de
escopo em quem chega agora. -->

| | |
| --- | --- |
| **Frontend** | [`{{REPO_FRONTEND}}`]({{URL_REPO_FRONTEND}}) |
| **Board** | [{{CHAVE_PROJETO_TRACKER}} (`{{PREFIXO_ISSUE_MAIUSCULO}}`)]({{URL_BOARD_TRACKER}}) |
| **Stack** | {{RUNTIME_BACKEND}} · {{FRAMEWORK_BACKEND}} · {{BANCO_DE_DADOS}} {{VERSAO_BANCO}} · {{ORM}} · OpenAPI · {{ESTILO_ARQUITETURA}} |

---

## Sumário da documentação

Comece pelo que você precisa fazer:

| Documento | Leia quando precisar de |
| --- | --- |
| **[Domínio](docs/dominio.md)** | Entender o vocabulário do negócio. **Leia antes do primeiro card** |
| **[Arquitetura](docs/arquitetura.md)** | Saber onde colocar o código que você vai escrever, e por que as camadas são assim |
| **[Banco de dados](docs/banco-de-dados.md)** | Criar ou aplicar migration, entender o modelo, as constraints e a carga de dados |
| **[Configuração](docs/configuracao.md)** | Apontar para outro ambiente, mexer em segredo, entender por que a aplicação não sobe |
| **[API](docs/api.md)** | Criar endpoint, tratar erro, sincronizar o OpenAPI |
| **[Decisões](docs/decisoes.md)** | Descobrir por que algo foi feito de um jeito estranho — antes de mudar |

E na raiz do repositório:

| Documento | Sobre |
| --- | --- |
| **[`AGENTS.md`](AGENTS.md)** | Regras de engenharia obrigatórias para todo código deste repositório |
| **[`CONTRIBUTING.md`](CONTRIBUTING.md)** | Fluxo de branches, padrão de commit e como o card anda sozinho no rastreador |

---

## Rodando

Pré-requisitos: {{PREREQUISITOS_RUNTIME}}.

```bash
{{CMD_INSTALAR_FERRAMENTAS_BACKEND}}
```

<!-- guia: descreva se o banco de desenvolvimento é compartilhado (servidor do time, sem
Docker local) ou local (docker-compose). O exemplo abaixo assume compartilhado — ajuste se
for diferente. -->

O banco é {{DESCRICAO_BANCO_DEV}}. O acesso
já está em `src/{{PREFIXO_NAMESPACE}}.Api/appsettings.Development.json`, então basta:

```bash
{{CMD_RUN_BACKEND}}
```

Para compilar tudo e executar os testes automatizados:

```bash
{{CMD_BUILD_BACKEND}}
{{CMD_TEST_BACKEND}}
```

<!-- guia: esta subseção só se aplica quando os testes de integração exigem um banco real
descartável, provisionado via variável de ambiente com allowlist de nome. Simplifique ou
apague se o projeto usar apenas testes com dependências fake/em memória. -->

Os testes relacionais usam o mesmo {{BANCO_DE_DADOS}} adotado pelo projeto. Para executá-los
localmente, defina `{{NOME_SISTEMA_TESTES}}` com a conexão de um banco exclusivo para testes — só
são aceitos nomes dentro de um padrão fixo (allowlist), e por ser allowlist a recusa alcança
também os ambientes que ninguém listou, produção inclusive. Cada teste cria um schema
temporário com nome aleatório, aplica as migrations reais e remove o schema ao terminar. Na
CI, o banco descartável é provisionado automaticamente.

Sem a variável, os testes de integração com banco são explicitamente ignorados; compilação e
demais validações continuam disponíveis.

- Swagger UI — http://localhost:{{PORTA_BACKEND_DEV}}/swagger
- Health check — http://localhost:{{PORTA_BACKEND_DEV}}/health

Se faltar configuração, a aplicação **não sobe** e diz exatamente o que falta. É proposital:
subir apontando para o banco errado é pior do que não subir. Detalhes em
[configuração](docs/configuracao.md).

### Ative os hooks de commit

Uma vez por clone. Sem isso os commits saem fora do padrão e o card não anda no rastreador:

```bash
git config core.hooksPath .githooks
```

---

## Estrutura do repositório

```
src/
  {{PREFIXO_NAMESPACE}}.Domain           entidades e invariantes — sem nenhuma dependência externa
  {{PREFIXO_NAMESPACE}}.Application      casos de uso e ports
  {{PREFIXO_NAMESPACE}}.Infrastructure   {{ORM}}, {{BANCO_DE_DADOS}}, migrations, seed
  {{PREFIXO_NAMESPACE}}.Api              endpoints, DI, OpenAPI, tratamento de erro
tests/
  {{PREFIXO_NAMESPACE}}.Infrastructure.Tests  testes relacionais do modelo e das constraints
docs/                   documentação (veja o sumário acima)
tools/                  scripts de apoio
artifacts/              saída gerada — ignorado pelo git
```

---

## Estado atual

<!-- guia: mantenha esta tabela e esta lista de rotas curtas e atualizadas — é o resumo que
alguém lê antes de entrar numa reunião de planejamento. Detalhe fica em docs/decisoes.md e
docs/api.md. -->

| Card | O que entregou |
| --- | --- |
| **{{PREFIXO_ISSUE_MAIUSCULO}}-XX** | {{RESUMO_ENTREGA_1}} |
| **{{PREFIXO_ISSUE_MAIUSCULO}}-XX** | {{RESUMO_ENTREGA_2}} |

```
/health
/auth/login  /auth/refresh  /auth/logout  /auth/me
```

Ainda **não** existem: {{FUNCIONALIDADES_PENDENTES}}.

---

## Como trabalhamos

```
feat|fix|hotfix/{{PREFIXO_ISSUE_MAIUSCULO}}-000-descricao  ──PR──▶  {{BRANCH_DESENVOLVIMENTO}}  ──PR──▶  {{BRANCH_PRODUCAO}}
```

Commits no formato `<tipo>({{PREFIXO_ISSUE_MAIUSCULO}}-000): descrição`. O ID do card é o que move o board sozinho —
e você não precisa digitá-lo: se a branch se chama `feat/{{PREFIXO_ISSUE}}-42-...`, o hook injeta.

Tudo em [`CONTRIBUTING.md`](CONTRIBUTING.md).

<!--
Como adaptar este template a um novo projeto (apague este bloco):
1. Substitua os placeholders — mantenha-os idênticos aos usados em
   AGENTS.md, docs/arquitetura.md, docs/banco-de-dados.md, docs/configuracao.md
   e docs/api.md, para os cinco arquivos concordarem entre si.
2. Reescreva "Estado atual" a cada entrega relevante — é a seção que mais
   envelhece rápido.
3. Se o repositório não tiver frontend irmão, apague a linha correspondente
   da primeira tabela.
-->
