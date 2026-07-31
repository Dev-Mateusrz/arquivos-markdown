# Convenções do Projeto — {{NOME_DO_SISTEMA}}

> **Para que serve:** definir as regras que o Claude (e qualquer humano) deve seguir neste repositório — branches, commits, PRs, issues e aprovação obrigatória antes de ações externas. É o arquivo que o agente relê antes de agir.
>
> **Template reutilizável.** Copie este arquivo para a raiz do repositório como `CLAUDE.md`, substitua todos os `{{PLACEHOLDERS}}` e remova as linhas marcadas com `<!-- guia: ... -->` e os blocos "Como adaptar" ao final.

## Placeholders deste template

| Placeholder | Significado | Exemplo |
|---|---|---|
| `{{NOME_DO_SISTEMA}}` | Nome do sistema/repositório | `SMSAgenda` |
| `{{CHAVE_PROJETO_TRACKER}}` | Chave do projeto no rastreador de issues | `SUBG-AGENDA` |
| `{{PREFIXO_ISSUE}}` | Prefixo da issue em minúsculo (usado em branch) | `sa` |
| `{{BRANCH_PRODUCAO}}` | Branch de produção | `master` ou `main` |
| `{{BRANCH_DESENVOLVIMENTO}}` | Branch base de desenvolvimento | `develop` |
| `{{RESPONSAVEL_PADRAO}}` | Pessoa a quem toda issue é atribuída | `Nome Sobrenome` |
| `{{IDIOMA_PADRAO}}` | Idioma de commits, branches, PRs e issues | `português do Brasil` |
| `{{CMD_BUILD_BACKEND}}` | Comando de build do backend | `dotnet build ...` |
| `{{CMD_TEST_BACKEND}}` | Comando de teste do backend | `dotnet test ...` |
| `{{CMD_BUILD_FRONTEND}}` | Comando de build do frontend | `pnpm build` |
| `{{CMD_LINT_FRONTEND}}` | Comando de lint do frontend | `pnpm lint` |

---

## Regra crítica: aprovação obrigatória antes de ações externas

O Claude **nunca** deve executar, sem aprovação explícita do usuário, nenhuma das ações abaixo:

- `git push`
- Abrir ou publicar um Pull Request
- Criar uma issue no rastreador ({{CHAVE_PROJETO_TRACKER}})
- Qualquer ação que publique, apague ou altere algo visível a terceiros

Antes de qualquer uma dessas ações, o Claude deve:

1. Mostrar exatamente o que pretende fazer (texto do commit, conteúdo do PR, conteúdo da issue).
2. Aguardar confirmação explícita do usuário (ex: "pode prosseguir", "aprovado").
3. Só então executar.

Isso vale **mesmo que o pedido inicial pareça autorizar implicitamente** (ex: "implementa e abre o PR") — a aprovação do conteúdo gerado é sempre necessária antes da ação ter efeito externo. Criar branch localmente e fazer commit local (sem push) pode acontecer sem essa pausa, já que são ações reversíveis e não visíveis a terceiros.

## Idioma

Commits, nomes de branch (na parte descritiva), títulos e descrições de PR, e títulos e descrições de issues devem ser sempre em **{{IDIOMA_PADRAO}}**.

<!-- guia: normalmente "português do Brasil". Em projetos com colaboradores internacionais, troque por "inglês" e ajuste os exemplos de commit abaixo. -->

## Releitura do CLAUDE.md antes de agir

Antes de criar um commit, uma branch, um PR ou uma issue, e também ao concluir qualquer implementação de código, o Claude deve reler este arquivo para confirmar que está seguindo as regras vigentes — especialmente relevante em sessões longas, onde o contexto inicial pode ter ficado distante.

## Estrutura de branches principais

- `{{BRANCH_PRODUCAO}}`: produção. Protegida — nunca commitar nem dar push direto aqui.
- `{{BRANCH_DESENVOLVIMENTO}}`: desenvolvimento. É a base para criar branches de `feature`, `bugfix`, `fix`, `chore`, `docs`, `refactor`, `test`.

