> **Instrução para a IA (Meta-Prompt):** Este documento define o **padrão de engenharia** para escrever arquivos modulares dentro de `.agents/`. Ao criar qualquer arquivo de regra (seja de Git, Pull Request, Jira ou Checks), **não escreva textos explicativos ou teóricos**; converta os requisitos do projeto em um algoritmo determinístico seguindo a estrutura: `Gatilho -> Proibições -> Formato/Template -> Exemplos Few-Shot (Certo vs. Errado) -> Fluxo Passo a Passo`. Adapte os nomes de branches e prefixos de tickets à realidade do repositório atual.


Atualizado: 26/11/2026

Esse modelo serve para montar a estrutura dos arquivos de regras-modulares-agents para terem uma melhor eficiência, precisão e sem desperdício de contexto. Eles devem ser escritos como um algoritmo determinístico (regras SE -> ENTÃO), proibições explícitas e exemplos concretos) em vez de prosa explicativa.

Modelos de linguagem respondem muito melhor a restrições negativas claras ("NUNCA faça X") combinadas com templates exatos e fluxos passo a passo validados por comandos.

## Boas Práticas para os Arquivos de Regras

Vamos usar o exemplo de boas práticas para um arquivo de regras de Commit e Branch: .agents/padrao-commit-branch.md

- Estrutura de Contrato (Gatilho -> Restrições -> Formato -> Fluxo): Comece dizendo exatamente quando o arquivo se aplica, liste o que é proibido antes do que é permitido, dê o molde exato e encerre com o checklist de execução.

- Exemplos Few-Shot (Certo vs. Errado): Incluir 2 exemplos válidos e 2 inválidos reduz erros de formatação da IA em mais de 80%, especialmente em regex de branches e Conventional Commits.

- Comandos Explícitos e Seguros: Como agentes de IA tendem a usar git add . por padrão (arriscando commitar .env ou arquivos temporários), a regra deve instruir explicitamente a listar os arquivos via git status e adicioná-los individualmente.

- Sem Ambiguidade de Branch Base: Como você tem master no front-end e main no back-end, o arquivo já deve resolver essa diferença na primeira linha para a IA não precisar adivinhar.

## Modelo Otimizado

Exemplo para: .agents/padrao-commit-branch.md

```
# Padrão de Branches e Commits

> **Gatilho:** Leia e aplique este documento obrigatoriamente antes de criar qualquer branch, preparar arquivos (`git add`) ou executar `git commit`.

---

## 1. Mapa de Branches do Projeto

* **Branch de Produção:**
  * `frontend-smsagenda`: `master`
  * `backend-smsagenda`: `main`
* **Branch de Desenvolvimento (Base padrão):** `develop`
* **Proibição Absoluta:** Nunca realize commits ou pushes diretamente em `master`, `main` ou `develop`.

---

## 2. Nomenclatura de Branches

Formato obrigatório (tudo em minúsculo, sem acentos, separado por hífen):

```text
<tipo>/sa-<id-jira>-<descricao-curta-em-kebab-case>
````markdown

### Tabela de Tipos Permitidos

| Tipo | Quando Usar | Branch de Origem | Branch de Destino (PR) |
| :--- | :--- | :--- | :--- |
| `feature` | Nova funcionalidade | `develop` | `develop` |
| `bugfix` | Correção de bug encontrado em desenvolvimento/homologação | `develop` | `develop` |
| `fix` | Correção pontual/ajuste técnico em desenvolvimento | `develop` | `develop` |
| `hotfix` | Correção crítica urgente em produção | `master` ou `main` | `master`/`main` **E** `develop` |
| `chore` | Manutenção, dependências, configs | `develop` | `develop` |
| `refactor` | Refatoração sem mudança de comportamento | `develop` | `develop` |
| `docs` | Documentação | `develop` | `develop` |

### Exemplos de Branches

* **Correto:** `feature/sa-142-filtro-agendamentos-por-unidade`
* **Correto:** `hotfix/sa-199-erro-autenticacao-token-expirado`
* **Incorreto:** `feature/SA-142_FiltroAgendamentos` (maiúsculas e underline proibidos)
* **Incorreto:** `sa-142-ajuste-tela` (falta o `<tipo>/` antes do ID)

---

## 3. Fluxo de Criação de Branch (Passo a Passo)

1. Verifique se há alterações não commitadas com `git status`.
2. Atualize a branch de origem antes de ramificar:
   * Fluxo normal: `git checkout develop && git pull origin develop`
   * Fluxo `hotfix`: `git checkout <master|main> && git pull origin <master|main>`
3. Crie a nova branch a partir dela: `git checkout -b <tipo>/sa-<id>-<descricao>`.
4. **Regra de Hotfix:** Ao finalizar um `hotfix`, informe obrigatoriamente ao usuário que serão necessários **dois Pull Requests** (um para produção `master`/`main` e outro para `develop`).

---

## 4. Padrão de Mensagens de Commit (Conventional Commits)

Todas as mensagens devem ser escritas em **português do Brasil**, no modo imperativo, com no máximo **72 caracteres** na linha de assunto.

### Formato

```text
<tipo>(<escopo-opcional>): <descrição curta no imperativo>

````markdown
* **Tipos permitidos:** `feat`, `fix`, `refactor`, `style`, `test`, `docs`, `chore`, `perf`, `ci`, `build`.
* **Regra de Granularidade:** Faça commits atômicos (um propósito lógico por commit).

### Exemplos de Commits

* **Correto:** `feat(agenda): adiciona filtro por status de confirmacao`
* **Correto:** `fix(auth): corrige renovacao automatica de token jwt`
* **Incorreto:** `feat: adicionado filtro` (use imperativo: *adiciona*, não *adicionado*)
* **Incorreto:** `ajustes gerais` (sem tipo Conventional Commit)

---

## 5. Regras de Execução (`git add` e `git commit`)

* **Proibido `git add .` ou `git add -A`:** Sempre rode `git status` e adicione cada arquivo explicitamente pelo caminho (`git add caminho/do/arquivo`).
* **Verificação de Arquivos Sensíveis:** Nunca adicione `.env`, `.env.local`, chaves, certificados ou arquivos temporários.
* **Proibido Co-autoria Automática:** Nunca inclua `Co-Authored-By:` ou assinaturas de IA na mensagem de commit.
* **Permissão:** Commits locais são permitidos sem pedir confirmação; `git push` exige aprovação explícita do usuário.

```
