# Hooks locais do frontend

Copie os templates para o projeto consumidor, configure-os e instale-os conforme abaixo. A instalação deste conjunto não altera os hooks do repositório de templates.

## Arquivos a copiar

| Template | Destino no projeto |
|---|---|
| [config-frontend.txt](config-frontend.txt) | `.githooks/config.sh` |
| [pre-commit-frontend.txt](pre-commit-frontend.txt) | `.githooks/pre-commit` |
| [prepare-commit-msg-frontend.txt](prepare-commit-msg-frontend.txt) | `.githooks/prepare-commit-msg` |
| [commit-msg-frontend.txt](commit-msg-frontend.txt) | `.githooks/commit-msg` |
| [pre-push-frontend.txt](pre-push-frontend.txt) | `.githooks/pre-push` |
| [post-merge-frontend.txt](post-merge-frontend.txt) | `.githooks/post-merge` |
| [install.mjs.txt](install.mjs.txt) | `.githooks/install.mjs` |
| [lint-staged.config.mjs.txt](lint-staged.config.mjs.txt) | `lint-staged.config.mjs` |
| [size-limit.config.json.txt](size-limit.config.json.txt) | `.size-limit.json` |

Em `config.sh`, substitua os placeholders por um prefixo real, como `PROJ`, e pelas branches protegidas. Escolha o gerenciador do projeto em `PACKAGE_MANAGER`; `HOOK_PACKAGE_MANAGER` pode sobrescrevê-lo. `JIRA_PROJECT_KEY` pode sobrescrever o prefixo, usando letras maiúsculas.

O prefixo identifica a referência de trabalho; não contém credenciais. Branches seguem `<tipo>/proj-42-descricao`, aceitando a chave sem distinção de caixa. Tipos reconhecidos: `feat`, `feature`, `fix`, `bugfix`, `hotfix`, `chore`, `docs`, `refactor`, `test`, `style`, `perf`, `build`, `ci` e `revert`. Nomes sem chave inequívoca não recebem injeção automática.

## Instalação e scripts do projeto

Instale versões compatíveis de `lint-staged`, ESLint, Prettier, TypeScript, `size-limit` e `@size-limit/file` nas dependências de desenvolvimento usando o gerenciador e lockfile adotados. Para o exemplo de bundle, use somente o plugin `file`, pois o build já pertence à aplicação. Os hooks usam shell POSIX e utilitários disponíveis em Git for Windows/Git Bash, macOS e Linux. O instalador usa o Node já necessário ao frontend, sem biblioteca adicional.

Adapte este fragmento ao `package.json` raiz, preservando scripts existentes:

```json
{
  "scripts": {
    "prepare": "node .githooks/install.mjs",
    "hooks:pre-commit": "lint-staged",
    "hooks:audit": "npm audit --audit-level=high --package-lock-only",
    "typecheck": "tsc --noEmit",
    "bundle:check": "size-limit --config .size-limit.json",
    "bundle:verify": "npm run build && npm run bundle:check",
    "hooks:pre-push": "npm run typecheck && npm run test:unit && npm run docs:check && npm run bundle:verify"
  }
}
```

Os scripts `build`, `test:unit` e `docs:check` precisam existir e executar verificações reais; ajuste os nomes à stack. O exemplo usa npm; troque as chamadas internas quando o projeto usar outro gerenciador. Para pnpm, defina `hooks:audit` como `pnpm audit --audit-level=high`. Para Yarn/Bun, adapte a auditoria à versão adotada: esses comandos não são intercambiáveis. Escolha um gerenciador, fixe sua versão e mantenha apenas o lockfile correspondente.

O `tsc --noEmit` deve carregar o projeto correto. Ajuste `-p` se necessário; em projetos com referências, configure um comando que percorra todos os projetos, pois um `tsconfig.json` raiz com `files: []` pode não checar o aplicativo. Frameworks que exigem verificador próprio devem usá-lo. Não passe a lista staged ao TypeScript. Tipagem complementa lint e testes; não garante comportamento em execução.

Se já existir um `prepare`, encadeie o instalador sem apagar o trabalho existente. Em workspaces, mantenha essa configuração no pacote raiz. O instalador configura `core.hooksPath` localmente, aceita `.git` como diretório ou arquivo de worktree e recusa sobrescrever outro gerenciador de hooks. Não combine este modelo com Husky sem escolher qual gerenciará o caminho.

Depois da cópia, execute `node .githooks/install.mjs`, ou instale as dependências com scripts de ciclo de vida habilitados. `prepare` não roda no clone por si só; o comportamento depende do gerenciador e de suas políticas de scripts. CI e `SKIP_GIT_HOOKS=1` fazem o instalador sair sem modificar a configuração. Arquivos distribuídos sem `.git` também são ignorados.

Mantenha LF no projeto consumidor:

```gitattributes
.githooks/* text eol=lf
```

