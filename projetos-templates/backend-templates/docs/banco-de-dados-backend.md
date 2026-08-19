<!--
Template reutilizável. Copie para `docs/banco-de-dados.md` no repositório de
backend, substitua os {{PLACEHOLDERS}} e apague este comentário e a seção
"Como adaptar" ao final. Usa os mesmos placeholders de AGENTS.md/arquitetura.md.

Placeholders adicionais deste arquivo:
  {{SCHEMA_BANCO}}         schema usado em desenvolvimento           (ex.: meusistema-dev)
  {{TABELA_A}}, {{TABELA_B}}, {{TABELA_C}}   nomes de tabela de exemplo, minúsculo/snake_case
  {{FAIXA_SEED_FIM}}       último ID reservado ao seed antes de a identity assumir (ex.: 100)
  {{SCRIPT_DADOS_PESSOAIS}} script que carrega dado pessoal fora do controle de versão (ex.: tools/Gerar-ContatoSql.ps1)
-->

# Banco de dados

{{BANCO_DE_DADOS}} {{VERSAO_BANCO}}<!-- guia: diga aqui se o banco é exclusivo deste sistema ou compartilhado com outros --> . O {{NOME_DO_SISTEMA}} vive em um schema
próprio por ambiente — `{{SCHEMA_BANCO}}` em desenvolvimento.

## Schema por ambiente, via `search_path`

<!-- guia: esta seção só se aplica a Postgres (ou bancos com o mesmo conceito de search
path/schema por conexão). Se o projeto usa um banco por ambiente em vez de um schema por
ambiente, reescreva a seção descrevendo essa estratégia. -->

O schema **não** é fixado no modelo do ORM. Ele entra como `search_path` da conexão, montado
a partir de uma chave de configuração. A consequência prática é que **a mesma migration serve para
todos os ambientes**: dev grava em `{{SCHEMA_BANCO}}`, produção gravará no schema dela, sem regerar
nada e sem `if` no código.

O `search_path` não cria schema. Antes da primeira migration em um ambiente novo:

```sql
CREATE SCHEMA IF NOT EXISTS "{{SCHEMA_BANCO_PROD}}";
```

Como o `search_path` padrão do servidor costuma ser `"$user", public`, um cliente SQL conectado sem
configuração **não enxerga as tabelas do {{NOME_DO_SISTEMA}}**. Consulte assim:

```sql
SELECT * FROM "{{SCHEMA_BANCO}}".{{TABELA_A}};
-- ou
SET search_path TO "{{SCHEMA_BANCO}}";
```

## Modelo

<!-- guia: substitua pelo diagrama real de entidades e relacionamentos do novo projeto —
este é apenas um esqueleto ilustrando o nível de detalhe esperado (chave, cardinalidade,
papel de cada tabela em uma frase). -->

```
{{TABELA_A}} ──┬──< {{TABELA_B}} ──< {{TABELA_C}}
               │
               └── (relação direta, quando houver)
```

| Tabela | Chave | Papel |
| --- | --- | --- |
| `{{TABELA_A}}` | `int` identity | {{PAPEL_TABELA_A}} |
| `{{TABELA_B}}` | `int` identity | {{PAPEL_TABELA_B}} |
| `{{TABELA_C}}` | `uuid` (ordenável no tempo) | {{PAPEL_TABELA_C}} |

### Chaves: `int` em umas, `uuid` em outras

Tabelas de cadastro pequenas, estáveis e que não circulam fora do sistema usam `int`
identity — lê melhor, ocupa menos e é conferível a olho numa consulta.

Entidades cujo identificador aparece em URL, é referenciado externamente ou não deve ser
adivinhável usam `uuid` numa variante ordenável no tempo (ex.: UUID v7), quando a stack
oferece: sequencial o suficiente para não fragmentar índice como um UUID v4 puramente
aleatório, mas não sequencial ao ponto de ser adivinhável.

### A faixa 1–{{FAIXA_SEED_FIM}} é reservada ao seed

Os registros semeados têm ID fixo (para a migration ser determinística). A identidade dessas
tabelas começa em **{{FAIXA_SEED_FIM}}** — sem isso, o primeiro registro criado pela aplicação
colidiria com o seed.

Ao criar uma tabela nova com seed de ID fixo, repita o padrão (exemplo em EF Core):

```{{EXT_CODIGO_BACKEND}}
builder.Property(x => x.Id)
    .UseIdentityByDefaultColumn()
    .HasIdentityOptions(startValue: {{FAIXA_SEED_FIM}});
```

### Regras garantidas pelo banco

Regra que não pode ser furada não fica só no código:

