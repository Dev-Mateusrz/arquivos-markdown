# Modelos de Issue — {{CHAVE_PROJETO_TRACKER}}

> **Template reutilizável.** Copie para `docs/JIRA_TAREFAS.md` (ou cole direto na descrição da issue), substitua os `{{PLACEHOLDERS}}` e apague os blocos `<!-- guia: ... -->`, os exemplos preenchidos e a seção "Como adaptar" ao final.
>
> Este arquivo é a fonte dos modelos de descrição referenciados na seção "Issues no rastreador" do `CLAUDE.md`. Quando um modelo mudar aqui, atualize a referência lá.

## Placeholders deste template

| Placeholder | Significado | Exemplo |
|---|---|---|
| `{{CHAVE_PROJETO_TRACKER}}` | Chave do projeto no rastreador | `SUBG-AGENDA` |
| `{{PREFIXO_ISSUE_MAIUSCULO}}` | Prefixo do código da issue | `SA` |
| `{{RESPONSAVEL_PADRAO}}` | Pessoa a quem toda issue é atribuída | `Nome Sobrenome` |
| `{{URL_BASE_TRACKER}}` | URL base para montar links de issue | `https://org.atlassian.net/browse` |
| `{{PREFIXO_ISSUE}}` | Prefixo em minúsculo, usado em branch | `sa` |

---

## Como escolher o modelo

