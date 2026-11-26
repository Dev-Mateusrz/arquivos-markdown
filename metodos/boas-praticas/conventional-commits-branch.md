> **Instrução para a IA:** Este documento contém as diretrizes de referência de mercado para Git. Ao usá-lo para criar o arquivo `.agents/padrao-commit-branch.md` de um projeto, converta estes conceitos em regras imperativas, adapte o fluxo (Trunk-Based ou GitFlow) e o prefixo de ticket à realidade do repositório atual, e inclua exemplos práticos de certo vs. errado.


# Conventional Commits e Conventional Branches


Atualização: 26/11/2026

Hoje, o mercado combina a especificação Conventional Commits 1.0.0 com a emergente Conventional Branch 1.1.0 e estratégias de integração contínua (Trunk-Based Development ou GitHub Flow simplificado), focando em automação de CI/CD, rastreabilidade com Jira e governança de código gerado por IA.

## Boas Práticas de Conventional Commits

O objetivo hoje não é apenas "deixar o histórico bonito", mas tornar os commits legíveis por máquinas para gerar changelogs, versionamento semântico (SemVer) e disparar pipelines de deploy.

- Anatomia Rígida: < tipo >(< escopo >): < descrição >.

- Regra dos 50/72 Caracteres: O título deve ter idealmente até 50 caracteres (no máximo 72) no modo imperativo ("adiciona", "corrige"), sem ponto final. O corpo (opcional, separado por linha em branco) explica o "porquê" e não o "como".

- Sinalização de Quebra de Contrato (!): Sempre que uma mudança no back-end quebrar a compatibilidade com o front-end ou clientes externos, usa-se ! antes dos dois pontos (ex: feat(api)!: altera payload de retorno do agendamento) ou BREAKING CHANGE: no rodapé.

- Atenção ao Squash Merge no GitHub/GitLab: Um erro clássico apontado pelo mercado é a equipe escrever commits perfeitos localmente, mas na hora de fazer Squash and Merge no Pull Request, o título do PR não segue o padrão e apaga todo o histórico semântico. Boa prática: O título do PR também deve seguir o formato Conventional Commits.

- Automação na Ponta (Shift-Left): Times eficientes não dependem apenas da memória do dev ou da IA; eles validam a mensagem antes do commit subir usando commitlint + husky (ou GitHub Actions no PR).

## Boas Práticas de Conventional Branches

- Adoção da Conventional Branch (incl. Prefixos de IA): A especificação Conventional Branch padronizou os prefixos em minúsculo (feature/, bugfix/, hotfix/, release/, chore/), exigindo apenas letras a-z, números 0-9 e hífens (sem underscores ou maiúsculas). Na versão 1.1.0, ela introduziu prefixos opcionais para rastrear branches criadas autonomamente por agentes (ai/, claude/, codex/, cursor/), embora em times com Jira o padrão :
< tipo >/< ticket-id >-< descricao > continue sendo o mais forte para integração automática.

- Branches de Vida Curta (Short-Lived Branches): O mercado abandonou branches que duram semanas. O padrão eficiente hoje é que uma branch viva no máximo 1 a 3 dias, com PRs pequenos e focados, reduzindo conflitos de merge e acelerando o Code Review.

- GitFlow vs. Trunk-Based / GitHub Flow:
  - O Trunk-Based Development (ou GitHub Flow com main + branches curtas + Feature Flags) é o padrão dominante para times ágeis com CI/CD automatizado.

  - O GitFlow tradicional (com develop, release/*, master) hoje é considerado legado para aplicações web/SaaS com deploy contínuo, pois gera atrito de merge e exige duplo PR em hotfixes. Ele só é mantido quando há ciclos de release agendados ou necessidade de homologação isolada em develop antes de produção.