### Regra geral (feature, bugfix, fix, chore, docs, refactor, test)

- Criar a branch a partir de `{{BRANCH_DESENVOLVIMENTO}}`.
- Abrir o PR com destino (`base`) em `{{BRANCH_DESENVOLVIMENTO}}`, nunca em `{{BRANCH_PRODUCAO}}`.

### Regra de hotfix (exceção)

- Criar a branch a partir de `{{BRANCH_PRODUCAO}}` (não de `{{BRANCH_DESENVOLVIMENTO}}`), porque o hotfix corrige algo que já está em produção e não pode vir misturado com código de `{{BRANCH_DESENVOLVIMENTO}}` ainda não liberado.
- Abrir **dois PRs**: um para `{{BRANCH_PRODUCAO}}` (leva a correção pra produção) e outro para `{{BRANCH_DESENVOLVIMENTO}}` (evita que o bug volte numa release futura).

<!-- guia: se o time usa trunk-based development em vez de Git Flow, substitua toda esta seção pela política real (branch única + feature flags) antes de usar. -->

## Branches — formato de nome

Formato: `<tipo>/{{PREFIXO_ISSUE}}-<id>-<descricao-curta-em-kebab-case>`

Tipos válidos (alinhados com os tipos de commit): `feature`, `bugfix`, `fix`, `hotfix`, `chore`, `docs`, `refactor`, `test`

- `bugfix`: correção de bug sem urgência de produção (merge para `{{BRANCH_DESENVOLVIMENTO}}`)
- `fix`: reservado para commits de correção dentro de uma branch (tipo de commit Conventional Commits)

Exemplo: `feature/{{PREFIXO_ISSUE}}-123-nome-curto`

## Commits

- Mensagens sempre em {{IDIOMA_PADRAO}}, descrevendo o que mudou e por que, quando couber em uma linha.
- Use Conventional Commits, sempre em mensagem curta e objetiva.

Tipos e exemplos:

```
feat: adiciona filtro de itens por disponibilidade
fix: corrige cancelamento de registro aprovado
docs: atualiza guia de onboarding
refactor: reorganiza serviço de domínio
test: cobre validação de entrada no cadastro
chore: ajusta configuração de desenvolvimento
```

### Antes de commitar

Revisar escopo sempre:

```
git status
git diff
```

Depois:

```
git add caminho/do/arquivo
git commit -m "tipo: resumo objetivo da mudança"
```

**Nunca usar `git add .` sem revisar antes.**

**Nunca incluir co-autor (`Co-Authored-By`) nas mensagens de commit.** As mensagens devem conter apenas o texto da mudança, sem nenhuma linha adicional de atribuição.

## Issues no rastreador (projeto {{CHAVE_PROJETO_TRACKER}})

Os modelos de descrição (Bug e Tarefa), os campos padrão (tipo, prioridade, labels) e o formato de título estão documentados em `JIRA_TAREFAS.md` — use esse arquivo como fonte ao criar qualquer issue no projeto **{{CHAVE_PROJETO_TRACKER}}**.

Duas regras de lá são reforçadas aqui porque dependem de ação do Claude, não apenas de formatação, e valem sempre:

- **Responsável:** sempre atribuir ao usuário ({{RESPONSAVEL_PADRAO}}). Se o Claude não conseguir localizar esse usuário no rastreador (ex: nome não encontrado via busca, ambiguidade entre contas), criar a issue **sem responsável atribuído** e avisar o usuário do motivo — nunca atribuir a outra pessoa ou adivinhar.
- **Data limite:** o Claude **deve perguntar ao usuário, toda vez**, se a issue tem prazo, antes de criar a issue — nunca definir uma data por conta própria, e nunca pular essa pergunta.

## Checks obrigatórios (rodar conforme o que foi alterado)