Em sistemas Unix, o instalador aplica a permissão de execução. Para preservá-la no índice Git, após adicionar os arquivos use:

```shell
git update-index --chmod=+x .githooks/pre-commit .githooks/prepare-commit-msg .githooks/commit-msg .githooks/pre-push .githooks/post-merge
```

## Responsabilidade e comportamento

| Gatilho | O que executa |
|---|---|
| `pre-commit` | Executa lint-staged; audita quando houver lockfile adicionado/modificado/renomeado no stage |
| `prepare-commit-msg` | Preenche uma mensagem vazia, insere a chave em um título convencional sem escopo ou acrescenta um trailer `Refs:` |
| `commit-msg` | Valida o título convencional, descrição mínima, chave no título/corpo e limite de comprimento |
| `pre-push` | Inspeciona todas as refs de destino; recusa alterações/exclusões das branches protegidas e roda `hooks:pre-push` uma vez se houver atualização de conteúdo |
| `post-merge` | Compara `ORIG_HEAD` e `HEAD`; sincroniza dependências alteradas com lockfile congelado, se não houver mudanças locais nesses arquivos |

O lint-staged seleciona arquivos com nomes seguros e oculta por padrão alterações não adicionadas de arquivos parcialmente staged. Preserve suas proteções de stash/restauração. Não use `git add .` no hook nem desabilite essas proteções para ganhar tempo. A configuração exemplo executa ESLint e Prettier em sequência nos mesmos arquivos, sem tarefas concorrentes sobrepostas.

Mantenha o feedback de commit curto e meça no projeto real; dois segundos é um objetivo de experiência, não uma garantia. Evite build ou suíte completa no pre-commit. A auditoria usa rede e o guard de bundle executa um build: podem demorar. Se o build inviabilizar o fluxo local, retire `bundle:verify` de `hooks:pre-push` e mantenha o bloqueio obrigatório no CI. Se usar testes de arquivos afetados, inclua dependências e um fallback de cobertura quando o impacto não for conhecido.

A injeção preserva o tipo já escrito, o marcador `!`, o escopo existente e uma chave já informada. Execuções repetidas não acrescentam trailers duplicados. O temporário é criado junto da mensagem e substituído por rename, sem `sed -i`, com limpeza em erro/sinal.

Mensagens de merge/squash/reutilização fornecidas pelo Git não são reescritas pelo preparo. `commit-msg` reconhece o estado de merge/revert/squash e títulos de revert/autosquash. Amend com mensagem reutilizada é preservado; uma mensagem normal de amend continua sujeita à validação. Quando uma mensagem nova é fornecida explicitamente, o Git pode identificá-la como `message`, mesmo no amend. Não há isenção universal de qualquer commit editado por ferramenta.

O limite usa `${#SUBJECT}` conforme a locale do shell, não grafemas. Em uma locale UTF-8, letras acentuadas podem ser contadas como caracteres; em outras, a contagem pode equivaler a bytes. Teste a locale adotada pelo time. Prefira `core.commentChar` explícito; o modo `auto` não é suportado pela reescrita de títulos deste template.

## Auditoria de dependências no commit

O hook aciona `hooks:audit` depois do lint-staged somente se um lockfile entrou no stage. Se manifests, lockfiles ou configurações de dependências tiverem alterações não adicionadas ou arquivos não rastreados, ele recusa a auditoria para não validar uma árvore diferente da que será commitada. Resolva essas diferenças; não há `git add .` automático.

O nível `high` bloqueia vulnerabilidades conhecidas altas e críticas, incluindo dependências de desenvolvimento quando não omitidas pela configuração do gerenciador. Erros de rede também falham: não use `--ignore-registry-errors` ou `audit fix` neste fluxo. `SKIP_DEPENDENCY_AUDIT=1` permite adiar apenas a auditoria local; registre a razão e exija o check no servidor.

O CI deve executar a auditoria mesmo sem mudança de lockfile, pois surgem novos avisos ao longo do tempo. Ela não comprova ausência de malware ou falhas ainda desconhecidas. Em monorepos com lockfile único, audite na raiz; com instalações independentes, adapte `hooks:audit` para percorrer cada raiz afetada, pois detectar vários lockfiles não faz o comando raiz auditá-los automaticamente.

## Sincronização após merge

O template ativa a sincronização automática para npm/pnpm. `npm ci` recria `node_modules`; `pnpm install --frozen-lockfile` preserva o lockfile. A instalação exige um lockfile existente e consistente. Ela mostra sua saída e não executa scripts de ciclo de vida por padrão (`--ignore-scripts`). Pacotes que dependem de geração ou binários nativos podem exigir uma etapa manual revisada; isso não significa que todo ambiente estará pronto após a instalação.

Configure `AUTO_INSTALL_AFTER_MERGE=0` em `config.sh` ou no ambiente para apenas avisar. Para um repositório confiável que necessite desses scripts, configure `HOOK_INSTALL_SCRIPTS=1`, respeitando também as políticas de aprovação do gerenciador. Essa opção pode executar código das dependências recebidas pelo merge.

