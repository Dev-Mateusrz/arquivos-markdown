<!--
Template reutilizável. Copie para `docs/configuracao.md` no repositório de
backend, substitua os {{PLACEHOLDERS}} e apague este comentário e a seção
"Como adaptar" ao final. Usa os mesmos placeholders dos demais arquivos de
docs/ deste template.
-->

# Configuração

A aplicação roda em qualquer ambiente sem alteração de código. O que muda é configuração, e
ela vem de {{QTD_FONTES_CONFIG}} fontes, nesta ordem de precedência (a de baixo vence):

```
appsettings.json                  base comum
appsettings.{Ambiente}.json       por ambiente, versionado
appsettings.Local.json            sua máquina, ignorado pelo git
User Secrets                      sua máquina, fora do repositório
Variáveis de ambiente             servidor
```

Qualquer chave vira variável de ambiente trocando `:` por `__` — ex.: `Database__Host`,
`Database__Password`.

## Chaves

<!-- guia: liste as chaves reais do projeto. A tabela abaixo é um esqueleto com as
categorias mais comuns (banco, autenticação, borda/proxy). -->

| Chave | Onde vive | Observação |
| --- | --- | --- |
| `Database:Host`, `:Port` | `appsettings.{Ambiente}.json` | |
| `Database:Name` | `appsettings.{Ambiente}.json` | Nome da base |
| `Database:Schema` | `appsettings.{Ambiente}.json` | Vira `search_path`; um schema por ambiente |
| `Database:Username` | `appsettings.{Ambiente}.json` | |
| `Database:Password` | dev: no arquivo · produção: `Database__Password` | Veja "Senhas" abaixo |
| `Database:SslMode` | `appsettings.{Ambiente}.json` | Modo permissivo em dev, obrigatório em produção |
| `Database:MaxPoolSize` | base | Padrão {{VALOR_MAX_POOL_SIZE}} |
| `Database:CommandTimeoutSeconds` | base | Padrão {{VALOR_TIMEOUT_SEGUNDOS}} |
| `Database:IncluirDetalheDeErro` | por ambiente | `true` só em dev — inclui o **valor dos parâmetros** nas mensagens de erro |
| `Database:MigrarAoIniciar` | por ambiente | `false` em todo lugar compartilhado; veja [banco de dados](banco-de-dados.md#migrations) |
| `Autenticacao:Emissor`, `:Audiencia` | base | Identificam o token; precisam bater entre quem emite e quem valida |
| `Autenticacao:Segredo` | dev: no arquivo · produção: `Autenticacao__Segredo` | Chave de assinatura, mínimo 32 caracteres. **Quem tem o segredo forja qualquer token** |
| `Autenticacao:MinutosDoTokenDeAcesso` | base | Padrão {{VALOR_MINUTOS_TOKEN_ACESSO}} — é também a janela em que uma inativação de usuário ainda não fez efeito |
| `Autenticacao:HorasDoTokenDeRenovacao` | base | Padrão {{VALOR_HORAS_TOKEN_RENOVACAO}} |

## Configuração incompleta derruba a aplicação

As opções obrigatórias são validadas no início (`ValidateOnStart` ou equivalente). Faltando
qualquer campo obrigatório, a aplicação **não sobe** e diz exatamente o que falta:

```
Database:Host não configurado.
Senha do banco não configurada. Em desenvolvimento use
'dotnet user-secrets set "Database:Password" "..."'; nos demais ambientes defina a
variável de ambiente Database__Password.
```

É proposital. Subir apontando para o banco errado é pior do que não subir.

As ferramentas de linha de comando de migration usam exatamente a mesma configuração da
aplicação — um caminho só, sem divergência entre o que roda e o que migra. Em troca, **os
comandos de migration exigem a configuração completa**, mesmo os que nem chegam a conectar
no banco.

## Senhas

**Desenvolvimento:** a senha está em `appsettings.Development.json`, por decisão do time, para
não exigir configuração manual em cada máquina. É banco de desenvolvimento e o repositório é
privado.

**Produção: a senha nunca entra em arquivo.** Ela vem de uma variável de ambiente no
servidor ou do cofre de segredos. O mesmo vale para qualquer token, chave de API ou
certificado que venha a existir.

Se precisar de uma senha só sua, sem tocar na configuração compartilhada:

```bash
dotnet user-secrets --project src/{{PREFIXO_NAMESPACE}}.Api set "Database:Password" "<senha>"
```

User Secrets tem precedência sobre o `appsettings` — o que também significa que, se você
deixar um secret antigo lá, trocar a senha no arquivo não terá efeito na sua máquina.

## Apontando para um banco seu

Crie `src/{{PREFIXO_NAMESPACE}}.Api/appsettings.Local.json` (ignorado pelo git):

```json
{
  "Database": {
    "Host": "localhost",
    "Name": "{{NOME_BANCO_LOCAL}}",
    "Schema": "{{NOME_BANCO_LOCAL}}",
    "Username": "postgres",
    "MigrarAoIniciar": true
  }
}
```

`MigrarAoIniciar: true` só faz sentido aqui, num banco que é só seu.

## Ambientes

O ambiente vem da variável padrão da plataforma (ex.: `ASPNETCORE_ENVIRONMENT`). Em
desenvolvimento a aplicação expõe Swagger UI e o documento OpenAPI; fora dele, não — e liga
redirecionamento HTTPS.

## Leia também

- [Banco de dados](banco-de-dados.md) — schema, migrations e carga de dados
- [API](api.md) — o que fica exposto em cada ambiente

## Borda: quem pode dizer de onde veio a requisição

<!-- guia: esta seção só se aplica quando a API roda atrás de proxy reverso e depende de
X-Forwarded-For para IP de auditoria/rate limit. Apague se não for o caso. -->

`Borda:ProxiesConfiaveis` recebe os endereços ou faixas CIDR dos proxies reversos à frente da
API — e somente eles. **Fechado por padrão:** sem nada declarado, o `X-Forwarded-For` é
ignorado e vale o endereço da conexão.

Fora de desenvolvimento a aplicação **não sobe** com esta lista vazia, nem com
`Cors:OrigensPermitidas` vazio. É deliberado: os dois falham de formas difíceis de ligar à
causa — IP forjável na auditoria, e conexões em tempo real recusadas pelo navegador sem
explicação.

O proxy declarado precisa **sobrescrever** o cabeçalho recebido do cliente, não acrescentar a
ele.

<!--
Como adaptar este template a um novo projeto (apague este bloco):
1. Substitua os placeholders com os valores/nomes reais das chaves de
   configuração do projeto.
2. Reescreva a tabela de "Chaves" com o inventário completo — é a primeira
   coisa que alguém consulta ao configurar uma máquina nova.
3. Se o projeto não roda atrás de proxy reverso, apague a seção "Borda".
-->
