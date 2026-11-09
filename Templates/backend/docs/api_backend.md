<!--
Template reutilizável. Copie para `docs/api.md` no repositório de backend,
substitua os {{PLACEHOLDERS}} e apague este comentário e a seção "Como
adaptar" ao final. Usa os mesmos placeholders dos demais arquivos de docs/
deste template.

Placeholders adicionais deste arquivo:
  {{RECURSO}}            nome de um recurso/entidade de domínio genérico, no plural da URL (ex.: grupos)
  {{RECURSO_SINGULAR}}   mesmo recurso, singular                                          (ex.: grupo)
  {{CAMPO_CONTEXTO}}     o que identifica "em nome de quem" a requisição atua              (ex.: vínculo, tenant, organização)

Este documento descreve os padrões de API que valeram para o sistema de
origem (autenticação por JWT + refresh token rotativo, RFC 9457 para erros,
paginação por página/tamanho). Mantenha os padrões que fizerem sentido para
o novo projeto e apague os que não se aplicam — não force um padrão de
autenticação ou paginação diferente do que o novo projeto realmente usa.
-->

# API

{{FRAMEWORK_BACKEND}}. O documento OpenAPI é gerado nativamente pelo framework; a interface é o Swagger UI, servido apenas em desenvolvimento.

| | |
| --- | --- |
| Swagger UI | `/swagger` — só em Development |
| Documento OpenAPI | `/openapi/v1.json` — só em Development |
| Health check | `/health` — em todos os ambientes |

## Autenticação

`POST /auth/login` devolve um par de tokens. Envie o de acesso em
`Authorization: Bearer <token>`.

<!-- guia: se o sistema não tem múltiplos contextos por usuário (ex.: um usuário só
pertence a uma organização/unidade), simplifique este bloco removendo a ramificação de
"vários contextos". -->

O token carrega o **{{CAMPO_CONTEXTO}} ativo** de quem está autenticado. Quem tem mais de um
{{CAMPO_CONTEXTO}} escolhe no login:

```
POST /auth/login  { email, senha }
  └─ um {{CAMPO_CONTEXTO}}      → 200 { situacao: "Autenticado", tokenDeAcesso, tokenDeRenovacao, contexto }
  └─ vários {{CAMPO_CONTEXTO}}s → 200 { situacao: "ContextoObrigatorio", contextos: [...] }
                            repita informando o {{CAMPO_CONTEXTO}} escolhido
```

`ContextoObrigatorio` é HTTP 200 de propósito: a credencial foi aceita, só falta escolher
o contexto. Erro de credencial é 401.

| Rota | O que faz |
| --- | --- |
| `POST /auth/login` | Abre a sessão |
| `POST /auth/refresh` | Rotaciona os tokens |
| `POST /auth/logout` | Revoga a sessão inteira |
| `GET /auth/me` | Identidade e contexto atuais |

### O que a sessão garante

**Rotação.** Cada renovação revoga o token usado e emite outro. O valor anterior morre no
mesmo instante — guarde sempre o último.

**Detecção de reúso.** Se um token já revogado for apresentado, **toda a família de tokens
daquela sessão cai**, inclusive a que está em uso. É a resposta a um indício de vazamento:
perder a sessão é melhor do que mantê-la sequestrada. Na prática, o usuário legítimo é
deslogado junto — e isso é o comportamento desejado.

> Se o sistema tiver mais de uma instância de API e precisar de tolerância a corrida entre
> requisições simultâneas de renovação, considere uma janela curta de carência (segundos) em
> que o token revogado pela rotação — e só pela rotação — ainda é aceito. Revogação por
> logout ou inativação não deve ganhar essa carência.

**Segredo não recuperável.** O token de renovação é aleatório e vai para o banco como hash
(ex.: SHA-256). Quem tiver acesso de leitura ao banco não consegue se passar por ninguém.

**Senha com hash forte e versionado**, de forma que, quando o custo do algoritmo subir, o
hash antigo possa ser re-derivado no próximo login, sem pedir troca de senha.

## Cadastro com aprovação

<!-- guia: esta seção só se aplica quando o sistema tem auto-cadastro que precisa de
aprovação humana antes de virar conta ativa. Apague se o cadastro for direto (sem
aprovação) ou administrado só por um admin. -->