| Constraint | O que impede |
| --- | --- |
| `{{NOME_CONSTRAINT_1}}` | {{DESCRICAO_CONSTRAINT_1}} |
| `{{NOME_CONSTRAINT_2}}` | {{DESCRICAO_CONSTRAINT_2}} |
| FKs em `RESTRICT` | Apagar um registro que ainda tem dependentes |

<!-- guia: liste aqui toda constraint que expressa uma regra de negócio — é o inventário
que qualquer revisão de schema deveria conferir antes de remover uma constraint "estranha". -->

### Enums são gravados como texto

Campos de conjunto fechado e estrutural (ex.: um status interno) viram `varchar` com CHECK,
não enum nativo do banco nem tabela de domínio separada. O valor continua legível num dump
ou numa consulta manual, e não quebra se a ordem do enum mudar no código. Alterar um enum
nativo em migration costuma ser doloroso; tabela de domínio é peso demais para um conjunto
fechado.

**Cadastro administrável é o caso oposto:** algo que um administrador pode criar pela tela
(ex.: uma categoria) vive numa tabela própria, nunca em enum, constante ou CHECK de valores
fixos — criar um valor novo não pode exigir deploy.

## Migrations

<!-- guia: ajuste os comandos ao ORM/ferramenta real do projeto. O exemplo abaixo é EF Core. -->

Ficam em `src/{{PREFIXO_NAMESPACE}}.Infrastructure/Persistence/Migrations`.

**Migration não é aplicada no boot da aplicação**, se o banco de desenvolvimento é
compartilhado pelo time: se cada máquina aplicasse a sua ao subir, duas branches diferentes
disputariam o esquema e a primeira a rodar quebraria a outra. Aplicar é ato deliberado.

Criar:

```bash
dotnet ef migrations add NomeDaMigration --project src/{{PREFIXO_NAMESPACE}}.Infrastructure --startup-project src/{{PREFIXO_NAMESPACE}}.Api --output-dir Persistence/Migrations
```

Aplicar em desenvolvimento:

```bash
dotnet ef database update --project src/{{PREFIXO_NAMESPACE}}.Infrastructure --startup-project src/{{PREFIXO_NAMESPACE}}.Api
```

Gerar o script para produção — sempre revisado antes, nunca `database update` direto:

```bash
dotnet ef migrations script --idempotent --project src/{{PREFIXO_NAMESPACE}}.Infrastructure --startup-project src/{{PREFIXO_NAMESPACE}}.Api --output artifacts/migration.sql
```

Toda migration precisa ser **reversível**: o `Down()` (ou equivalente) tem que desfazer o que
o `Up()` fez.

Dois detalhes que costumam custar tempo:

- Depois de `migrations add`, **recompile** antes de aplicar sem rebuild. Senão a ferramenta
  usa o assembly anterior e acusa mudança de modelo pendente por engano.
- Para declarar dois índices sobre a mesma coluna, nomeie-os explicitamente no modelo. Sem o
  nome, alguns ORMs tratam como um índice só e mantêm apenas o último.

## Dados de referência e dados pessoais

<!-- guia: esta seção só se aplica quando a migration carrega dado real de referência
(estrutura organizacional, catálogo). Apague se o projeto não tiver esse caso. -->

O seed da migration traz a estrutura de referência que já existe fora do sistema. São dados
de referência — valem em todos os ambientes.

**Dado pessoal identificável (e-mail, telefone, endereço) não entra na migration.** Uma vez
versionado, ficaria no histórico do Git permanentemente, em todo clone. Esses dados entram por
script gerado a partir da fonte de origem:

```{{SHELL_PADRAO}}
{{SCRIPT_DADOS_PESSOAIS}} -Planilha <caminho> -Schema {{SCHEMA_BANCO}}
```

```bash
psql "<connection string>" -v ON_ERROR_STOP=1 -f artifacts/contato.sql
```

O gerador é versionado (não contém dado nenhum); a saída vai para uma pasta que o
`.gitignore` exclui. O script é idempotente.

Um ambiente recriado do zero funciona sem ele: os campos ficam nulos até alguém preencher.
Mas **a migration sozinha não reproduz esse dado** — se recriar o banco, reaplique o script.

## Leia também

- [Configuração](configuracao.md) — como apontar para cada ambiente
- [Domínio](dominio.md) — o vocabulário do negócio
- [Decisões](decisoes.md) — o porquê de cada escolha acima

<!--
Como adaptar este template a um novo projeto (apague este bloco):
1. Substitua os placeholders — mantenha-os idênticos aos de AGENTS.md e
   arquitetura.md.
2. Redesenhe a seção "Modelo" com o diagrama e a tabela reais do projeto.
3. Se o banco não for compartilhado com outros sistemas, simplifique ou
   remova a seção "Schema por ambiente".
4. Se não houver dado pessoal fora do controle de versão, apague a última
   seção inteira.
-->
