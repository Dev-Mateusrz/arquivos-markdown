<!--
Template reutilizável. Apesar do nome do arquivo (mantido para acompanhar a
convenção deste projeto de templates — ver nota abaixo), o conteúdo é um
CLAUDE.md: copie para `CLAUDE.md` na raiz do repositório de FRONTEND,
substitua os {{PLACEHOLDERS}} e apague este comentário e a seção "Como
adaptar" ao final.

Nota sobre o nome do arquivo: no material de origem, este documento existe
como par de `readme-backend.md`, mas seu conteúdo real é o CLAUDE.md
específico do frontend (não um README). Ao adaptar para um projeto novo,
confirme se você quer replicar essa nomenclatura ou salvar diretamente como
`CLAUDE.md` — o conteúdo é o mesmo de qualquer forma.

Este arquivo assume Next.js (App Router) + React + TypeScript, e complementa
o CLAUDE.md geral deste docs-template (regras de aprovação, idioma, modelo de
issue) com o que é específico do frontend: stack, convenções de UI e
prioridades de engenharia do lado do cliente. Se o novo projeto usa outra
stack de frontend (Vue, Angular, mobile nativo), mantenha a estrutura das
seções e troque os detalhes técnicos.
-->

# CLAUDE.md — {{REPO_FRONTEND}}

Este arquivo é lido automaticamente pelo Claude Code no início de cada sessão neste
repositório. Ele reúne, num só lugar, o que os demais `.md` do projeto já estabelecem —
[`AGENTS.md`](AGENTS.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), [`README.md`](README.md) —
e acrescenta como o Claude deve operar aqui especificamente. **Nada abaixo é sugestão: são as
instruções vigentes do projeto, com prioridade sobre qualquer comportamento padrão.** Releia
este arquivo sempre que a sessão for longa o bastante para o contexto inicial ter ficado
distante.

@AGENTS.md
@CONTRIBUTING.md
@README.md

<!-- guia: se o repositório ainda não tem um AGENTS.md próprio de frontend (com convenções
de engenharia equivalentes ao do backend), diga isso explicitamente, como no exemplo abaixo,
e aponte onde as convenções vivem enquanto isso. -->

> `AGENTS.md` ainda não tem um documento de regras de engenharia equivalente ao do backend.
> Até que exista, as convenções de frontend vivem nas seções "Stack e convenções" abaixo e no
> `README.md`.

---

## Regra crítica: aprovação obrigatória antes de ações externas

O Claude **nunca** executa, sem aprovação explícita do usuário, nenhuma das ações abaixo:

- `git push`
- Abrir ou publicar um Pull Request
- Criar, editar ou comentar uma issue no rastreador (**{{CHAVE_PROJETO_TRACKER}}**, chave
  `{{PREFIXO_ISSUE_MAIUSCULO}}`, em `{{DOMINIO_TRACKER}}`)
- Qualquer ação que publique, apague ou altere algo visível a terceiros

Antes de qualquer uma dessas ações:

1. Mostre exatamente o que pretende fazer (texto do commit, conteúdo do PR, conteúdo da issue).
2. Aguarde confirmação explícita do usuário ("pode prosseguir", "aprovado").
3. Só então execute.

Isso vale **mesmo que o pedido pareça autorizar implicitamente** ("implementa e abre o PR") —
a aprovação do conteúdo gerado é sempre necessária antes do efeito externo. Criar branch local
e commitar localmente (sem push) pode acontecer sem essa pausa: são ações reversíveis e não
visíveis a terceiros.

## Idioma

Commits, nomes de branch (parte descritiva), títulos e descrições de PR, e títulos e
descrições de issues: sempre em **{{IDIOMA_PADRAO}}**. Nomes de componente, hook e arquivo
seguem o que já está em `src/` — {{CONVENCAO_IDIOMA_CODIGO}}.

---

## O que é o {{NOME_DO_SISTEMA}}, em três frases

