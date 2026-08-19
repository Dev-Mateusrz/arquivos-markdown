# Como trabalhamos no {{NOME_DO_SISTEMA}}

> **Template reutilizável.** Copie este arquivo para `CONTRIBUTING.md` na raiz de cada repositório do projeto (backend e frontend usam o **mesmo arquivo**, com o mesmo conteúdo — é assim de propósito, ver nota no fim). Substitua os `{{PLACEHOLDERS}}`, apague os blocos `<!-- guia: ... -->` e a seção "Como adaptar" ao final.

## Placeholders deste template

| Placeholder | Significado | Exemplo |
|---|---|---|
| `{{NOME_DO_SISTEMA}}` | Nome do sistema | `GIPE` |
| `{{CHAVE_PROJETO_TRACKER}}` | Nome/chave do projeto no rastreador | `SMS-GIPE` |
| `{{PREFIXO_ISSUE_MAIUSCULO}}` | Prefixo do código da issue (maiúsculo) | `SG` |
| `{{PREFIXO_ISSUE}}` | Mesmo prefixo, em minúsculo — usado no nome da branch | `sg` |
| `{{BRANCH_PRODUCAO}}` | Branch de produção | `main` |
| `{{BRANCH_DESENVOLVIMENTO}}` | Branch base de desenvolvimento | `develop` |
| `{{COLUNA_EM_DESENVOLVIMENTO}}` | Coluna do board para push em branch de trabalho | `EM DESENVOLVIMENTO` |
| `{{COLUNA_EM_REVISAO}}` | Coluna do board para PR aprovado/mergeado na branch de desenvolvimento | `TESTES` |
| `{{COLUNA_CONCLUIDO}}` | Coluna do board para PR mergeado na branch de produção | `Itens concluídos` |
| `{{ROTULO_FULLSTACK}}` | Label usada para travar cards que têm as duas pontas (frontend + backend) | `fullstack` |
| `{{DOMINIO_TRACKER}}` | Domínio do rastreador (sem `/browse`) | `suaorg.atlassian.net` |
| `{{ORG_GITHUB}}` | Organização/usuário do GitHub que hospeda os repositórios | `SUBG-RioSaude` |
| `{{REPO_BACKEND}}` | Nome do repositório de backend | `backend-gipe` |
| `{{REPO_FRONTEND}}` | Nome do repositório de frontend | `frontend-gipe` |

<!-- guia: se o projeto for só backend ou só frontend, apague as referências ao repositório irmão e a seção 6 (cards fullstack) inteira. -->

---

## 1. O fluxo em uma linha

```
feat|fix|hotfix/{{PREFIXO_ISSUE_MAIUSCULO}}-000-descricao  ──PR──▶  {{BRANCH_DESENVOLVIMENTO}}  ──PR──▶  {{BRANCH_PRODUCAO}}
        {{COLUNA_EM_DESENVOLVIMENTO}}                                {{COLUNA_EM_REVISAO}}         {{COLUNA_CONCLUIDO}}
```

| O que você faz                                     | O que acontece no rastreador (`{{CHAVE_PROJETO_TRACKER}}` / `{{PREFIXO_ISSUE_MAIUSCULO}}`) |
| -------------------------------------------------- | --------------------------------------------- |
| `git push` numa branch `feat/`, `fix/`, `hotfix/`  | card vai para **{{COLUNA_EM_DESENVOLVIMENTO}}**          |
| PR **aprovado** mergeado na `{{BRANCH_DESENVOLVIMENTO}}`              | card vai para **{{COLUNA_EM_REVISAO}}**                      |
| PR mergeado na `{{BRANCH_PRODUCAO}}`                              | card vai para **{{COLUNA_CONCLUIDO}}**            |
| PR mergeado na `{{BRANCH_DESENVOLVIMENTO}}` **sem aprovação**         | card **não anda** e a automação comenta o motivo |
| card com rótulo `{{ROTULO_FULLSTACK}}`, só uma ponta mergeada | card **espera** a outra ponta (ver seção 6)   |

O que liga tudo é o **ID do card** (`{{PREFIXO_ISSUE_MAIUSCULO}}-42`). Ele precisa aparecer no nome da branch,
no título do PR ou na mensagem do commit — a automação procura nos três.

---

## 2. Setup (uma vez por máquina, em cada repositório)

```bash
git clone <url-do-repo>
cd <repo>
npm install          # se o repositório usa npm; ativa os hooks automaticamente
```

Se o repositório não usa npm (ou você prefere fazer na mão), ative os hooks assim:

```bash
git config core.hooksPath .githooks
```

