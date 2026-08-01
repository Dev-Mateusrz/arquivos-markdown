# Convenções do Projeto — {{NOME_DO_SISTEMA}}

> **Template reutilizável.** Copie este arquivo para a raiz do repositório como `CLAUDE.md`, substitua todos os `{{PLACEHOLDERS}}` e remova as linhas marcadas com `<!-- guia: ... -->` e os blocos "Como adaptar" ao final.

## Placeholders deste template

| Placeholder | Significado | Exemplo |
|---|---|---|
| `{{NOME_DO_SISTEMA}}` | Nome do sistema/repositório | `SMSAgenda` |
| `{{CHAVE_PROJETO_TRACKER}}` | Chave do projeto no rastreador de issues | `SUBG-AGENDA` |
| `{{PREFIXO_ISSUE}}` | Prefixo da issue em minúsculo (usado em branch) | `sa` |
| `{{PREFIXO_ISSUE_MAIUSCULO}}` | Prefixo da issue em maiúsculo (código gerado pelo tracker) | `SA` |
| `{{BRANCH_PRODUCAO}}` | Branch de produção | `master` ou `main` |
| `{{BRANCH_DESENVOLVIMENTO}}` | Branch base de desenvolvimento | `develop` |
| `{{RESPONSAVEL_PADRAO}}` | Pessoa a quem toda issue é atribuída | `Nome Sobrenome` |
| `{{CMD_BUILD_BACKEND}}` | Comando de build do backend | `dotnet build ...` |
| `{{CMD_TEST_BACKEND}}` | Comando de teste do backend | `dotnet test ...` |
| `{{CMD_BUILD_FRONTEND}}` | Comando de build do frontend | `pnpm build` |
| `{{CMD_LINT_FRONTEND}}` | Comando de lint do frontend | `pnpm lint` |
| `{{CMD_TEST_FRONTEND}}` | Comando de teste do frontend | `pnpm test` |
| `{{SHELL_PADRAO}}` | Shell usado nos exemplos | `powershell` ou `bash` |

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

Usar o modelo abaixo para toda nova issue criada no projeto **{{CHAVE_PROJETO_TRACKER}}**, baseado no padrão já em uso no projeto (referência: issue {{PREFIXO_ISSUE_MAIUSCULO}}-1).

### Campos

- **Tipo:** `Tarefa` (ajustar para `Bug`, `Subtarefa`, etc., conforme o caso real)
- **Prioridade:** definir de acordo com a dificuldade/complexidade da tarefa:
  - `Highest`: mudança estrutural ou de alto risco, várias camadas, alto impacto
  - `High`: mudança relevante, exige atenção e cuidado, mas escopo definido
  - `Medium`: mudança padrão, escopo claro, complexidade moderada
  - `Low`: mudança pequena, baixo risco, baixa complexidade
- **Responsável:** sempre atribuir ao usuário ({{RESPONSAVEL_PADRAO}}). Se o Claude não conseguir localizar esse usuário no rastreador (ex: nome não encontrado via busca, ambiguidade entre contas), criar a issue **sem responsável atribuído** e avisar o usuário do motivo — nunca atribuir a outra pessoa ou adivinhar.
- **Categorias (labels):** atribuir conforme a área/objetivo da tarefa (ex: `backend`, `frontend`, `infra`, `documentacao` — reaproveitar labels já existentes no projeto sempre que possível; criar uma nova só se nenhuma existente cobrir o caso)
- **Data limite:** o Claude **deve perguntar ao usuário, toda vez**, se a issue tem prazo, antes de criar a issue — nunca definir uma data por conta própria, e nunca pular essa pergunta

### Estrutura da descrição

```markdown
## Contexto
[Por que essa tarefa existe — qual problema ou lacuna motiva a mudança]

## Objetivo
[O que a tarefa busca alcançar, de forma direta]

## Área afetada
- Front-end: [sim/não — o que muda]
- Back-end: [sim/não — o que muda]

## Escopo sugerido
- [item 1]
- [item 2]

## Critérios de aceite
- [condição que precisa ser verdadeira para considerar a tarefa concluída]

## Testes esperados
- [o que deveria ser validado, por camada]

## Observações técnicas
[Pontos de atenção, dependências ou contexto técnico relevante antes de implementar]
```

