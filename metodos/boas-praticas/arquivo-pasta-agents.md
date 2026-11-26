> **Instrução para a IA (Meta-Prompt):** Este documento é um **guia de arquitetura** para estruturar o `AGENTS.md` e a pasta `.agents/` de um repositório. Ao utilizá-lo para criar ou refatorar a documentação de um projeto, **não copie os nomes fictícios dos exemplos** (`Projeto X`, `frontend-smsagenda`, `ESPAÇO-JIRA`). Inspecione primeiro a estrutura de pastas, branches e stack tecnológica do repositório atual e gere um `AGENTS.md` enxuto (máx. 120 linhas) funcionando estritamente como índice de roteamento para `.agents/`.


# Estrutudando um arquivo AGENTS.md com Boas Práticas

Atualizado 26/11/2026

Antes eu estruturava e organizava o arquivo `AGENTS.md` da forma errada, misturando regras de segurança, checks de build/teste, padrões de Git e um template extenso do Jira. Isso fazia a eficiência da minha IA cair drásticamente por consumir tokens e foco - lendo todas as regras sem necessidade.

O Objetivo do `AGENTS.md` é funcionar como índice de roteamento curto que redireciona para arquivos modulares do projeto, carregando apenas sob demanda.

## Boas Práticas

- Limitar o Tamanho do Conteúdo do arquivo AGENTS: Mantenha o AGENTS.md principal entre 60 e 120 linhas (nunca passe de 150). Ele é injetado em 100% das interações; tudo o que não for necessário em todas as tarefas deve ir para .agents/.

- Gatilhos Condicionais Explícitos (When-to-Load): Não basta listar os arquivos. A IA precisa de instruções imperativas de gatilho, como: "Antes de criar uma branch ou commit, leia .agents/padrao-commit-branch.md"

- Separação entre Guardrails e Procedimentos. Regras de segurança inegociáveis (como não dar git push sem aprovação) ficam sempre na raiz. Templates, checklists e fluxos passo a passo ficam nos arquivos únicos e específicos.

- Regra da Cascata (Monorepos / Multi-Repo). Como você trabalha com frontend-smsagenda e backend-smsagenda, a especificação oficial do AGENTS.md permite ter um AGENTS.md na raiz do workspace (com regras globais de Git/Jira) e um AGENTS.md dentro de cada sub-repositório com os comandos específicos de pnpm ou dotnet.


## Arquitetura Recomendada

workspace-projeto/                   # Pasta local de trabalho (não é um repo Git) mas serve para juntar os dois repo.
├── AGENTS.md                       # [OPCIONAL] Apenas mapa de contexto multi-repo (quando trabalhar nos 2 juntos)
│
├── frontend-smsagenda/          # Repositório Git 1
│   ├── AGENTS.md                     # Índice do Front-end + Guardrails + Gatilhos para .agents/
│   └── .agents/
│       ├── padrao-commit-branch.md   # Regras globais de Git, branch e commit
│       ├── padrao-pullrequest.md         # Regras globais de PR + exigência de screenshot/UI
│       ├── padrao-jira.md                     # Template de Tarefas no Jira
│       └── checks-frontend.md            # Comandos pnpm build, pnpm lint e padrões de checks
│
└── backend-smsagenda/          # Repositório Git 2
    ├── AGENTS.md                     # Índice do Back-end + Guardrails + Gatilhos para .agents/
    └── .agents/
        ├── padrao-commit-branch.md   # Regras globais de Git, branch e commit
        ├── padrao-pullrequest.md         # Regras globais de PR (sem screenshot)
        ├── padrao-jira.md                     # Template de Tarefas no Jira
        └── checks-backend.md            # Comandos dotnet build, dotnet test e regras EF/Migrations


## Estrutura do Agents.md

```
# Exemplo — Projeto X

## 1. Guardrails Críticos (Sempre Ativos)

* **Aprovação obrigatória:** Nunca execute `git push`, abra Pull Requests ou crie issues no Jira sem antes exibir o conteúdo exato ao usuário e receber confirmação explícita (ex: "aprovado"), mesmo que o prompt inicial pareça autorizar.
* **Ações locais permitidas:** Criar branches locais e realizar commits locais (sem push) é permitido sem pausa.
* **Idioma padrão:** Commits, descrições de branches, PRs e issues no Jira devem ser escritos em **português do Brasil**.
* **Branches protegidas:** Nunca faça commit ou push diretamente em `main` (`frontend-x`), `main` (`backend-x`) ou `develop`.

## 2. Roteamento de Regras (Carregamento Sob Demanda)

Leia o arquivo correspondente em `.agents/` **antes** de executar qualquer uma das ações abaixo:

| Ação / Contexto | Arquivo de Regra Obrigatório |
| :--- | :--- |
| Criar branch ou realizar `git commit` | Leia `.agents/padrao-commit-branch.md` antes de agir. |
| Validar código antes de finalizar tarefa | Leia `.agents/checks-validacao.md` e execute os checks da camada alterada. |
| Preparar ou abrir um Pull Request | Leia `.agents/padrao-pullrequest.md` antes de montar o texto. |
| Criar ou estruturar tarefa no Jira (`ESPAÇO-JIRA`) | Leia `.agents/padrao-jira.md` e siga o template exato. |

## 3. Mapa de Repositórios

* **`frontend-x`:** Produção em `main` | Desenvolvimento em `develop`.
* **`backend-x`:** Produção em `main` | Desenvolvimento em `develop`.

## 4. Higiene de Contexto em Sessões Longas

Antes de executar qualquer ação de Git, PR ou Jira — ou ao concluir uma implementação extensa — releia este arquivo e o arquivo específico em `.agents/` para garantir conformidade com as regras vigentes.
```


## Dicas Extras de Compatibilidade Cruzada

Se parte da sua equipe usa Claude Code, Cursor ou Windsurf além do Codex, crie um symlink (link simbólico) na raiz do projeto apontando CLAUDE.md -> AGENTS.md. Assim, todas as ferramentas leem exatamente a mesma fonte da verdade sem duplicação de arquivos.
