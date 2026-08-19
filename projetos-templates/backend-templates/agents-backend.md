<!--
Template reutilizável. Copie para `AGENTS.md` na raiz do repositório de
backend, substitua os {{PLACEHOLDERS}} e apague este comentário e a seção
"Como adaptar" ao final.

Placeholders deste template:
  {{NOME_DO_SISTEMA}}          Nome do sistema                                   (ex.: GIPE)
  {{PREFIXO_NAMESPACE}}        Prefixo comum dos projetos/namespaces do backend  (ex.: Gipe — vira Gipe.Domain, Gipe.Application...)
  {{RUNTIME_BACKEND}}          Runtime/versão da linguagem                        (ex.: .NET 10)
  {{LINGUAGEM_BACKEND}}        Linguagem                                          (ex.: C#)
  {{FRAMEWORK_BACKEND}}        Framework web                                      (ex.: ASP.NET Core Web API)
  {{BANCO_DE_DADOS}}           SGBD                                               (ex.: PostgreSQL)
  {{ORM}}                      ORM/camada de acesso a dados                       (ex.: EF Core)
  {{ESTILO_ARQUITETURA}}       Estilo arquitetural adotado                        (ex.: Arquitetura Hexagonal)
  {{ARQUIVO_VERSOES_PACOTES}}  Onde as versões de pacote ficam centralizadas      (ex.: Directory.Packages.props)
  {{EXCECAO_REGRA_DE_NEGOCIO}} Nome da exceção de domínio usada para violação de regra (ex.: RegraDeNegocioException)
  {{PREFIXO_ISSUE_MAIUSCULO}}  Prefixo da issue no rastreador                     (ex.: SG)

Este documento assume uma stack .NET + EF Core + banco relacional em
arquitetura hexagonal — é a combinação mais comum nos backends deste time.
Se o novo projeto usa outra stack (Node, Java, Go...), mantenha a estrutura
das seções e troque os detalhes técnicos (EF Core vira o ORM equivalente,
`CancellationToken` vira o mecanismo de cancelamento da linguagem, etc.) —
os princípios (regra de dependência entre camadas, sem superengenharia,
prioridades de engenharia) são portáveis entre stacks.
-->

# backend-{{NOME_DO_SISTEMA_KEBAB}} — regras de engenharia

Backend do {{NOME_DO_SISTEMA}}. Estas regras valem para todo código produzido neste repositório.
Leia antes de escrever qualquer coisa.

O detalhamento de cada tema está em [`docs/`](docs/) — em especial
[arquitetura](docs/arquitetura.md), [banco de dados](docs/banco-de-dados.md) e
[decisões](docs/decisoes.md), que registram o porquê de cada escolha. Antes de mudar algo
que pareça estranho, confira se não há decisão documentada por trás.

## Stack

{{RUNTIME_BACKEND}} · {{LINGUAGEM_BACKEND}} · {{FRAMEWORK_BACKEND}} · {{BANCO_DE_DADOS}} · {{ORM}} · OpenAPI · {{ESTILO_ARQUITETURA}}.

Versões dos pacotes ficam centralizadas em `{{ARQUIVO_VERSOES_PACOTES}}`. Não versione pacote
solto no arquivo de projeto.

**Não adicione dependência sem necessidade real.** Antes de incluir um pacote, verifique se
o problema não se resolve com a biblioteca padrão ou com o que já está no projeto. Se incluir, deixe o
motivo explícito.

## Camadas e regra de dependência

```
{{PREFIXO_NAMESPACE}}.Api  ──▶  {{PREFIXO_NAMESPACE}}.Application  ──▶  {{PREFIXO_NAMESPACE}}.Domain
{{PREFIXO_NAMESPACE}}.Infrastructure  ──▶  {{PREFIXO_NAMESPACE}}.Application  ──▶  {{PREFIXO_NAMESPACE}}.Domain
```

| Projeto | Responsabilidade | Nunca contém |
| --- | --- | --- |
| `{{PREFIXO_NAMESPACE}}.Domain` | Entidades, invariantes, regras de negócio | ORM, driver de banco, framework web, qualquer dependência externa |
| `{{PREFIXO_NAMESPACE}}.Application` | Casos de uso, commands, queries, DTOs, ports | Implementação concreta de infraestrutura |
| `{{PREFIXO_NAMESPACE}}.Infrastructure` | {{ORM}}, repositórios, integrações, cache, mensageria | Regra de negócio |
| `{{PREFIXO_NAMESPACE}}.Api` | Endpoints, DI, autenticação, middleware, OpenAPI | Regra de negócio |

`{{PREFIXO_NAMESPACE}}.Api` referencia `{{PREFIXO_NAMESPACE}}.Infrastructure` **apenas como composition root** — o ponto de
entrada da aplicação registra as implementações no contêiner. Nenhum endpoint fala com infraestrutura direto.

O domínio não conhece Infrastructure nem Api. A Application depende de abstrações, não de
implementações.

<!-- guia: se o projeto ainda não tem casos de uso (Application vazio), diga isso explicitamente — abstração sem consumidor é o que a seção "Não superengenharie" abaixo proíbe. -->

## Idioma

<!-- guia: descreva a convenção real do projeto. O exemplo abaixo reflete um domínio em
português (linguagem do negócio) com código técnico em inglês — troque pelos termos do
domínio do novo projeto, ou apague se o projeto for monolíngue. -->

Domínio em {{IDIOMA_DOMINIO}} (ex.: `{{ENTIDADE_EXEMPLO_1}}`, `{{ENTIDADE_EXEMPLO_2}}`) — é a linguagem do
negócio e do rastreador de issues. Técnico em inglês (`GetByIdAsync`, `CancellationToken`,
`IEntityTypeConfiguration`). Tabelas e colunas em `snake_case`, aplicado automaticamente por
convenção de nomenclatura do ORM.

## Banco

- `appsettings.Development.json` carrega o acesso completo ao banco de desenvolvimento,
  senha inclusive — decisão do time, para não exigir configuração manual em cada máquina.
- **Produção é outra história: senha de produção nunca entra em arquivo.** Ela vem de
  variável de ambiente no servidor ou do cofre de segredos. O mesmo vale para
  qualquer token, chave de API ou certificado.
- Configuração incompleta derruba a aplicação no start, com a mensagem do que falta. Subir
  apontando para o banco errado é pior do que não subir.
- **Migration não roda no boot.** Se o banco de dev é compartilhado entre o time, aplicar é
  ato deliberado, não automático.
- Toda mudança de esquema entra por migration, e a migration precisa ser **reversível**.
- **Chaves primárias**: `int`/identity em tabelas de cadastro pequenas e estáveis — leem
  melhor, ocupam menos e são conferíveis a olho. `uuid` (versão ordenável no tempo, quando
  disponível na stack) onde o identificador circula fora do sistema, aparece em URL ou
  precisa não ser adivinhável.
- Quando uma tabela tiver seed com ID fixo, comece a identidade acima da faixa reservada —
  senão o primeiro registro criado colide com o seed.
- Dado de referência (estrutura real do domínio) vai na migration, com identificadores
  fixos. Dado de teste vai em um seed próprio, que só roda em ambiente de desenvolvimento.
- Índice tem custo de escrita e manutenção. Crie conforme padrão real de consulta, não por
  precaução. Ao declarar dois índices sobre a mesma coluna, nomeie-os explicitamente no
  modelo — sem isso alguns ORMs tratam como um só e mantêm o último.
- Regra que não pode ser furada deve ser garantida por constraint, não só por código.

## {{ORM}}

Priorize: leitura sem tracking quando o resultado não será alterado, projeção explícita dos
campos usados, filtro e paginação executados no banco, carregamento só do necessário,
operações assíncronas.

Evite: eager loading indiscriminado, materialização prematura, N+1, buscar tudo e filtrar
em memória.

```{{EXT_CODIGO_BACKEND}}
// não
var todos = await db.{{ENTIDADE_EXEMPLO_2}}s.ToListAsync(ct);
var ativos = todos.Where(u => u.Ativo);

// sim
var ativos = await db.{{ENTIDADE_EXEMPLO_2}}s.AsNoTracking()
    .Where(u => u.Ativo)
    .Select(u => new {{ENTIDADE_EXEMPLO_2}}Resumo(u.Id, u.Nome))
    .ToListAsync(ct);
```

## Assincronismo

`async`/`await` para todo I/O. Nunca bloqueie uma chamada assíncrona esperando o resultado
de forma síncrona. Propague o token/sinal de cancelamento de ponta a ponta: endpoint → caso
de uso → repositório → banco.

## API e OpenAPI

**Feature só está concluída com a documentação sincronizada.** Alterou endpoint, rota,
request, response, DTO, status code, validação, paginação, filtro ou autenticação? A
documentação OpenAPI muda junto, no mesmo commit.

A documentação descreve comportamento, não repete o nome do método. `Gets user` não serve;
"Obtém os dados detalhados de um usuário pelo identificador. Retorna 404 quando não existe"
serve. Documente parâmetros, obrigatoriedade, validações, exemplos e **todos** os status
codes que a implementação realmente produz.

Status codes com significado correto. Nunca `200 OK` para erro de negócio.

Não exponha entidade de domínio nem entidade do ORM na API — use DTO de entrada e de saída.

Endpoints leves: recebem, delegam ao caso de uso, mapeiam o resultado, devolvem HTTP.

## Erros

Estratégia centralizada, nunca `try/catch` espalhado por endpoint. Respostas seguem RFC 9457
(`application/problem+json`) com identificador de correlação (`traceId`). Violação de invariante de domínio
(`{{EXCECAO_REGRA_DE_NEGOCIO}}`) vira **422**.

Nunca exponha stack trace, connection string, credencial ou detalhe de infraestrutura — nem
em resposta de erro, nem em log.

## Antes de implementar

Responda para si mesmo: qual é o problema, de que camada é a responsabilidade, qual o custo em
tempo/espaço/consultas ao banco, existe N+1, dá para ser assíncrono, precisa de
cancelamento, muda o contrato da API, o OpenAPI precisa mudar, precisa de teste, tem
risco de segurança, e — sempre — existe solução mais simples.

## Não superengenharie

Nada de abstração sem consumidor, interface para tudo, camada extra, factory ou wrapper por
simetria. Arquitetura robusta não é arquitetura burocrática. A melhor solução resolve o
problema com a menor complexidade necessária.

## Ao alterar código existente

Entenda antes. Identifique dependências e impactos. Faça a menor alteração que resolve.
Preserve comportamento que não precisava mudar. Confira performance, testes, OpenAPI, banco e
se a regra de dependência continua respeitada. Não faça refactor gigante sem necessidade.

## Prioridades, nesta ordem

Correção · Segurança · Arquitetura · Performance · Manutenibilidade · Clareza · Simplicidade.

Nunca sacrifique correção ou segurança por performance prematura.

## Fluxo de trabalho

Veja [CONTRIBUTING.md](CONTRIBUTING.md). Branch e commit carregam o ID do card
(`feat/{{PREFIXO_ISSUE_MAIUSCULO}}-12-...`, `feat({{PREFIXO_ISSUE_MAIUSCULO}}-12): ...`) — é o que move o rastreador automaticamente.

<!--
Como adaptar este template a um novo projeto (apague este bloco):
1. Substitua os placeholders do topo, inclusive {{NOME_DO_SISTEMA_KEBAB}} no
   título (ex.: "gipe" para "GIPE").
2. Se a stack não é .NET/EF Core, reescreva as seções "Banco" e "{{ORM}}"
   com os equivalentes reais (ex.: Prisma/TypeORM em Node, JPA/Hibernate em
   Java) — mantenha o espírito das regras (sem N+1, sem tracking
   desnecessário, migrations reversíveis), não necessariamente a sintaxe.
3. Ajuste a seção "Idioma" ao vocabulário real do domínio do novo projeto.
4. Mantenha "Prioridades, nesta ordem" a menos que o time decida
   explicitamente outra ordem — é a seção mais citada quando duas pessoas
   discordam de uma escolha técnica.
-->
