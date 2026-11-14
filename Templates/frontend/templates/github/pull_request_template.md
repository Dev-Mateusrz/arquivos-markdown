<!--
Template reutilizável. Copie para `.github/pull_request_template.md` na raiz do
repositório, substitua os {{PLACEHOLDERS}} e apague este comentário.

Placeholders deste template:
  {{CMD_BUILD_BACKEND}}      comando de build do backend      (ex.: dotnet build MeuSistema/MeuSistema.csproj --configuration Release)
  {{CMD_TEST_BACKEND}}       comando de teste do backend       (ex.: dotnet test MeuSistema.Tests/MeuSistema.Tests.csproj --configuration Release)
  {{CMD_BUILD_FRONTEND}}     comando opcional de build do frontend (ex.: npm run build)
  {{CMD_LINT_FRONTEND}}      comando opcional de lint do frontend  (ex.: npm run lint)
  {{SHELL_PADRAO}}           linguagem do bloco de código dos comandos executados (ex.: powershell, bash)
  {{BRANCH_DESENVOLVIMENTO}} branch base para a qual todo PR aponta na regra geral (ex.: develop)
  {{BRANCH_PRODUCAO}}        branch de produção usada na exceção de hotfix (ex.: main)

Após a cópia e inclusão na default branch, o GitHub oferece este template
ao abrir novos PRs no projeto consumidor. Ele é
deliberadamente mais enxuto que o modelo de PR do CLAUDE.md/CONTRIBUTING.md:
aqui é o time humano preenchendo rápido; lá é o texto de referência completo.
Mantenha os dois compatíveis nos itens essenciais (branch de destino, o que
testar, checklist de segredos).
-->

## Resumo

<!--
Descreva em poucas linhas o que muda, por que a mudança é necessária e o
resultado esperado. Inclua o link ou a chave da issue/ticket relacionado.
Para encerrar uma issue do GitHub, use Closes #<número>; o encerramento automático
pela descrição exige merge na default branch. Para apenas referenciar uma tarefa,
use Refs #<número> ou a URL do ticket externo.
-->

## Tipo de mudança

<!-- Marque o tipo predominante da alteração. -->

- [ ] Feature
- [ ] Bugfix
- [ ] Hotfix
- [ ] Refactor
- [ ] Documentação
- [ ] Configuração/infra

## Como testar

<!--
Informe pré-requisitos, dados fictícios, passos e resultado esperado para o revisor
reproduzir o cenário. Registre os comandos realmente executados, os resultados
obtidos e as verificações pendentes. Ajuste o bloco abaixo ao que foi validado.
Para mudanças de UI, inclua capturas ou vídeo do comportamento alterado.
-->

- [ ] Validei o fluxo principal alterado e os cenários de erro aplicáveis.

```{{SHELL_PADRAO}}
# Backend
{{CMD_BUILD_BACKEND}}
{{CMD_TEST_BACKEND}}

# Frontend (se aplicável)
# {{CMD_BUILD_FRONTEND}}
# {{CMD_LINT_FRONTEND}}
```

<!-- Se não foram criados ou atualizados testes unitários, justifique em texto. -->

## Cobertura da mudança

<!--
Descreva quais regras de negócio, validações/permissões e contratos ou mapeamentos
de dados foram cobertos pelos testes. Aponte os cenários ou arquivos relevantes.
Se a mudança for apenas documental/configuração sem comportamento, informe que
a cobertura de comportamento não se aplica e registre a validação pertinente.
-->

## Banco de dados

- [ ] Não altera banco
- [ ] Altera modelo/migration
- [ ] Precisa de seed ou ajuste manual

<!-- Se houver alteração, detalhe a migration, o seed ou o ajuste manual, a ordem
de execução e os cuidados de compatibilidade e reversão. -->

## Variáveis de ambiente

- [ ] Não adiciona variáveis
- [ ] Adiciona/altera variáveis

<!-- Se houver alteração, informe os nomes das variáveis, sua finalidade e os
ambientes afetados. Não inclua valores sensíveis; indique onde configurá-las. -->

## Checklist do autor

<!-- Marque somente após verificar. Siga a exceção documentada para hotfixes. -->

- [ ] A origem da branch e o destino do PR seguem o fluxo de `{{BRANCH_DESENVOLVIMENTO}}` ou a exceção de hotfix documentada.
- [ ] Não inclui chaves, senhas ou dados sensíveis
- [ ] Não inclui arquivos temporários, logs ou dumps locais

<!--
Como adaptar este template a um novo projeto (apague este bloco):
1. Substitua os placeholders do cabeçalho.
2. Se o projeto tiver frontend, preencha e descomente os comandos opcionais
   de build e lint. Mantenha-os alinhados ao CLAUDE.md; se não se aplicarem,
   remova as linhas opcionais e seus placeholders.
3. Documente a exceção de hotfix no CONTRIBUTING.md e ajuste o item de branches:
   hotfix sai de `{{BRANCH_PRODUCAO}}`, não de `{{BRANCH_DESENVOLVIMENTO}}`.
4. Configure build, testes e validação de Conventional Commits no CI e exija os
   checks aplicáveis nas regras de proteção. Este template não executa essas
   verificações; a descrição registra o contexto e as evidências para o revisor.
-->