| Mudança | Check mínimo |
|---|---|
| Backend | `{{CMD_BUILD_BACKEND}}` |
| Backend com regra de negócio | `{{CMD_TEST_BACKEND}}` |
| Frontend | `{{CMD_BUILD_FRONTEND}}` |
| Frontend com comportamento novo | Teste unitário quando houver runner; enquanto não houver, documentar validação manual no PR |
| Frontend com lint relevante | `{{CMD_LINT_FRONTEND}}`, se o lint estiver limpo no contexto |
| Migration/modelo de banco | Revisar migration e validar que não aponta para banco errado |
| Documentação | Reler comandos, URLs e variáveis citadas |

Se a mudança tocar mais de uma camada (ex: backend com regra de negócio + frontend), aplicar **todos** os checks correspondentes às camadas alteradas — não apenas um deles.

<!-- guia: adicione linhas para camadas que existirem no projeto (mobile, infra/terraform, workers, jobs agendados, contratos de API). -->

## Abrindo Pull Request

### Antes do PR

1. Garantir que a branch está atualizada com a base correta (`{{BRANCH_DESENVOLVIMENTO}}` na regra geral, `{{BRANCH_PRODUCAO}}` em hotfix — ver "Estrutura de branches principais").
2. Rodar os checks mínimos conforme a tabela acima.
3. Confirmar que não há secrets novos, `.env.local`, dumps ou arquivos temporários.
4. Confirmar que migrations, scripts SQL ou alterações de banco estão explicadas no PR.

### Push

```
git push -u origin feature/{{PREFIXO_ISSUE}}-123-nome-curto
```

### Título do PR

Seguir Conventional Commits, igual ao commit principal:

```
feat: adiciona filtro de itens por disponibilidade
```

### Descrição do PR

Use o modelo em `PULL_REQUEST_TEMPLATE.md`, copiado para `.github/pull_request_template.md` na raiz do repositório — o GitHub preenche automaticamente a descrição de todo PR novo com esse conteúdo, então não é necessário reescrevê-lo manualmente.

Marcar no checklist apenas os itens aplicáveis à mudança feita.

### Regra adicional

Se o PR tocar frontend visual, incluir print ou descrever claramente o fluxo testado.

---

## Como adaptar este template a um novo projeto

<!-- guia: remova esta seção inteira depois de preencher. Ela existe só para o momento da adaptação. -->

1. **Substitua os placeholders.** Faça um find-and-replace de cada `{{...}}` da tabela do topo. Se um placeholder não se aplica (ex: projeto sem frontend), apague a linha inteira em vez de deixar o marcador.
2. **Confirme a política de branches.** Git Flow (`{{BRANCH_PRODUCAO}}` + `{{BRANCH_DESENVOLVIMENTO}}`) é o padrão deste template. Se o time usa trunk-based, reescreva as seções de branch e hotfix.
3. **Ajuste a tabela de checks.** Ela é a parte que mais varia entre projetos — cada linha deve corresponder a um comando que de fato existe e passa hoje.
4. **Decida o rastreador.** O modelo de issue (Bug e Tarefa, campos, estrutura de descrição) vive em `JIRA_TAREFAS.md`, escrito para Jira. Os campos (tipo, prioridade, responsável, labels, prazo) existem em Azure DevOps, GitHub Issues e Linear com nomes próximos — adapte lá, não aqui.
5. **Copie também `PULL_REQUEST_TEMPLATE.md`** para `.github/pull_request_template.md`. Este `CLAUDE.md` só referencia o modelo de PR, não o duplica.
6. **Mantenha a regra de aprovação intacta.** É a única seção que não deveria ser relaxada por projeto: nenhuma ação com efeito externo (push, PR, issue) sem confirmação explícita.
7. **Apague a tabela de placeholders e esta seção.** O `CLAUDE.md` final deve conter apenas regras, sem meta-instruções.
