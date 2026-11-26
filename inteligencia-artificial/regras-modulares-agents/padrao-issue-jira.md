# Padrão de issues no Jira

> **Gatilho** — Aplique esta regra antes de redigir, criar ou atualizar o conteúdo de uma issue no Jira.

## Proibições

- NUNCA crie ou atualize uma issue no Jira sem autorização explícita do usuário para a operação. Um pedido de rascunho autoriza apenas a preparação do conteúdo.
- NUNCA invente projeto, tipo, prioridade, labels, responsável, sprint ou prazo. Use os valores confirmados e as opções disponíveis no projeto.
- NUNCA registre hipótese como causa confirmada, inclua segredos ou dados pessoais em evidências, ou marque uma verificação do DoD como concluída sem evidência.
- NUNCA use título genérico ou critério de aceite sem resultado observável.

## Formato e templates

### Tipo e campos do Jira

| SE a issue descreve | ENTÃO use |
| --- | --- |
| Uma iniciativa que reúne várias entregas | Épico. Registre o resultado esperado e relacione as entregas conhecidas. |
| Uma capacidade nova para o usuário ou consumidor | História. Descreva o valor entregue. |
| Um trabalho técnico ou operacional com resultado próprio | Tarefa. Descreva a entrega verificável. |
| Um comportamento que diverge de uma regra existente | Bug. Inclua o bloco de reprodução. |
| Uma parte técnica de uma entrega já registrada | Subtarefa. Vincule-a à issue pai. |

- **Projeto e tipo** — Use a chave real do projeto e o nome de tipo habilitado nele.
- **Título** — Escreva uma frase curta com a ação e o resultado ou com a correção e o sintoma. Inclua prefixo de área somente se o projeto o adotar. Use o idioma do projeto ou português do Brasil como padrão.
- **Prioridade e labels** — Defina a prioridade pelo impacto e pela urgência. Use as labels do projeto que identifiquem a camada ou o domínio.
- **Responsável, sprint, prazo e vínculos** — Preencha conforme o padrão confirmado ou o compromisso informado. Use os campos nativos do Jira para issue pai e dependências. SE faltarem valores obrigatórios, ENTÃO solicite apenas os dados faltantes.

### Descrição base

```markdown
## Contexto e objetivo
<Em 2 a 3 linhas, descreva o problema, quem é afetado e o resultado esperado.>

## Escopo técnico
<Quando aplicável, indique camadas, componentes, contratos, regras e referências confirmadas.>

## Critérios de aceite

### <Nome do cenário>
- **Dado que** <estado inicial ou pré-condição>
- **Quando** <ação executada pelo usuário ou sistema>
- **Então** <resultado observável e verificável>

## Definition of Done (DoD)
- [ ] <Verificação exigida pelo time, com a evidência esperada.>
```

- Omita o escopo técnico quando ele não se aplicar. Para histórias e tarefas, mire 3 a 5 cenários. Cubra o fluxo principal e os casos de erro ou borda que se aplicarem. Para épicos, registre resultados verificáveis no nível da iniciativa e detalhe os cenários nas issues filhas.
- SE uma história ou tarefa não couber em uma sprint ou passar de 10 critérios de aceite, ENTÃO proponha dividi-la em entregas verificáveis. Busque recortes de 1 a 3 dias quando fizer sentido para o time.
- Preencha o DoD com as verificações do projeto, como build, lint, testes, revisão de PR e homologação. Inclua revisão humana de casos de borda e segurança em código assistido por IA quando o time a exigir.

### Bloco obrigatório para bug

Insira após **Contexto e objetivo**. Registre ambiente e versão quando conhecidos e vincule evidências sanitizadas, se disponíveis.

```markdown
## Passos para reproduzir
1. <Acesse a tela, rota ou operação afetada.>
2. <Informe as pré-condições e execute a ação com dados seguros.>

## Resultado atual
<Descreva o comportamento observado e a mensagem ou código de erro, se houver.>

## Resultado esperado
<Descreva o comportamento previsto pela regra existente.>
```

- Inclua um cenário de aceite que repita a ação que expunha o defeito e verifique o resultado esperado. Registre a causa quando confirmada. No DoD, indique como comprovar a correção e inclua um teste automatizado de regressão quando aplicável.

## Exemplos

| Resultado | Campo | Exemplo | Motivo |
| --- | --- | --- | --- |
| Certo | Título de história | `Permitir filtrar solicitações por status` | Identifica a ação e a capacidade entregue. |
| Certo | Critério de aceite de bug | Dado que a lista está vazia. Quando o usuário exporta em CSV. Então o arquivo contém apenas a linha de cabeçalho. | Define uma entrada, uma ação e uma saída verificável. |
| Errado | Título | `Ajustes gerais` | O título não identifica a entrega. |
| Errado | Critério de aceite | `Então a exportação deve funcionar corretamente` | Falta um resultado observável para o teste. |

## Fluxo passo a passo

1. Identifique a operação solicitada, o projeto de destino e, em uma atualização, a chave da issue. Consulte as instruções do projeto e os campos disponíveis para o tipo aplicável.
2. Escolha o tipo pela tabela. SE for criar uma issue, ENTÃO procure pelo objetivo ou sintoma no projeto e sinalize issues equivalentes antes de publicar. SE for atualizar, ENTÃO leia a issue atual e preserve os campos fora do escopo.
3. Preencha o título, os campos e a descrição. Para bugs, inclua reprodução, resultado atual e resultado esperado. Valide se cada critério permite observar um resultado e se o DoD corresponde às verificações do time.
4. SE o pedido for apenas de redação, faltar autorização ou houver campos obrigatórios pendentes, ENTÃO entregue o rascunho e indique as pendências, se houver. Caso contrário, crie ou atualize a issue e confirme o resultado com a chave e o link retornados pelo Jira.