Confira se pegou:

```bash
git config core.hooksPath
```

Tem que responder `.githooks`. Se não responder, os hooks não estão rodando e você vai
descobrir o erro só no CI.

<!-- guia: se o setup dos hooks difere entre backend e frontend (ex.: um usa npm install, outro exige o comando manual), diga explicitamente qual repositório faz o quê — foi o caso do projeto original. -->

---

## 3. Começando um card

Pegue o card no board, mova-o... **não**. Só crie a branch com o ID dentro:

```bash
git checkout {{BRANCH_DESENVOLVIMENTO}}
git pull
git checkout -b feat/{{PREFIXO_ISSUE}}-42-descricao-curta
```

Padrão do nome da branch:

```
<tipo>/{{PREFIXO_ISSUE}}-<numero>-<descricao-curta-em-kebab-case>
```

| Tipo      | Quando usar                                                          |
| --------- | -------------------------------------------------------------------- |
| `feat/`   | funcionalidade nova                                                   |
| `fix/`    | correção de bug encontrado em teste/desenvolvimento                   |
| `hotfix/` | correção urgente do que já está em produção (sai da `{{BRANCH_PRODUCAO}}`)           |
| `chore/`  | build, dependência, configuração — coisas que não mudam o produto     |
| `docs/`   | só documentação                                                       |
| `refactor/` | reorganização de código sem mudar comportamento                     |

---

## 4. Commitando

Formato obrigatório (o hook `commit-msg` recusa o que sair disso):

```
<tipo>({{PREFIXO_ISSUE_MAIUSCULO}}-000): descrição no imperativo
```

```bash
git commit -m "feat({{PREFIXO_ISSUE_MAIUSCULO}}-42): cadastra setores e centrais de resposta"
```

**Você não precisa digitar o `{{PREFIXO_ISSUE_MAIUSCULO}}-42`.** Se a branch se chama `feat/{{PREFIXO_ISSUE}}-42-...`, o hook
`prepare-commit-msg` injeta o ID sozinho — `git commit -m "feat: cadastra setores"`
vira `feat({{PREFIXO_ISSUE_MAIUSCULO}}-42): cadastra setores`. E `git commit` sem `-m` já abre o editor com
`feat({{PREFIXO_ISSUE_MAIUSCULO}}-42): ` escrito.

Regras que o hook cobra:

- tipo válido: `feat`, `fix`, `hotfix`, `chore`, `docs`, `refactor`, `test`, `style`, `perf`, `build`, `ci`, `revert`
- descrição com pelo menos 4 caracteres, no imperativo ("cadastra", não "cadastrado")
- primeira linha com no máximo 100 caracteres
- o ID do card em algum lugar da mensagem

Um commit, um assunto. Se a frase precisa de "e", provavelmente são dois commits.

---

## 5. Abrindo o PR

```bash
git push -u origin feat/{{PREFIXO_ISSUE}}-42-descricao-curta
```