| Situação | Tipo no rastreador | Modelo |
|---|---|---|
| Algo já existe e está se comportando errado | `Bug` | [Modelo A — Bug](#modelo-a--bug) |
| Algo novo precisa existir, ou algo existente precisa mudar de propósito | `Tarefa` | [Modelo B — Tarefa](#modelo-b--tarefa) |
| Recorte de uma tarefa maior já criada | `Subtarefa` | Modelo B, com escopo reduzido e link para a issue pai |
| Investigação sem entrega de código garantida | `Tarefa` | Modelo B, com "Critérios de aceite" descrevendo o **artefato de decisão** esperado, não o código |

A diferença prática entre os dois modelos: **Bug parte de uma evidência** (o sistema faz X, deveria fazer Y) e a descrição converge para a causa. **Tarefa parte de uma necessidade** (alguém precisa de X) e a descrição diverge para escopo, aceite e teste.

Se você não consegue escrever o campo `Sintoma` sem usar a palavra "deveria ter", provavelmente não é um bug — é uma tarefa.

---

## Campos padrão (aplicam-se aos dois modelos)

- **Tipo:** conforme a tabela acima.
- **Prioridade:** definida pela dificuldade/complexidade da tarefa:
  - `Highest`: mudança estrutural ou de alto risco, várias camadas, alto impacto
  - `High`: mudança relevante, exige atenção e cuidado, mas escopo definido
  - `Medium`: mudança padrão, escopo claro, complexidade moderada
  - `Low`: mudança pequena, baixo risco, baixa complexidade
- **Responsável:** sempre {{RESPONSAVEL_PADRAO}}. Na dúvida entre contas homônimas, criar **sem responsável** e avisar — nunca adivinhar.
- **Categorias (labels):** reaproveitar labels já existentes no projeto (ex: `backend`, `frontend`, `infra`, `documentacao`). Criar uma nova só se nenhuma existente cobrir o caso.
- **Data limite:** **sempre perguntar** se a issue tem prazo antes de criá-la. Nunca definir uma data por conta própria, nunca pular a pergunta.
- **Card relacionado:** quando a issue compartilha branch, causa-raiz ou entrega com outra, linkar explicitamente.

### Título da issue

Descrição curta e direta, no infinitivo ou como afirmação do defeito. O código `{{PREFIXO_ISSUE_MAIUSCULO}}-XX` é gerado pelo rastreador e **não** entra no texto.

```text
Bug:     dashboard anual retorna sempre Dezembro em vez do último mês com dados
Tarefa:  criar fluxo de agendamento recorrente para administradores
```

---

## Modelo A — Bug

<!-- guia: use quando existe um comportamento observável e errado. Se você ainda não sabe a causa, escreva `Causa` como "Sob investigação" e preencha depois — não invente. -->

````markdown
## Sintoma
[O que acontece hoje, de forma verificável: rota, entrada, saída observada, saída esperada]
[Exemplo concreto que reproduz o problema, com valores reais]

## Causa
[Onde está o defeito — arquivo, classe, método ou consulta]

```{{LINGUAGEM}}
[trecho mínimo de código que contém o defeito, com um comentário apontando a linha]
```

[Por que a lógica atual está errada — qual premissa foi assumida e não se sustenta]

## Fix
[A correção proposta, em uma ou duas frases diretas]

* [Caso 1 — entrada → resultado esperado]
* [Caso 2 — entrada → resultado esperado]
* [Caso de borda — entrada → resultado esperado, incluindo o comportamento atual que deve ser preservado]

## Card relacionado
[{{PREFIXO_ISSUE_MAIUSCULO}}-XX]({{URL_BASE_TRACKER}}/{{PREFIXO_ISSUE_MAIUSCULO}}-XX) — [relação: mesma branch, mesma causa-raiz, bloqueia, é bloqueado por]
````

### Seções opcionais do Modelo A

Acrescente apenas quando agregarem informação que o revisor não tem:

- **`## Como reproduzir`** — quando o sintoma não é óbvio a partir de uma chamada única. Passos numerados.
- **`## Impacto`** — quando o bug afeta produção, dados ou usuários reais. Diga quem é afetado e desde quando.
- **`## Workaround`** — quando existe contorno manual em uso enquanto o fix não sai.

### Exemplo preenchido (Modelo A)

<!-- guia: apague este exemplo ao adaptar o template. Ele existe só para calibrar o nível de detalhe esperado. -->

> **Sintoma** — `GET /api/dashboard/profissionais?ano=2026` retorna os dados de Dezembro/2026 (ou 404 se Dezembro não existe), em vez do último mês com dados dentro de 2026. Se 2026 só tem importações de Jan a Maio, o esperado é mostrar Maio/2026 — não forçar Dezembro.
>
> **Causa** — `ObterDashboardUseCase.ResolverJanela`, caso "Ano só": o código crava `new DateOnly(ano, 12, 1)` como data de referência. Dezembro é assumido como "fim do ano", mas o ano pode estar incompleto (ano corrente) ou ter buracos.
>
> **Fix** — No caso "Ano só" (sem Mês, sem dimensão): buscar `MAX(mes_competencia) WHERE year = @ano` e usar como `dataRef`. A série continua Jan–Dez. Ano parcial (Jan–Mai) → `dataRef = Mai`; ano completo → `dataRef = Dez` (comportamento atual preservado); ano sem dado → 404 via `ExisteSnapshotAsync`, já existente.
>
> **Card relacionado** — SP-79 / SP-80, mesma branch (`fix/SP-79-dashboard-filtros-temporais`).

Repare no que o exemplo faz e o template exige:

1. O **Sintoma** traz a chamada exata e um caso numérico. "Está retornando o mês errado" não seria suficiente.
2. A **Causa** aponta o método e cita o trecho, com comentário na linha do defeito. E, mais importante, nomeia a **premissa falsa** ("Dezembro é o fim do ano").
3. O **Fix** enumera os casos de borda, incluindo o que **não deve mudar**. Isso é o que impede que a correção vire uma regressão.

---

## Modelo B — Tarefa

<!-- guia: este é o modelo referenciado no CLAUDE.md. Mantenha os cabeçalhos exatamente com estes nomes — scripts e buscas no rastreador dependem deles. -->

````markdown
## Contexto
[Por que essa tarefa existe — qual problema ou lacuna motiva a mudança, e para quem]

## Objetivo
[O que a tarefa busca alcançar, de forma direta, em uma ou duas frases]

## Área afetada
* Front-end: [sim/não — o que muda]
* Back-end: [sim/não — o que muda]

## Escopo sugerido
* [item 1 — o que precisa ser construído ou alterado]
* [item 2]
* [item 3]

## Critérios de aceite
* [condição verificável que precisa ser verdadeira para considerar a tarefa concluída]
* [uma condição sobre o caminho feliz]
* [uma condição sobre o caminho de erro]
* [uma condição sobre quem NÃO deve conseguir fazer isso, quando houver permissão envolvida]
* [O PR informa quais testes foram criados ou executados]

## Testes esperados
* Back-end: [o que validar, por comportamento — não por arquivo]
* Back-end: [caso de conflito, erro ou borda]
* Front-end: [teste de componente/formulário, se houver infraestrutura de teste disponível]
* Front-end: [exibição de feedback de erro retornado pela API]

## Observações técnicas
[Decisão que precisa ser tomada ANTES da implementação, dependência de outra issue, risco conhecido, ou ponto de atenção sobre dados/migration]
````

### Exemplo preenchido (Modelo B)

<!-- guia: apague este exemplo ao adaptar o template. -->

> **Contexto** — Administradores precisam reservar a mesma sala repetidamente por um período (semanas ou meses), mantendo setor, propósito e demais informações principais.
>
> **Objetivo** — Criar fluxo de agendamento recorrente para administradores, gerando múltiplos agendamentos a partir de uma regra de repetição.
>
> **Área afetada** — Front-end: sim, controles de recorrência no fluxo administrativo. Back-end: sim, validar e criar múltiplos agendamentos com consistência transacional.
>
> **Escopo sugerido** — Escolha de frequência, período final e dados comuns; validação de conflito por ocorrência antes de confirmar; retorno ao front-end de quais ocorrências seriam criadas e quais teriam conflito; criação segura, evitando criação parcial sem feedback claro.
>
> **Critérios de aceite** — Admin cria a série; o sistema valida conflitos em todas as datas antes de concluir; o usuário recebe feedback claro quando alguma ocorrência não puder ser criada; dados principais são reaproveitados; **usuários comuns não acessam a funcionalidade**; o PR informa quais testes foram criados ou executados.
>
> **Testes esperados** — Back-end: geração das ocorrências por frequência/período; conflito em uma ou mais ocorrências; garantia de que a criação não fique parcial sem comportamento definido. Front-end: seleção de recorrência e envio do payload, se houver infra de teste; exibição de feedback de conflito.
>
> **Observações técnicas** — Definir antes da implementação se conflitos bloqueiam toda a série ou se o admin poderá criar apenas as ocorrências livres.

Repare no que o exemplo faz e o template exige:

1. **Critérios de aceite incluem uma negativa** ("usuários comuns não acessam"). Todo aceite que envolve permissão precisa dizer quem *não* pode.
2. **Testes esperados descrevem comportamento**, não arquivo. "Teste da geração das ocorrências por frequência" sobrevive a um refactor; "teste de `RecorrenciaService.cs`" não.
3. **Observações técnicas contém uma decisão em aberto**, não um detalhe de implementação. É o campo que impede alguém de começar a codar com a pergunta errada na cabeça.

---

## Regras de escrita

- **Idioma:** {{IDIOMA_PADRAO}}, tanto no título quanto na descrição.
- **Uma issue, um resultado.** Se os "Critérios de aceite" descrevem duas entregas que poderiam ir em PRs separados, são duas issues.
- **Sem estimativa disfarçada de escopo.** "Escopo sugerido" é sugestão; quem implementa pode divergir, desde que os critérios de aceite se mantenham.
- **Não escreva a solução no `Contexto`.** Contexto é o problema. Solução é `Escopo sugerido`.
- **Código só onde há defeito.** O Modelo A cita código porque a causa mora nele. O Modelo B normalmente não cita código nenhum — se citar, é sinal de que a tarefa já foi implementada na cabeça de quem escreveu.
- **Links de issue sempre com URL completa** no formato `[{{PREFIXO_ISSUE_MAIUSCULO}}-XX]({{URL_BASE_TRACKER}}/{{PREFIXO_ISSUE_MAIUSCULO}}-XX)`.
- **Branch derivada da issue** segue `<tipo>/{{PREFIXO_ISSUE}}-<id>-<descricao-curta-em-kebab-case>`, conforme o `CLAUDE.md`.

---

## Checklist antes de criar a issue

- [ ] O tipo está correto (Bug vs Tarefa) segundo o teste do "deveria ter"
- [ ] O título descreve o resultado ou o defeito, sem o código da issue
- [ ] A prioridade reflete complexidade, não urgência sentida
- [ ] O responsável é {{RESPONSAVEL_PADRAO}} (ou nenhum, com aviso)
- [ ] As labels reaproveitam as já existentes no projeto
- [ ] **O prazo foi perguntado explicitamente**, e não inferido
- [ ] Bug: o `Sintoma` tem um caso reproduzível com valores concretos
- [ ] Bug: o `Fix` diz o que **não** deve mudar
- [ ] Tarefa: os `Critérios de aceite` incluem o caminho de erro e, se houver permissão, a negativa
- [ ] Tarefa: `Observações técnicas` registra decisões pendentes antes da implementação
- [ ] Cards relacionados foram linkados nos dois sentidos

> **Regra de aprovação:** o conteúdo da issue deve ser exibido e aprovado antes da criação. Criar issue é ação com efeito externo — vale a mesma regra de `git push` e de abertura de PR descrita no `CLAUDE.md`.

---

## Como adaptar este template a um novo projeto

<!-- guia: apague esta seção inteira depois de preencher. -->

1. **Substitua os placeholders** da tabela do topo e apague a tabela.
2. **Apague os dois exemplos preenchidos.** Eles são calibragem, não conteúdo. Depois de a equipe criar 3 ou 4 issues boas, substitua-os por links para issues reais do próprio projeto — exemplo vivo envelhece melhor que exemplo escrito.
3. **Não renomeie os cabeçalhos do Modelo B** sem verificar o `CLAUDE.md`. Os dois arquivos precisam concordar, senão o agente gera issues fora do padrão.
4. **Ajuste "Área afetada"** ao número real de camadas. Projeto com worker, app mobile ou infra como código precisa de mais linhas; projeto só de backend precisa de menos.
5. **Se o rastreador não for o Jira**, o mapeamento é direto: Azure DevOps (Work Item/Bug), GitHub Issues (labels + templates em `.github/ISSUE_TEMPLATE/`) e Linear têm os mesmos campos com nomes próximos. Para GitHub, os Modelos A e B viram dois arquivos YAML de issue form.
6. **Mantenha o checklist curto.** Se ninguém marca os itens, o problema é o tamanho da lista, não a disciplina do time.