O hook adia a instalação se houver mudanças locais de dependências, arquivos correspondentes não rastreados ou outra instalação deste hook em andamento. Se o processo for interrompido sem limpeza, verifique a ausência de instalador ativo antes de remover o diretório vazio indicado por `git rev-parse --git-path frontend-install.lock`. O lock não coordena instalações manuais.

`post-merge` cobre merges bem-sucedidos, inclusive fast-forward e pull com merge. Pull com rebase precisa de outro gatilho; squash recebe apenas um aviso para instalação manual após o commit. Uma falha de instalação é informada, mas não desfaz o merge.

## Orçamento de bundle antes do push

Copie a configuração para `.size-limit.json` e substitua os limites por valores medidos e aprovados no projeto, com unidade, por exemplo `180 kB`. Os caminhos `dist/assets/*.js` e `dist/assets/*.css` são exemplos para uma saída como a do Vite. Ajuste-os ao build real; remova justificadamente o check de CSS se esse artefato não existir. Não use `--ignore-missing`: caminho errado ou artefato ausente deve falhar.

`bundle:verify` gera o build de produção antes de medir. `bundle:check` apenas mede os artefatos e deve ser usado no CI após a etapa de build, evitando uma segunda compilação. Configure `build` para limpar a saída antiga; o guard não deve somar arquivos obsoletos. Não há promessa de mini-build em memória.

Os checks de push analisam os arquivos locais, que podem conter mudanças não commitadas. O CI deve repetir as validações no conteúdo do PR; o resultado local não comprova sozinho que todos os commits enviados foram verificados.

O exemplo soma o tamanho gzip de todos os chunks correspondentes em cada grupo. Isso controla o total, mas não representa o JavaScript inicial de cada rota. Para projetos com divisão de código, acrescente orçamentos de carregamento por rota baseados no manifesto do bundler. Em SSR, separe assets do navegador de bundles do servidor. Gzip é uma métrica de transferência; não substitui medições de execução, LCP ou outros indicadores reais.

No workflow de frontend, configure `CMD_AUDIT_FRONTEND` como o comando de `hooks:audit` e `CMD_BUNDLE_CHECK_FRONTEND` como o de `bundle:check`, usando o gerenciador escolhido. Exija ambos na proteção de branches.

## Emergência e proteção no servidor

`ALLOW_DIRECT_PUSH=1` pula apenas a barreira local de branches; os checks de push continuam. `SKIP_GIT_HOOKS=1` pula todos os hooks deste conjunto e sua instalação. No Git Bash/POSIX:

```shell
ALLOW_DIRECT_PUSH=1 git push
SKIP_GIT_HOOKS=1 git commit -m "chore(PROJ-42): corrige infraestrutura"
```

Em PowerShell, use `$env:ALLOW_DIRECT_PUSH='1'` ou `$env:SKIP_GIT_HOOKS='1'` e remova a variável após o comando. Registre a justificativa no fluxo do projeto. `--no-verify` não desativa `prepare-commit-msg`, mas a variável explícita acima o desativa.

Hooks são conveniência local. Configure proteção de branches no servidor e CI nos PRs de desenvolvimento e produção, usando os mesmos comandos reais de tipagem, lint, testes, documentação, auditoria e bundle. Valide mensagens de commits no intervalo do PR; se a política for squash por título de PR, valide também esse título na automação correspondente. Proteger apenas o push local não protege o remoto.

Gitleaks é uma proteção adicional de segredos, independente da auditoria de pacotes. Se adotado, integre sua versão/configuração ao script de commit e ao CI. `console.log` só será barrado se a regra correspondente estiver habilitada no ESLint; lint-staged apenas executa as ferramentas configuradas.

## Verificação deste conjunto

Execute `python -B -m unittest discover -s Templates/frontend/templates/githooks -p test_githooks.py -v` na raiz desta biblioteca. Os testes usam Git, Node e um shell POSIX em repositórios temporários. As chamadas ao gerenciador são simuladas; ESLint, Prettier e lint-staged precisam ser validados com as dependências do projeto consumidor.

Fontes: [Git — contratos dos hooks](https://git-scm.com/docs/githooks), [lint-staged — stage parcial e tarefas](https://github.com/lint-staged/lint-staged), [npm — ciclo de vida dos scripts](https://docs.npmjs.com/cli/v11/using-npm/scripts/), [npm audit](https://docs.npmjs.com/cli/v11/commands/npm-audit/), [pnpm audit](https://pnpm.io/cli/audit), [npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci/), [pnpm install](https://pnpm.io/cli/install), [TypeScript — noEmit](https://www.typescriptlang.org/tsconfig/noEmit.html) e [Size Limit](https://github.com/ai/size-limit).