A pessoa não se cadastra sozinha e entra: ela **pede acesso**, e um responsável decide.

```
gestor              POST /cadastros/convites        → código, válido por um período
  │                 (repassa o link a quem vai entrar)
  ▼
candidato           GET  /auth/register/{codigo}    → mostra o contexto do convite no formulário
                    POST /auth/register             → 202, pedido Pendente
  │
  ▼
gestor              GET  /cadastros/pendentes
                    POST /cadastros/{id}/aprovar    → cria usuário e credencial
                    POST /cadastros/{id}/rejeitar   → registra o motivo
  │
  ▼
candidato           POST /auth/login                → entra normalmente
```

**O usuário só existe a partir da aprovação.** Antes disso o pedido guarda os dados e o hash
da senha. Pedido recusado não deixa conta órfã nem reserva o e-mail — e a pessoa pode tentar
de novo, porque o índice de unicidade só vale para pedidos pendentes.

### O cadastro não revela quem já tem conta

Se o formulário de cadastro confere unicidade de e-mail, documento ou matrícula, **os
diferentes conflitos respondem com a mesma mensagem e o mesmo status**, e todas as
conferências rodam sempre — parar na primeira faria o tempo de resposta (ou a ordem dos
erros) dizer qual campo colidiu. O motivo real vai para a trilha de auditoria, não para a
resposta ao chamador anônimo.

## Padrão de recurso: cadastro com inativação em vez de exclusão

<!-- guia: use este esqueleto para qualquer recurso de catálogo/cadastro que não deve
sumir do histórico quando "removido". Duplique a seção por recurso real do projeto. -->

```
GET    /{{RECURSO}}                      → paginado; filtros por query string
GET    /{{RECURSO}}?incluirInativos=true → administração e leitura histórica
GET    /{{RECURSO}}/{id}                 → detalhe, ativo ou inativo
POST   /{{RECURSO}}                      → 201
PUT    /{{RECURSO}}/{id}                 → campos editáveis, incluindo situação (ativo)
DELETE /{{RECURSO}}/{id}                 → 204, ou 409 se houver dependente vinculado
```

| Situação | O que fazer | O que acontece |
| --- | --- | --- |
| {{RECURSO_SINGULAR}} em uso, não deve mais ser escolhido | `PUT` com `ativo: false` | Some dos formulários de criação; quem já referencia continua resolvendo o nome |
| {{RECURSO_SINGULAR}} criado por engano, nunca usado | `DELETE` | Removido de vez |
| {{RECURSO_SINGULAR}} com dependente vinculado | `DELETE` devolve **409** | Apagar deixaria o dependente sem classificação e quebraria o histórico |

A listagem esconde inativos por padrão — `?incluirInativos=true` traz tudo, para telas de
administração que precisam mostrar e reativar o que foi inativado.

### Unicidade que ignora caixa e espaço

Quando um campo textual precisa ser único "para humanos" (ex.: nome de categoria), normalize
antes de comparar (minúsculas, sem espaço nas pontas) e persista a forma normalizada ao lado
da grafia exibida, com índice único na forma normalizada — assim a regra vale mesmo sob
requisições concorrentes.

## Padrão de importação em massa

<!-- guia: use quando o projeto tem carga de dados por planilha/CSV. Apague se não houver
esse caso. -->

```
POST /{{RECURSO}}/importacoes/pre-visualizar   → multipart/form-data; lê e valida, não grava nada
POST /{{RECURSO}}/importacoes                  → mesmo contrato; grava as linhas aceitas
```

Os dois endpoints devolvem o mesmo formato de relatório:

```json
{
  "linhasLidas": 120,
  "linhasAceitas": 114,
  "linhasRejeitadas": 6,
  "rejeicoes": [ { "numeroDaLinha": 8, "motivo": "..." } ],
  "persistido": false
}
```

As duas fases rodam **exatamente a mesma validação**, sem estado de sessão entre elas — o
cliente reenvia o arquivo na confirmação. "Tudo ou nada" vale para o conjunto aceito, não
para o arquivo inteiro: uma linha ruim não derruba as boas.

## Paginação

