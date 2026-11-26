# Padrão de branches e commits

> **Gatilho** — Leia e aplique esta regra antes de criar uma branch, preparar alterações para commit ou escrever uma mensagem de commit. Se o projeto usa squash merge, aplique o formato de commit também ao título do pull request.

## Proibições

- NUNCA faça commit ou push diretamente nas branches de integração, produção ou em outras branches protegidas pelo projeto. Neste repositório, use `main` como base protegida.
- NUNCA use `git add .`, `git add -A`, `git add -u` sem caminhos ou `git commit -a`. Prepare somente os arquivos ou trechos que pertencem ao commit.
- NUNCA inclua credenciais, chaves privadas, arquivos `.env` com valores reais ou arquivos temporários fora do escopo. NUNCA inclua `Co-Authored-By:` automático nem assinaturas de IA.
- NUNCA execute `git push` sem autorização explícita do usuário nem ignore hooks ou checks de commit configurados.

## Formato de branches

```text
<tipo>/<descricao-em-kebab-case>
<tipo>/<chave-jira-em-minusculas>-<descricao-em-kebab-case>
```

- Use `feature` para funcionalidade, `bugfix` para correção comum, `hotfix` para correção urgente em produção, `release` para preparação de versão, `chore` para manutenção, `refactor` para refatoração e `docs` para documentação. Use `release` somente se o fluxo do projeto prevê essa branch.
- Use apenas letras `a-z`, números `0-9` e hífens simples entre os termos após a barra. Use uma descrição curta sem acentos.
- SE houver ticket Jira vinculado, ENTÃO inclua sua chave em minúsculas (`ABC-123` vira `abc-123`). SE o projeto exigir ticket e a chave estiver ausente, ENTÃO solicite a chave antes de criar a branch.
- SE o projeto adotar um prefixo de agente, ENTÃO use o prefixo configurado (`ai/`, `claude/`, `codex/` ou `cursor/`) no lugar do tipo. Preserve a chave do ticket quando aplicável.

## Formato de commits

```text
<tipo>[(<escopo>)][!]: <descrição no imperativo>

<corpo opcional>

<rodapé opcional>
```

- Os colchetes indicam partes opcionais. Use `feat`, `fix`, `refactor`, `style`, `test`, `docs`, `chore`, `perf`, `ci` ou `build`, conforme o propósito da alteração. Omita os parênteses quando não houver escopo e use `!` somente para sinalizar quebra de compatibilidade.
- Escreva o assunto em português do Brasil, no imperativo, sem ponto final. Mire até 50 caracteres e respeite o máximo de 72, contando o prefixo.
- SE precisar explicar a motivação da mudança, ENTÃO adicione um corpo após uma linha em branco. Separe também o rodapé do bloco anterior com uma linha em branco.
- SE a alteração quebrar compatibilidade, ENTÃO sinalize a quebra com `!` antes dos dois-pontos ou com o rodapé `BREAKING CHANGE: <impacto e orientação de migração>`. SE o squash usar o título do PR como assunto do commit final, ENTÃO inclua `!` no título.

## Exemplos

| Item | Resultado | Exemplo | Motivo |
| --- | --- | --- | --- |
| Branch | Certo | `docs/revisa-padrao-de-commits` | Documentação sem ticket em projeto que o dispensa |
| Branch | Certo | `bugfix/abc-142-corrige-filtro-por-unidade` | Correção com chave Jira em minúsculas |
| Branch | Errado | `feature/ABC-142_filtro-unidade` | Maiúsculas e sublinhado |
| Branch | Errado | `abc-142-corrige-filtro` | Prefixo ausente |
| Commit | Certo | `docs: atualiza padrão de commits` | Escopo opcional e descrição no imperativo |
| Commit | Certo | `feat(api)!: altera resposta do agendamento` | Quebra de compatibilidade sinalizada |
| Commit | Errado | `feat: adicionado filtro` | Descrição no particípio |
| Commit | Errado | `ajustes gerais.` | Tipo ausente e ponto final |

## Fluxo passo a passo

### Criar a branch

1. Execute `git status --short --branch` e identifique a branch atual e as alterações locais.
2. Defina a base e o destino do PR conforme o projeto. Em trunk-based ou GitHub Flow, use a branch principal para ambos (`main` neste repositório). Em GitFlow, use `develop` no trabalho regular, siga o fluxo de releases do projeto e crie `hotfix` a partir da branch de produção. Para `hotfix` em GitFlow, planeje a incorporação da correção em produção e em `develop`, com dois PRs quando esse for o mecanismo de integração do projeto.
3. Monte o nome e execute `git check-ref-format --branch <nome>`. Confirme também o formato desta regra, incluindo o ticket quando aplicável.
4. SE a base for publicada em um remoto, ENTÃO atualize a referência com `git fetch <remoto> refs/heads/<base>:refs/remotes/<remoto>/<base>` e, após sucesso, crie a branch com `git switch --no-track -c <nome> refs/remotes/<remoto>/<base>`. SE o projeto trabalhar sem remoto, ENTÃO use `git switch -c <nome> <base>`. SE alterações locais impedirem a troca segura, ENTÃO preserve-as e informe o impedimento.
5. Mantenha a branch focada em uma entrega pequena. Busque integrá-la em 1 a 3 dias e divida entregas maiores em partes que possam ser revisadas e integradas separadamente.

### Preparar e criar o commit

1. Execute `git status --short --branch` e revise `git diff` e `git diff --cached`. Confirme que a branch atual permite commits e que cada commit tem um único propósito.
2. Prepare arquivos inteiros com `git add -- <caminho>` ou selecione trechos com `git add -p -- <caminho>`. SE houver alterações preparadas fora do escopo, ENTÃO preserve o índice e resolva a seleção antes de executar o commit.
3. Execute `git diff --cached --check` e revise `git diff --cached` para confirmar o escopo e verificar a presença de arquivos sensíveis.
4. Valide a mensagem pelo formato acima. SE o projeto tiver `commitlint`, hooks como Husky ou validação de título no CI, ENTÃO respeite as verificações aplicáveis e corrija as falhas antes de prosseguir.
5. Execute `git commit -m "<assunto>"` para uma mensagem de uma linha ou `git commit -F <arquivo-da-mensagem>` quando houver corpo ou rodapé. Confirme o resultado com `git log -1 --format=%B` e `git status --short --branch`.