{{OBJETIVO_DO_SISTEMA_TRES_FRASES}} Este repositório é a interface: {{TELAS_PRINCIPAIS}} —
ver [`README.md`](README.md) para o detalhe de cada tela. O backend (`{{REPO_BACKEND}}`) segue
{{DESCRICAO_MOTOR_DE_ESTADOS_OU_REGRA_CENTRAL}}; ao construir uma tela nova, confira o
vocabulário e as regras de negócio na documentação funcional antes de inventar um termo ou um
estado que já existe com outro nome.

## Stack e convenções

Next.js {{VERSAO_NEXT}} (App Router) · React {{VERSAO_REACT}} · TypeScript · {{FRAMEWORK_CSS}} · {{LIB_ANIMACAO}} · {{GERENCIADOR_PACOTES}} (o
`{{CMD_INSTALL_FRONTEND}}` já ativa os hooks de commit via `scripts/setup-hooks.mjs` — não precisa rodar
`git config core.hooksPath` manualmente aqui, ao contrário do backend).

- **Fidelidade ao design.** {{DESCRICAO_FLUXO_DESIGN_PARA_CODIGO}}
- **Responsividade.** {{DESCRICAO_ESTRATEGIA_RESPONSIVA}}
- **Tema claro/escuro** {{DESCRICAO_TEMA}}
- **Estrutura:** `src/app/` (rotas), `src/components/` (UI), `src/lib/` (utilitários
  transversais). Siga o que já existe em vez de introduzir uma pasta nova sem necessidade.
- **Reaproveite antes de criar.** {{DESCRICAO_COMPONENTES_REUTILIZAVEIS}} — não duplique.
- **Não superengenharie.** Mesmo princípio do backend: sem abstração sem consumidor, sem
  camada extra "para o futuro".

## Branches

- `{{BRANCH_PRODUCAO}}`: produção. Protegida — nunca commitar nem dar push direto.
- `{{BRANCH_DESENVOLVIMENTO}}`: desenvolvimento. Base para `feat/`, `fix/`, `chore/`, `docs/`, `refactor/`.
- `hotfix/`: sai de `{{BRANCH_PRODUCAO}}` (não de `{{BRANCH_DESENVOLVIMENTO}}`), para bug já em produção. Depois do merge em
  `{{BRANCH_PRODUCAO}}`, abre-se **também** um PR de `{{BRANCH_PRODUCAO}}` para `{{BRANCH_DESENVOLVIMENTO}}`.

Nome da branch: `<tipo>/{{PREFIXO_ISSUE}}-<numero>-<descricao-curta-em-kebab-case>` — ex.:
`feat/{{PREFIXO_ISSUE}}-36-nome-da-tela`. Tipos: `feat`, `fix`, `hotfix`, `chore`,
`docs`, `refactor`. Push direto em `{{BRANCH_PRODUCAO}}`/`{{BRANCH_DESENVOLVIMENTO}}` é bloqueado pelo hook `pre-push` — não
tente contornar (nem com `--no-verify`).

## Commits

Formato obrigatório, cobrado pelo hook `commit-msg`: `<tipo>({{PREFIXO_ISSUE_MAIUSCULO}}-000): descrição no
imperativo`. Não digite o número manualmente — se a branch é `feat/{{PREFIXO_ISSUE}}-36-...`, o hook
`prepare-commit-msg` injeta o ID sozinho. Tipos aceitos pelo hook: `feat`, `fix`, `hotfix`,
`chore`, `docs`, `refactor`, `test`, `style`, `perf`, `build`, `ci`, `revert`. Um commit, um
assunto. Revise sempre `git status`/`git diff` antes — **nunca `git add .` sem revisar**.

O que acontece no rastreador a cada push/merge, e o que fazer quando um card "não anda" sozinho:
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## Issues no rastreador (projeto {{CHAVE_PROJETO_TRACKER}}, chave `{{PREFIXO_ISSUE_MAIUSCULO}}`)

<!-- guia: se o board já tem épicos definidos, diga a faixa de números aqui — evita que uma
issue nova duplique um épico existente. -->