`pagina` (1-based, padrão 1), `tamanhoDaPagina` (padrão {{PAGINACAO_PADRAO}}, teto
{{PAGINACAO_TETO}} — valores fora da faixa são normalizados, não rejeitados), resposta em
`{ dados, total, pagina, tamanhoDaPagina }`. Os dois parâmetros têm valor padrão no
endpoint — omitir a query string devolve a primeira página, não 400.

**Toda listagem paginada ordena por campo + `id`.** Um campo de ordenação que não é único
sozinho (ex.: nome) precisa de desempate por `id` — sem isso o banco não garante ordem
estável entre duas execuções da mesma consulta, e a mesma linha pode aparecer em duas
páginas enquanto outra some.

## A regra do OpenAPI

**Feature só está concluída com a documentação sincronizada.** Alterou endpoint, rota,
request, response, DTO, status code, validação, paginação, filtro ou autenticação? A
documentação muda no mesmo commit.

A documentação descreve **comportamento**, não repete o nome do método:

```
❌  Gets user.
✅  Obtém os dados detalhados de um usuário pelo identificador informado.
    Retorna 404 quando o usuário não existe.
```

Documente parâmetros, obrigatoriedade, validações, exemplos e **todos** os status codes que
a implementação realmente produz — não os que seriam bonitos.

## Contrato de erro

Erros seguem RFC 9457 (`application/problem+json`), com identificador de correlação para
rastreamento:

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.21",
  "title": "Regra de negócio violada",
  "status": 422,
  "detail": "campo é obrigatório.",
  "instance": "/{{RECURSO}}",
  "traceId": "00-8f3c...-01"
}
```

O tratamento é centralizado — middleware/handler global por tipo de erro. **Nunca**
`try/catch` espalhado por endpoint devolvendo o erro cru.

| Situação | Status |
| --- | --- |
| Violação de invariante de domínio (`{{EXCECAO_REGRA_DE_NEGOCIO}}`) | **422** |
| Entrada malformada, JSON inválido, tipo errado | 400 |
| Recurso inexistente | 404 |
| Conflito de estado (duplicidade, concorrência) | 409 |
| Dependência indisponível | 503 |

Erro de negócio nunca volta como `200 OK`. E resposta de erro nunca expõe stack trace,
connection string, credencial ou detalhe de infraestrutura.

## Status codes

Use o código com o significado correto. `201 Created` com `Location` ao criar, `204 No
Content` ao deletar, `200 OK` com corpo ao consultar. Os códigos documentados no OpenAPI
precisam refletir exatamente os que a implementação produz.

## DTOs

Entidade de domínio e entidade do ORM **não** são expostas na API. Todo endpoint recebe e
devolve DTO próprio. Isso mantém o contrato público sob controle, evita vazar campo interno
sem querer e permite reduzir payload sem mexer no domínio.

## Endpoints leves

O endpoint recebe a requisição, delega ao caso de uso, mapeia o resultado e devolve HTTP.
Regra de negócio dentro de endpoint é regra que não dá para testar sem subir a aplicação.

## `/health`

Verifica as dependências registradas (banco, filas, serviços externos). Devolve **200**
quando tudo está saudável e **503** quando alguma dependência está indisponível — quem
consome isso costuma ser um health probe de orquestrador, que decide pelo status code.

```json
{
  "status": "Healthy",
  "duracaoMs": 14.53,
  "dependencias": [{ "nome": "banco", "status": "Healthy", "descricao": null }]
}
```

Não exige autenticação e nunca expõe connection string nem credencial.

## Leia também

- [Arquitetura](arquitetura.md) — onde a lógica mora, se não é no endpoint
- [Configuração](configuracao.md) — o que fica exposto em cada ambiente

<!--
Como adaptar este template a um novo projeto (apague este bloco):
1. Substitua os placeholders. `{{RECURSO}}` pode se repetir — duplique a
   seção "Padrão de recurso" uma vez por recurso real que segue esse padrão.
2. Apague as seções que não se aplicam (cadastro com aprovação, importação
   em massa) em vez de deixá-las com placeholder sem preencher.
3. Se a autenticação não for JWT + refresh token, reescreva a seção
   "Autenticação" do zero com o mecanismo real — não force o vocabulário
   daqui num esquema diferente (ex.: OAuth de terceiros, API key).
4. Liste os endpoints reais do projeto à medida que forem sendo criados —
   este documento deve refletir o que existe, não o que está planejado.
-->
