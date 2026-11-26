# Subagentes do Codex

Esta coleção reúne **35 subagentes** selecionados do [VoltAgent/awesome-codex-subagents](https://github.com/VoltAgent/awesome-codex-subagents). A organização abaixo acompanha as pastas deste repositório; cada item leva ao arquivo `.toml` correspondente.

## Base (6)

- [architect-reviewer](Base/architect-reviewer.toml) — Revisa arquitetura e dependências ao avaliar mudanças estruturais.
- [code-mapper](Base/code-mapper.toml) — Localiza arquivos e fluxos de execução antes de alterar código desconhecido.
- [code-reviewer](Base/code-reviewer.toml) — Avalia clareza, complexidade e manutenção de módulos e implementações.
- [docs-researcher](Base/docs-researcher.toml) — Pesquisa documentação para esclarecer APIs, versões e limitações técnicas.
- [reviewer](Base/reviewer.toml) — Revisa diffs e PRs para encontrar bugs, regressões e testes ausentes.
- [security-auditor](Base/security-auditor.toml) — Audita segurança em autenticação, permissões, entradas e tratamento de segredos.

## Backend (6)

- [api-designer](Backend/api-designer.toml) — Define contratos, esquemas e erros antes de criar ou alterar APIs.
- [backend-developer](Backend/backend-developer.toml) — Implementa funcionalidades e corrige falhas em serviços e APIs.
- [database-optimizer](Backend/database-optimizer.toml) — Investiga lentidão no banco e propõe melhorias em consultas e índices.
- [performance-engineer](Backend/performance-engineer.toml) — Investiga gargalos de latência, recursos, renderização e escalabilidade.
- [qa-expert](Backend/qa-expert.toml) — Planeja cenários de teste e critérios de aceite para funcionalidades e releases.
- [sql-pro](Backend/sql-pro.toml) — Cria e revisa consultas SQL, transações e migrações de banco.

## Frontend (8)

- [accessibility-tester](Frontend/accessibility-tester.toml) — Verifica acessibilidade de componentes e fluxos, incluindo teclado, foco e semântica.
- [anti-ui-slop-reviewer](Frontend/anti-ui-slop-reviewer.toml) — Revisa interfaces para identificar padrões genéricos e desvios do design system.
- [browser-debugger](Frontend/browser-debugger.toml) — Reproduz falhas no navegador e analisa console, rede e comportamento da interface.
- [design-bridge](Frontend/design-bridge.toml) — Transforma um DESIGN.md em orientações para implementar telas fiéis ao design.
- [frontend-developer](Frontend/frontend-developer.toml) — Implementa telas, componentes, estados e integrações com APIs.
- [microservices-architect](Frontend/microservices-architect.toml) — Define limites e contratos entre serviços em sistemas distribuídos.
- [mobile-developer](Frontend/mobile-developer.toml) — Implementa e depura aplicativos mobile, considerando navegação, permissões e conectividade.
- [ui-ux-tester](Frontend/ui-ux-tester.toml) — Testa jornadas e interações da interface e registra defeitos reproduzíveis.

## Refatoração (3)

- [dependency-manager](Refatoração/dependency-manager.toml) — Revisa atualizações, compatibilidade, lockfiles e riscos de dependências.
- [legacy-modernizer](Refatoração/legacy-modernizer.toml) — Planeja migrações graduais de código e tecnologias legadas.
- [refactoring-specialist](Refatoração/refactoring-specialist.toml) — Reorganiza código para melhorar manutenção sem alterar seu comportamento.

## Documentação (3)

- [api-documenter](Documentação/api-documenter.toml) — Documenta APIs para consumidores, com contratos, autenticação, erros e exemplos reais.
- [documentation-engineer](Documentação/documentation-engineer.toml) — Cria e atualiza guias técnicos de instalação, desenvolvimento e operação.
- [readme-generator](Documentação/readme-generator.toml) — Cria e organiza READMEs com informações verificadas no repositório.

## DebugTests (3)

- [debugger](DebugTests/debugger.toml) — Investiga a causa de bugs e valida correções em falhas complexas ou intermitentes.
- [error-detective](DebugTests/error-detective.toml) — Analisa logs e exceções para identificar a origem provável de uma falha.
- [test-automator](DebugTests/test-automator.toml) — Implementa testes automatizados e cobertura contra regressões.

## Outros (6)

- [context-manager](Outros/context-manager.toml) — Prepara contexto e restrições do projeto antes de delegar tarefas.
- [devops-engineer](Outros/devops-engineer.toml) — Configura pipelines de CI/CD, ambientes e automações de entrega.
- [docker-expert](Outros/docker-expert.toml) — Revisa Dockerfiles, otimiza imagens e investiga falhas em containers.
- [git-workflow-manager](Outros/git-workflow-manager.toml) — Orienta fluxos de branches, PRs, merges, releases e hotfixes.
- [knowledge-synthesizer](Outros/knowledge-synthesizer.toml) — Consolida resultados de vários agentes, destacando conclusões e divergências.
- [ponder-reviewer](Outros/ponder-reviewer.toml) — Faz revisões aprofundadas em múltiplas passagens de código, segurança e fluxos de produto.

## Uso

Copie os arquivos `.toml` desejados para `.codex/agents/` no projeto ou `~/.codex/agents/` no perfil do usuário, conforme as [instruções de instalação do projeto de origem](https://github.com/VoltAgent/awesome-codex-subagents/blob/9abe3279a0aa4ee518381af800ca1062398f5433/README.md#installation). Depois, atualize a sessão do Codex e solicite explicitamente a delegação ao agente pelo nome.

Coleta em 12/11/2026 · [Revisão de origem](https://github.com/VoltAgent/awesome-codex-subagents/commit/9abe3279a0aa4ee518381af800ca1062398f5433) · [Licença MIT](LICENSE).

## Índice da pasta

- [Backend](Backend/README.md) — Subagentes para APIs, implementação de serviços, banco de dados, desempenho e qualidade.
- [Base](Base/README.md) — Subagentes para análise de código, arquitetura, revisão, documentação de referência e segurança.
- [DebugTests](DebugTests/README.md) — Subagentes para investigação de falhas e automação de testes.
- [Documentação](Documenta%C3%A7%C3%A3o/README.md) — Subagentes para documentação técnica, APIs e READMEs.
- [Frontend](Frontend/README.md) — Subagentes para interfaces, acessibilidade, testes de navegação, aplicações móveis e arquitetura de serviços.
- [Outros](Outros/README.md) — Subagentes para contexto, síntese, infraestrutura, containers, Git e revisão aprofundada.
- [Refatoração](Refatora%C3%A7%C3%A3o/README.md) — Subagentes para refatoração, modernização e gestão de dependências.
- [LICENSE](LICENSE)

## Navegação

[Voltar ao índice da pasta anterior](../README.md)
