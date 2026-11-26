# Padrão de pull requests

> **Gatilho** — Aplique esta regra antes de preparar, abrir, atualizar ou revisar um pull request (PR).

## Proibições

- NUNCA abra ou atualize um PR, envie commits ao remoto ou execute merge sem autorização explícita para a ação. Um pedido de rascunho autoriza apenas a preparação do conteúdo.
- NUNCA misture mudança de comportamento com refatoração estrutural, renomeações ou ajustes independentes. Mantenha no mesmo PR as alterações necessárias para validar a entrega como um todo.
- NUNCA publique credenciais, arquivos `.env` com valores reais, dados pessoais ou evidências que exponham informações sensíveis. Remova assinaturas automáticas de IA da descrição.
- NUNCA apresente como concluídos testes, verificações do CI ou revisões que ainda estejam pendentes ou cujos resultados não foram conferidos.

## Formato e template

Use um título no formato abaixo e siga as regras de assunto de [commits e branches](padrao-commit-branch.md). SE houver quebra de compatibilidade, ENTÃO inclua `!` antes dos dois-pontos e descreva no PR quem é afetado e como migrar.

```text
<tipo>[(<escopo>)][!]: <descrição no imperativo>
```

Os colchetes indicam partes opcionais. O título deve funcionar como assunto do commit final quando houver squash merge.

SE o repositório tiver um template oficial, ENTÃO preencha-o. Caso contrário, use o modelo abaixo. Vincule a issue real quando houver. Use um comando de encerramento automático somente se o fechamento fizer parte da entrega e a integração do projeto o suportar.

```markdown
## Resumo e motivação
<Em 2 a 4 linhas, descreva o problema, a mudança e o resultado esperado.>

**Issue vinculada** — <Chave ou link, quando houver.>

## Alterações e impacto
- <Componentes, regras, contratos ou configurações afetados.>
- <Quebra de compatibilidade, migration ou ordem de deploy, quando aplicável.>

## Como validar
1. <Informe ambiente, pré-requisitos e dados de teste.>
2. <Execute a ação e confira o resultado esperado.>

**Verificações executadas** — <Comandos, cenários cobertos e resultados observados.>

**Pendências** — <Verificações ainda não concluídas e respectivos motivos.>

## Evidências
- <Capturas, vídeo, exemplos de contrato ou links de execução aplicáveis.>
```

- SE a interface mudar, ENTÃO anexe capturas de antes e depois ou um vídeo curto do fluxo afetado.
- SE o contrato de API mudar, ENTÃO documente entradas, saídas ou erros alterados e inclua um exemplo ou evidência de teste.
- SE houver migration, alteração de configuração ou deploy coordenado, ENTÃO indique os ambientes afetados, a ordem de aplicação e o procedimento de reversão quando aplicável. Para variáveis de ambiente, informe nomes e finalidades e preserve os valores sensíveis.

## Exemplos

| Resultado | Campo | Exemplo | Motivo |
| --- | --- | --- | --- |
| Certo | Título | `fix(exportacao): corrige CSV de lista vazia` | Indica o tipo, o escopo e a correção. |
| Certo | Como validar | Com a lista vazia, selecione **Exportar CSV**. Abra o arquivo baixado e confirme que ele contém apenas o cabeçalho. | Dá ao revisor uma ação e um resultado reproduzível. |
| Errado | Título | `Ajustes finais` | O título não indica o tipo nem a mudança. |
| Errado | Como validar | `Testado. Tudo certo.` | Faltam os passos, as verificações executadas e os resultados. |

## Fluxo passo a passo

### Preparar ou atualizar o PR

1. Confirme o repositório, as branches de origem e destino, o template e a issue vinculada. Use a branch de destino definida pelo fluxo do projeto. Neste repositório, o destino padrão é `main`. SE estiver atualizando um PR, ENTÃO leia a descrição atual e preserve as informações fora do escopo da atualização.
2. Execute `git status --short --branch`. Substitua `<base>` e `<origem>` pelas referências atualizadas do destino e da origem. Confira os commits com `git log --oneline <base>..<origem>` e revise `git diff --stat <base>...<origem>` e `git diff <base>...<origem>`. Retire do PR arquivos alheios, código morto, logs temporários e dados sensíveis. Prefira diffs de até 400 linhas alteradas. SE o diff for maior e puder ser dividido, ENTÃO proponha PRs menores em sequência e explicite as dependências.
3. Execute `git diff --check <base>...<origem>` e os checks aplicáveis à versão de origem, como build, lint, typecheck, testes e varredura de segredos, conforme a configuração do projeto. Registre comandos, resultados e pendências. SE houver mudança de comportamento, ENTÃO valide o fluxo principal e os casos de erro ou borda pertinentes. SE houver código assistido por IA, ENTÃO confira as decisões e os resultados antes de solicitar revisão.
4. Preencha o título e a descrição com base no diff e nos resultados observados. SE o pedido for só para preparar ou a publicação não estiver autorizada, ENTÃO entregue o rascunho. Caso contrário, abra ou atualize o PR. Use **Draft** se houver trabalho ou validações pendentes e a plataforma permitir. Registre as pendências, solicite revisão após as verificações exigidas para essa etapa e confirme o destino, o estado e o link do PR.

### Revisar o PR

1. Leia a descrição, a issue vinculada e os critérios de aceite disponíveis antes do diff. Identifique o comportamento e o escopo esperados.
2. Compare o diff com esse escopo. Confira os checks, a cobertura dos casos de borda e os impactos de segurança, compatibilidade e implantação aplicáveis. Examine também as decisões que dependem de código gerado por IA e confirme que as evidências permitem verificá-las.
3. Relate cada achado com arquivo e linha, condição em que ocorre e impacto. Indique as verificações pendentes e as limitações da revisão.