**Antes de propor uma issue nova, confira se ela não é uma subtarefa de um épico já
existente.**

Ao criar uma issue:

- **Tipo:** `Tarefa` (padrão) · `Subtarefa` (parte de uma tarefa maior — vincule ao pai) ·
  `Epic` (só para iniciativa nova) · `Incidente` (bug em produção).
- **Prioridade:** `Highest` (mudança estrutural/alto risco) · `High` (relevante, escopo
  definido) · `Medium` (padrão, complexidade moderada) · `Low` (pequena, baixo risco).
- **Responsável:** sempre **{{RESPONSAVEL_PADRAO}}**. Se a busca no rastreador não
  encontrar essa conta, crie a issue **sem responsável** e avise o motivo — nunca atribua a
  outra pessoa nem adivinhe.
- **Categorias (labels):** reaproveite o que já existe — a área do épico correspondente e,
  quando a tarefa tiver as duas pontas, o rótulo `{{ROTULO_FULLSTACK}}`
  ([`CONTRIBUTING.md`](CONTRIBUTING.md) — trava o card até frontend e backend chegarem na
  mesma etapa).
- **Data limite:** pergunte ao usuário, **toda vez**, antes de criar a issue — nunca defina
  por conta própria.

Estrutura da descrição:

```markdown
## Contexto
[Por que essa tarefa existe]

## Objetivo
[O que a tarefa busca alcançar, de forma direta]

## Área afetada
- Front-end: [sim/não — o que muda]
- Back-end: [sim/não — o que muda]

## Escopo sugerido
- [item 1]

## Critérios de aceite
- [condição verificável]

## Testes esperados
- [o que validar]

## Observações técnicas
[Dependências, tela/design de origem, pontos em aberto]
```

## Checks obrigatórios

| Mudança | Check mínimo |
| --- | --- |
| Qualquer código | `{{CMD_BUILD_FRONTEND}}` |
| Lint | `{{CMD_LINT_FRONTEND}}` — resolva o que estiver no escopo da mudança |
| Comportamento novo de UI | {{ESTRATEGIA_TESTE_UI}} |
| Mudança visual | Print ou vídeo no PR (ver "Regra adicional" em [CONTRIBUTING.md](CONTRIBUTING.md)) |

Mudança que toca mais de uma linha da tabela aplica **todos** os checks correspondentes.

## Abrindo Pull Request

Fluxo completo em [`CONTRIBUTING.md`](CONTRIBUTING.md): base é `{{BRANCH_DESENVOLVIMENTO}}` na regra geral, ou
`{{BRANCH_PRODUCAO}}` só em hotfix (com PR de volta para `{{BRANCH_DESENVOLVIMENTO}}` depois do merge). Título igual ao commit:
`feat({{PREFIXO_ISSUE_MAIUSCULO}}-36): nome da tela`. O repositório já tem um template de PR em
[`.github/pull_request_template.md`](.github/pull_request_template.md) — preencha-o por
completo, principalmente o card (`{{PREFIXO_ISSUE_MAIUSCULO}}-000`) e o item de dados sensíveis/PII do checklist.

## Prioridades de engenharia

Correção · Segurança (validação de entrada, sem XSS) · Acessibilidade · Fidelidade ao design ·
Performance percebida (evitar layout shift e animação travada) · Manutenibilidade ·
Simplicidade. Nunca sacrifique correção ou acessibilidade por proximidade pixel-perfect do
design.

<!--
Como adaptar este template a um novo projeto (apague este bloco):
1. Substitua os placeholders — vários já são definidos no CLAUDE.md geral
   deste docs-template (raiz); mantenha os valores idênticos entre os dois
   arquivos.
2. Ajuste "Stack e convenções" à stack de frontend real do projeto.
3. Se o projeto tiver um único repositório (fullstack), avalie se este
   arquivo deveria ser fundido com o CLAUDE.md geral em vez de existir à
   parte.
-->
