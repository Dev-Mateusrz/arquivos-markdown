<!--
Template reutilizável. Copie para `docs/arquitetura.md` no repositório de
backend, substitua os {{PLACEHOLDERS}} e apague este comentário e a seção
"Como adaptar" ao final. Usa os mesmos placeholders de AGENTS.md — mantenha
os dois arquivos consistentes.
-->

# Arquitetura

{{ESTILO_ARQUITETURA}} (ports and adapters) em quatro projetos. A regra que sustenta tudo:
**o domínio e as regras de negócio não dependem de detalhe de infraestrutura.**

## Os quatro projetos

```
{{PREFIXO_NAMESPACE}}.Api  ──────────▶  {{PREFIXO_NAMESPACE}}.Application  ──▶  {{PREFIXO_NAMESPACE}}.Domain
{{PREFIXO_NAMESPACE}}.Infrastructure ▶  {{PREFIXO_NAMESPACE}}.Application  ──▶  {{PREFIXO_NAMESPACE}}.Domain
```

| Projeto | Responsabilidade | O que nunca entra |
| --- | --- | --- |
| `{{PREFIXO_NAMESPACE}}.Domain` | Entidades, invariantes, regras de negócio | ORM, driver de banco, framework web — **nenhuma dependência externa** |
| `{{PREFIXO_NAMESPACE}}.Application` | Casos de uso, commands, queries, DTOs, ports | Implementação concreta de infraestrutura |
| `{{PREFIXO_NAMESPACE}}.Infrastructure` | {{ORM}}, {{BANCO_DE_DADOS}}, migrations, integrações | Regra de negócio |
| `{{PREFIXO_NAMESPACE}}.Api` | Endpoints, DI, autenticação, middleware, OpenAPI | Regra de negócio |

A ausência de dependências no `{{PREFIXO_NAMESPACE}}.Domain` é verificável — na stack .NET, por
exemplo:

```bash
dotnet list src/{{PREFIXO_NAMESPACE}}.Domain/{{PREFIXO_NAMESPACE}}.Domain.csproj package --include-transitive
```

Se algum dia aparecer alguma coisa aí, uma regra de negócio começou a depender de
infraestrutura — e o custo disso aparece quando você tentar testar essa regra ou trocar o
banco.

## Por que a Api referencia a Infrastructure

Ela referencia, mas só como **composition root**: o ponto de entrada da aplicação
registra as implementações no contêiner de injeção de dependências. Nenhum endpoint conversa com
infraestrutura direto — quando existirem casos de uso, o endpoint vai falar com a
`Application`.

É o arranjo pragmático padrão nesta stack. A alternativa purista (um quinto projeto só para
composição) resolve um problema que a maioria dos times não tem.

<!-- guia: se o projeto de Application está vazio no início (comum quando o primeiro card
entrega só o modelo de dados), explique isso aqui — evita que alguém "preencha" o projeto
com abstração sem consumidor só para não deixá-lo vazio. -->

## Onde colocar cada coisa

**Regra de negócio invariante** — dentro da entidade, no construtor ou no método que altera
estado. Uma entidade não deixa existir num estado inconsistente; isso é do domínio.

**Regra que depende de outros agregados ou de consulta** — caso de uso na `Application`.
Uma regra que precisa olhar o banco (ex.: "não pode haver dois registros com a mesma chave
natural") é caso de uso — e, por ser regra que não pode ser furada, também vira constraint
no banco.

**Detalhe de como persistir** — `Infrastructure`. O domínio não sabe que existe uma coluna
`snake_case` ou qual é o nome real da tabela.

**Tradução de erro para HTTP** — `Api`. Uma exceção de domínio virar um status HTTP
específico é decisão de contrato HTTP, não de domínio.

## Idioma

<!-- guia: ajuste ao vocabulário real do domínio do novo projeto — ou apague esta seção se
o projeto for monolíngue. -->

Domínio em {{IDIOMA_DOMINIO}} — `{{ENTIDADE_EXEMPLO_1}}`, `{{ENTIDADE_EXEMPLO_2}}`. É a linguagem do
negócio, do rastreador de issues e das conversas com quem pede a funcionalidade; traduzir os
termos do domínio só criaria um dicionário para todo mundo consultar.

Técnico em inglês — `GetByIdAsync`, `CancellationToken`, `IEntityTypeConfiguration`. É a
linguagem da stack, e misturar os dois no mesmo método deixaria o código bilíngue.

## Leia também

- [Banco de dados](banco-de-dados.md) — modelo, migrations e políticas
- [Decisões](decisoes.md) — o registro do que foi decidido e por quê
- [`AGENTS.md`](../AGENTS.md) — as regras de engenharia que valem para todo código

<!--
Como adaptar este template a um novo projeto (apague este bloco):
1. Substitua os placeholders — mantenha-os idênticos aos de AGENTS.md.
2. Se a arquitetura não for hexagonal em quatro projetos, redesenhe o
   diagrama e a tabela de camadas, mas preserve a seção "Onde colocar cada
   coisa": é a parte mais consultada no dia a dia, independente do estilo
   arquitetural escolhido.
-->