Depois do push o git imprime um link `https://github.com/.../pull/new/...` — é só abrir.
Quem tiver o [GitHub CLI](https://cli.github.com) instalado pode usar `gh pr create --base {{BRANCH_DESENVOLVIMENTO}}`.

**Confira a branch de destino**: o padrão é `{{BRANCH_DESENVOLVIMENTO}}`. O GitHub às vezes sugere `{{BRANCH_PRODUCAO}}`,
e um PR para `{{BRANCH_PRODUCAO}}` marca o card como concluído sem ele ter passado por teste.

O título do PR segue o mesmo padrão do commit: `feat({{PREFIXO_ISSUE_MAIUSCULO}}-42): cadastro de setores`.

Daí em diante:

1. Alguém do time revisa e **aprova**.
2. Merge na `{{BRANCH_DESENVOLVIMENTO}}` → o card vai para **{{COLUNA_EM_REVISAO}}** automaticamente, com um comentário
   no rastreador dizendo quem aprovou.
3. Quando a release for pra produção, PR da `{{BRANCH_DESENVOLVIMENTO}}` para a `{{BRANCH_PRODUCAO}}` → os cards da
   release vão para **{{COLUNA_CONCLUIDO}}**.

Push direto na `{{BRANCH_DESENVOLVIMENTO}}` ou na `{{BRANCH_PRODUCAO}}` é bloqueado pelo hook `pre-push`. Isso é de
propósito: sem PR, não existe aprovação, e sem aprovação o card não anda.

---

## 6. Cards que precisam de frontend e backend

<!-- guia: apague esta seção inteira se o projeto tiver um único repositório (fullstack ou monorepo). -->

Um card como "Cadastro de setores" quase sempre tem as duas pontas. Se nada for feito, o
primeiro repositório a chegar na `{{BRANCH_PRODUCAO}}` marca o card como concluído — mesmo com a outra
metade pela metade.

Para esses casos, **coloque o rótulo `{{ROTULO_FULLSTACK}}` no card**, no rastreador. A partir daí:

- cada merge grava um selo no próprio card — `testes-backend`, `entregue-frontend`, …
- o card **só avança quando as duas pontas chegarem na mesma etapa**
- enquanto falta uma, a automação comenta no card exatamente quem está faltando
- se o card voltar para desenvolvimento (um `fix/` novo), os selos são apagados e o
  ciclo recomeça do zero

Card sem o rótulo anda normalmente, com um repositório só. Então a regra prática é:
**na dúvida, rotule** — o custo de rotular um card que era só de uma ponta é ele esperar
um merge que nunca vem (e aí você move na mão); o custo de esquecer é dar como entregue
o que não foi.

Se preferir dividir o trabalho em vez de travar, também funciona: dois cards (ou duas
sub-tarefas), um por camada, cada branch citando o seu. Aí nenhum rótulo é necessário.

---

## 7. Hotfix

Bug em produção sai da `{{BRANCH_PRODUCAO}}`, não da `{{BRANCH_DESENVOLVIMENTO}}`:

```bash
git checkout {{BRANCH_PRODUCAO}} && git pull
git checkout -b hotfix/{{PREFIXO_ISSUE}}-77-corrige-o-que-quebrou
# ... corrige, commita ...
git push -u origin hotfix/{{PREFIXO_ISSUE}}-77-corrige-o-que-quebrou
# abra o PR pelo link que o git imprime, com destino {{BRANCH_PRODUCAO}}
```

Depois do merge na `{{BRANCH_PRODUCAO}}`, **abra também um PR da `{{BRANCH_PRODUCAO}}` para a `{{BRANCH_DESENVOLVIMENTO}}`** (ou faça o
merge de volta), senão a correção some no próximo release.

---

## 8. Quando o card não anda

A automação sempre deixa rastro. Antes de mover na mão, olhe:

- **GitHub → aba Actions → workflow de sincronização com o rastreador**: o log diz exatamente quais
  cards encontrou e o que fez com cada um.
- **O card no rastreador**: a automação comenta cada movimento e também cada recusa.

Causas mais comuns:

| Sintoma no log                                          | Causa                                                          |
| ------------------------------------------------------- | --------------------------------------------------------------- |
| `Nenhum ID de card ({{PREFIXO_ISSUE_MAIUSCULO}}-000) encontrado`                 | branch, PR e commits sem o ID — coloque no título do PR         |
| `entrou na {{BRANCH_DESENVOLVIMENTO}} sem aprovação válida`                | mergearam sem review aprovado, ou há "changes requested" aberto |
| `não há transição para "{{COLUNA_EM_REVISAO}}"`                        | renomearam a coluna no board do rastreador                            |
| `Secret JIRA_API_TOKEN não configurado`                 | falta configurar os secrets do repositório (ver seção 9)  |
| `Card {{PREFIXO_ISSUE_MAIUSCULO}}-999 não existe no rastreador`                        | número do card errado na branch/commit                          |
| `é {{ROTULO_FULLSTACK}} e ainda falta frontend`                    | comportamento esperado — a outra ponta ainda não mergeou        |
| `Não consegui gravar os rótulos`                        | falta permissão de **Edit Issues** para a conta da automação    |
| `Não consegui autenticar`                               | `JIRA_USER_EMAIL` não é o e-mail da conta que gerou o token     |

Precisou mover um card na mão? **GitHub → Actions → workflow de sincronização →
Run workflow**, informe o card e o status. Fica registrado.

---

## 9. Configuração do repositório (quem administra)

### Primeiro push para o GitHub

O hook `pre-push` bloqueia `{{BRANCH_PRODUCAO}}` e `{{BRANCH_DESENVOLVIMENTO}}` — inclusive na primeira vez, quando as
branches ainda não existem no remoto. Só nesse momento, libere:

**PowerShell** (o terminal padrão do Windows):

```powershell
git remote add origin git@github.com:{{ORG_GITHUB}}/<repo>.git
$env:ALLOW_DIRECT_PUSH = '1'; git push -u origin {{BRANCH_PRODUCAO}} {{BRANCH_DESENVOLVIMENTO}}; Remove-Item Env:ALLOW_DIRECT_PUSH
```

**Git Bash / WSL / macOS:**

```bash
git remote add origin git@github.com:{{ORG_GITHUB}}/<repo>.git
ALLOW_DIRECT_PUSH=1 git push -u origin {{BRANCH_PRODUCAO}} {{BRANCH_DESENVOLVIMENTO}}
```

Depois disso, ninguém mais empurra nada direto nessas branches.

> `VARIAVEL=valor comando` só existe no bash. No PowerShell a variável de ambiente é
> definida antes, com `$env:`, e vale para o resto da sessão — por isso o
> `Remove-Item` no fim, para a proteção voltar a valer.

### Secrets — `Settings → Secrets and variables → Actions`

| Secret            | Valor                                                                          |
| ----------------- | ------------------------------------------------------------------------------ |
| `JIRA_BASE_URL`   | `https://{{DOMINIO_TRACKER}}`                                                 |
| `JIRA_USER_EMAIL` | e-mail da conta Atlassian usada pela automação                                 |
| `JIRA_API_TOKEN`  | token criado em `id.atlassian.com/manage-profile/security/api-tokens`          |

O `JIRA_USER_EMAIL` tem que ser **o e-mail da conta que gerou aquele token** — o par
e-mail + token é a credencial. É uma credencial única para o time inteiro: a automação
não age em nome de quem commitou, ela é um robô que move o card de qualquer pessoa. Não
existe configuração por desenvolvedor, e a atribuição do card nunca é alterada.

A conta precisa de duas permissões no projeto `{{PREFIXO_ISSUE_MAIUSCULO}}`:

- **Transition Issues** — mover o card entre as colunas
- **Edit Issues** — gravar os selos (`testes-backend`, `entregue-frontend`) usados pela
  trava dos cards `{{ROTULO_FULLSTACK}}`

Use uma conta de serviço se puder — assim o histórico dos cards não registra todos os
movimentos como se fossem de uma pessoa só. Lembre que no Jira Cloud cada conta consome
uma licença.

### Branch protection — `Settings → Rules → Rulesets`

Para `{{BRANCH_PRODUCAO}}` e `{{BRANCH_DESENVOLVIMENTO}}`:

- exigir Pull Request antes do merge
- exigir **pelo menos 1 aprovação**
- descartar aprovações antigas quando chegam commits novos
- bloquear push direto (o hook local ajuda, mas só a regra do servidor garante)

O hook `pre-push` protege quem esquece; a branch protection protege o repositório.

### Os arquivos da automação

| Arquivo                                | Papel                                                          |
| -------------------------------------- | -------------------------------------------------------------- |
| `.github/workflows/jira-pipeline.yml`  | dispara nos eventos de push e de PR mergeado; define o `REPO_ROLE` |
| `.github/scripts/jira-sync.mjs`        | acha os IDs, confere a aprovação, aplica a trava e a transição   |
| `.githooks/prepare-commit-msg`         | injeta o ID do card na mensagem                                 |
| `.githooks/commit-msg`                 | recusa commit fora do padrão                                    |
| `.githooks/pre-push`                   | bloqueia push direto em `{{BRANCH_PRODUCAO}}`/`{{BRANCH_DESENVOLVIMENTO}}`                        |
| `scripts/setup-hooks.*`                | aponta o git para `.githooks/` (uma variante por ecossistema, se necessário) |

Se o projeto tiver mais de um repositório (backend/frontend), **use exatamente os mesmos
arquivos nos dois**. Mudou em um, replique no outro.

---

## Como adaptar este template a um novo projeto

<!-- guia: apague esta seção inteira depois de preencher. -->

1. **Substitua os placeholders** da tabela do topo. `{{PREFIXO_ISSUE}}` é o prefixo em minúsculo — se `{{PREFIXO_ISSUE_MAIUSCULO}}` é `SG`, o valor é `sg`.
2. **Confirme os nomes reais das colunas do board** antes de preencher `{{COLUNA_EM_DESENVOLVIMENTO}}` etc. — copiar o nome errado faz a automação (ver `jira-pipeline-*.yml`) falhar silenciosamente.
3. **Se o projeto for um único repositório**, apague a seção 6 e toda menção a "a outra ponta".
4. **Se o rastreador não for Jira**, adapte a seção 9 (secrets, permissões) para o equivalente em Azure DevOps, Linear ou GitHub Issues — a lógica de "ID na branch move o card" é portável, os nomes dos campos não.
5. **Mantenha os dois arquivos (backend e frontend) idênticos.** É proposital: quem alterna entre repositórios não deveria reaprender o fluxo.
