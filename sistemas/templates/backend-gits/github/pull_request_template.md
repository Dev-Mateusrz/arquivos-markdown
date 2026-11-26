<!--
Template reutilizável. Copie para `.github/pull_request_template.md` na raiz do
repositório, substitua os {{PLACEHOLDERS}} e apague este comentário.

Placeholders deste template:
  {{CMD_BUILD_BACKEND}}      comando de build do backend      (ex.: dotnet build MeuSistema/MeuSistema.csproj --configuration Release)
  {{CMD_TEST_BACKEND}}       comando de teste do backend       (ex.: dotnet test MeuSistema.Tests/MeuSistema.Tests.csproj --configuration Release)
  {{SHELL_PADRAO}}           linguagem do bloco de código dos comandos executados (ex.: powershell, bash)
  {{BRANCH_DESENVOLVIMENTO}} branch base para a qual todo PR aponta na regra geral (ex.: develop)

Este arquivo é o template padrão do GitHub — ele preenche a descrição sempre
que alguém abre um PR neste repositório, sem precisar copiar nada. Ele é
deliberadamente mais enxuto que o modelo de PR do CLAUDE.md/CONTRIBUTING.md:
aqui é o time humano preenchendo rápido; lá é o texto de referência completo.
Mantenha os dois compatíveis nos itens essenciais (branch de destino, o que
testar, checklist de segredos).
-->

# Resumo

Descreva em poucas linhas o que este PR altera.

## Tipo de mudança

- [ ] Feature
- [ ] Bugfix
- [ ] Hotfix
- [ ] Refactor
- [ ] Documentação
- [ ] Configuração/infra

## Como testar

Explique os passos usados para validar a mudança.

- [ ] Rodei build local
- [ ] Rodei testes unitários
- [ ] Rodei testes automatizados adicionais, quando aplicável
- [ ] Validei o fluxo principal alterado

Comandos executados:

```{{SHELL_PADRAO}}
# Backend
{{CMD_BUILD_BACKEND}}
{{CMD_TEST_BACKEND}}
```

Se não foram criados testes unitários, explique o motivo:

```text

```

## Cobertura da mudança

- [ ] Cobre regra de negócio alterada
- [ ] Cobre validação/permissão alterada
- [ ] Cobre contrato ou mapeamento de dados alterado
- [ ] Não se aplica, pois a mudança é somente documental/configuração sem comportamento

## Banco de dados

- [ ] Não altera banco
- [ ] Altera modelo/migration
- [ ] Precisa de seed ou ajuste manual

Detalhes, se houver:

## Variáveis de ambiente

- [ ] Não adiciona variáveis
- [ ] Adiciona/altera variáveis

Detalhes, se houver:

## Checklist do autor

- [ ] A branch saiu de `{{BRANCH_DESENVOLVIMENTO}}`
- [ ] O PR aponta para `{{BRANCH_DESENVOLVIMENTO}}`
- [ ] O título do PR está claro
- [ ] Commits seguem Conventional Commits
- [ ] Não inclui chaves, senhas ou dados sensíveis
- [ ] Não inclui arquivos temporários, logs ou dumps locais

<!--
Como adaptar este template a um novo projeto (apague este bloco):
1. Substitua os placeholders do cabeçalho.
2. Se o projeto tiver frontend, acrescente uma segunda linha ao bloco de
   comandos (npm run build / npm run lint), no mesmo padrão de
   {{CMD_BUILD_FRONTEND}} / {{CMD_LINT_FRONTEND}} usado no CLAUDE.md.
3. Se hotfix é uma exceção de branch de destino no projeto (ver
   CONTRIBUTING.md), acrescente um item ao checklist perguntando qual regra
   se aplica — hotfix sai de `{{BRANCH_PRODUCAO}}`, não de `{{BRANCH_DESENVOLVIMENTO}}`.
-->