Título da issue: descrição curta e direta da tarefa (o código `{{PREFIXO_ISSUE_MAIUSCULO}}-XX` é gerado automaticamente pelo rastreador, não precisa ser incluído no texto).

> A regra de prioridade por dificuldade acima é uma proposta inicial — ajuste as faixas se não refletirem como você de fato avalia complexidade no dia a dia.

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

### Descrição do PR (template)

````markdown
## Resumo

[O que mudou e por que mudou]

## Tipo de mudança

- [ ] Feature
- [ ] Bugfix
- [ ] Hotfix
- [ ] Refactor
- [ ] Documentação
- [ ] Configuração/infra

## Como testar

1. [passo a passo para reproduzir/validar a mudança]

- [ ] Rodei build local
- [ ] Rodei testes unitários, quando houver script/configuração no projeto
- [ ] Rodei testes automatizados adicionais, quando aplicável
- [ ] Validei o fluxo principal alterado
- [ ] Inclui prints ou vídeo quando a mudança afeta interface

Comandos executados:

```{{SHELL_PADRAO}}
[listar os comandos reais rodados, conforme a tabela de checks]
```

Se não foram criados testes unitários, explique o motivo:

```text
[motivo]
```

## Cobertura da mudança

- [ ] Cobre componente, hook, service ou utilitário alterado
- [ ] Cobre estado de erro/loading/vazio quando aplicável
- [ ] Cobre comportamento visual/interativo relevante
- [ ] Não se aplica, pois a mudança é somente documental/configuração sem comportamento

## Impacto visual

- [ ] Não altera interface
- [ ] Altera interface

Prints ou vídeo, se houver:

> [adicionar após revisão visual]

## Variáveis de ambiente

- [ ] Não adiciona variáveis
- [ ] Adiciona/altera variáveis

## Checklist do autor

- [ ] A branch saiu da base correta (`{{BRANCH_DESENVOLVIMENTO}}` na regra geral, `{{BRANCH_PRODUCAO}}` em hotfix)
- [ ] O PR aponta para a base correta
- [ ] O título do PR está claro
- [ ] Commits seguem Conventional Commits, em {{IDIOMA_PADRAO}}
- [ ] Não inclui chaves, senhas ou dados sensíveis
- [ ] Não inclui arquivos temporários, logs, dumps locais ou screenshots soltos
````

Marcar no checklist apenas os itens aplicáveis à mudança feita.

### Regra adicional

Se o PR tocar frontend visual, incluir print ou descrever claramente o fluxo testado.

---

## Como adaptar este template a um novo projeto

<!-- guia: remova esta seção inteira depois de preencher. Ela existe só para o momento da adaptação. -->

1. **Substitua os placeholders.** Faça um find-and-replace de cada `{{...}}` da tabela do topo. Se um placeholder não se aplica (ex: projeto sem frontend), apague a linha inteira em vez de deixar o marcador.
2. **Confirme a política de branches.** Git Flow (`{{BRANCH_PRODUCAO}}` + `{{BRANCH_DESENVOLVIMENTO}}`) é o padrão deste template. Se o time usa trunk-based, reescreva as seções de branch e hotfix.
3. **Ajuste a tabela de checks.** Ela é a parte que mais varia entre projetos — cada linha deve corresponder a um comando que de fato existe e passa hoje.
4. **Decida o rastreador.** O modelo de issue foi escrito para Jira, mas os campos (tipo, prioridade, responsável, labels, prazo) existem em Azure DevOps, GitHub Issues e Linear com nomes próximos. Renomeie os campos, mantenha a estrutura da descrição.
5. **Mantenha a regra de aprovação intacta.** É a única seção que não deveria ser relaxada por projeto: nenhuma ação com efeito externo (push, PR, issue) sem confirmação explícita.
6. **Apague a tabela de placeholders e esta seção.** O `CLAUDE.md` final deve conter apenas regras, sem meta-instruções.
