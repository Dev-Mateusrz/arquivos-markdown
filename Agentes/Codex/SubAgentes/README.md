# Subagentes Codex

Seleção de 35 subagentes do [VoltAgent/awesome-codex-subagents](https://github.com/VoltAgent/awesome-codex-subagents), agrupados conforme as pastas deste repositório.

## Codex-Base

- [architect-reviewer](Codex-Base/architect-reviewer.toml) — Revisa arquitetura e dependências ao avaliar mudanças estruturais.
- [code-mapper](Codex-Base/code-mapper.toml) — Localiza arquivos e fluxos de execução antes de alterar código desconhecido.
- [code-reviewer](Codex-Base/code-reviewer.toml) — Avalia clareza, complexidade e manutenção de módulos e implementações.
- [docs-researcher](Codex-Base/docs-researcher.toml) — Pesquisa documentação para esclarecer APIs, versões e limitações técnicas.
- [reviewer](Codex-Base/reviewer.toml) — Revisa diffs e PRs para encontrar bugs, regressões e testes ausentes.
- [security-auditor](Codex-Base/security-auditor.toml) — Audita segurança em autenticação, permissões, entradas e tratamento de segredos.

## Codex-Backend

- [api-designer](Codex-Backend/api-designer.toml) — Define contratos, esquemas e erros antes de criar ou alterar APIs.
- [backend-developer](Codex-Backend/backend-developer.toml) — Implementa funcionalidades e corrige falhas em serviços e APIs.
- [database-optimizer](Codex-Backend/database-optimizer.toml) — Investiga lentidão no banco e propõe melhorias em consultas e índices.
- [performance-engineer](Codex-Backend/performance-engineer.toml) — Investiga gargalos de latência, recursos, renderização e escalabilidade.
- [qa-expert](Codex-Backend/qa-expert.toml) — Planeja cenários de teste e critérios de aceite para funcionalidades e releases.
- [sql-pro](Codex-Backend/sql-pro.toml) — Cria e revisa consultas SQL, transações e migrações de banco.

## Codex-Frontend

- [accessibility-tester](Codex-Frontend/accessibility-tester.toml) — Verifica acessibilidade de componentes e fluxos, incluindo teclado, foco e semântica.
- [anti-ui-slop-reviewer](Codex-Frontend/anti-ui-slop-reviewer.toml) — Revisa interfaces para identificar padrões genéricos e desvios do design system.
- [browser-debugger](Codex-Frontend/browser-debugger.toml) — Reproduz falhas no navegador e analisa console, rede e comportamento da interface.
- [design-bridge](Codex-Frontend/design-bridge.toml) — Transforma um DESIGN.md em orientações para implementar telas fiéis ao design.
- [frontend-developer](Codex-Frontend/frontend-developer.toml) — Implementa telas, componentes, estados e integrações com APIs.
- [microservices-architect](Codex-Frontend/microservices-architect.toml) — Define limites e contratos entre serviços em sistemas distribuídos.
- [mobile-developer](Codex-Frontend/mobile-developer.toml) — Implementa e depura aplicativos mobile, considerando navegação, permissões e conectividade.
- [ui-ux-tester](Codex-Frontend/ui-ux-tester.toml) — Testa jornadas e interações da interface e registra defeitos reproduzíveis.

## Codex-Refatoração

- [dependency-manager](Codex-Refatoração/dependency-manager.toml) — Revisa atualizações, compatibilidade, lockfiles e riscos de dependências.
- [legacy-modernizer](Codex-Refatoração/legacy-modernizer.toml) — Planeja migrações graduais de código e tecnologias legadas.
- [refactoring-specialist](Codex-Refatoração/refactoring-specialist.toml) — Reorganiza código para melhorar manutenção sem alterar seu comportamento.

## Codex-Documentação

- [api-documenter](Codex-Documentação/api-documenter.toml) — Documenta APIs para consumidores, com contratos, autenticação, erros e exemplos reais.
- [documentation-engineer](Codex-Documentação/documentation-engineer.toml) — Cria e atualiza guias técnicos de instalação, desenvolvimento e operação.
- [readme-generator](Codex-Documentação/readme-generator.toml) — Cria e organiza READMEs com informações verificadas no repositório.

## Codex-DebugTests

- [debugger](Codex-DebugTests/debugger.toml) — Investiga a causa de bugs e valida correções em falhas complexas ou intermitentes.
- [error-detective](Codex-DebugTests/error-detective.toml) — Analisa logs e exceções para identificar a origem provável de uma falha.
- [test-automator](Codex-DebugTests/test-automator.toml) — Implementa testes automatizados e cobertura contra regressões.

## Codex-Outros

- [context-manager](Codex-Outros/context-manager.toml) — Prepara contexto e restrições do projeto antes de delegar tarefas.
- [devops-engineer](Codex-Outros/devops-engineer.toml) — Configura pipelines de CI/CD, ambientes e automações de entrega.
- [docker-expert](Codex-Outros/docker-expert.toml) — Revisa Dockerfiles, otimiza imagens e investiga falhas em containers.
- [git-workflow-manager](Codex-Outros/git-workflow-manager.toml) — Orienta fluxos de branches, PRs, merges, releases e hotfixes.
- [knowledge-synthesizer](Codex-Outros/knowledge-synthesizer.toml) — Consolida resultados de vários agentes, destacando conclusões e divergências.
- [ponder-reviewer](Codex-Outros/ponder-reviewer.toml) — Faz revisões aprofundadas em múltiplas passagens de código, segurança e fluxos de produto.

## Uso

Conforme as [instruções do projeto de origem](https://github.com/VoltAgent/awesome-codex-subagents/blob/9abe3279a0aa4ee518381af800ca1062398f5433/README.md#installation), copie os `.toml` desejados para `.codex/agents/` no projeto ou `~/.codex/agents/` no perfil do usuário. Atualize a sessão do Codex e solicite explicitamente a delegação ao agente escolhido.

Coleta: 12/11/2026 · [Revisão de origem](https://github.com/VoltAgent/awesome-codex-subagents/commit/9abe3279a0aa4ee518381af800ca1062398f5433) · [Licença MIT](LICENSE).
