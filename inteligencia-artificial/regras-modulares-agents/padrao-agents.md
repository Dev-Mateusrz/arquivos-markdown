# Padrão de AGENTS.md e delegação

> **Gatilho** — Leia esta regra antes de criar, revisar ou reorganizar um `AGENTS.md`. Consulte o fluxo de delegação antes de usar subagentes quando o `AGENTS.md` aplicável indicar este módulo.

## Proibições

- NUNCA carregue todos os módulos, catálogos ou arquivos `.toml` por padrão. Leia os módulos acionados pela tarefa e os trechos necessários para executá-la.
- NUNCA duplique no `AGENTS.md` os templates e procedimentos dos módulos. Mantenha na raiz as regras aplicáveis a todo o repositório e os gatilhos para consultar cada módulo.
- NUNCA delegue por iniciativa própria. Exija pedido explícito do usuário ou instrução aplicável, benefício claro e escopo delimitado.
- NUNCA execute mais de dois subagentes simultâneos. Atribua responsabilidades distintas e separe os arquivos que cada agente pode alterar. Subagentes NUNCA criam outros agentes.
- NUNCA execute simultaneamente agentes do mesmo grupo abaixo sobre o mesmo escopo, salvo pedido explícito do usuário para essa sobreposição.
  - `reviewer`, `code-reviewer`, `ponder-reviewer`
  - `debugger`, `error-detective`, `browser-debugger`
  - `api-documenter`, `documentation-engineer`, `readme-generator`
  - `architect-reviewer`, `microservices-architect`
  - `database-optimizer`, `sql-pro`, `performance-engineer`
  - `accessibility-tester`, `ui-ux-tester`, `anti-ui-slop-reviewer`
  - `code-mapper`, `context-manager`
- NUNCA repita uma análise ou aumente o esforço de raciocínio automaticamente. Encaminhe ao agente principal as evidências e as lacunas relevantes.

## Formato e templates

Use este molde para o `AGENTS.md`. Escreva apenas as linhas necessárias, com até 120 linhas no arquivo principal. Use os caminhos reais, relativos ao diretório desse `AGENTS.md`.

```markdown
# Instruções de <projeto ou área>

## Escopo
- <Diretórios cobertos e instruções locais aplicáveis, se existirem.>

## Regras sempre ativas
- <Restrições e permissões que se aplicam a todo o escopo.>

## Regras por atividade

| Quando | Leia antes de agir |
| --- | --- |
| <Ação concreta que aciona a consulta> | `<caminho do módulo>` |
```

Use este molde em cada atribuição a um subagente.

```text
Objetivo: <resultado esperado>
Escopo: <arquivos e símbolos a consultar ou alterar e responsabilidade atribuída>
Restrições: <instruções obrigatórias, permissões e limites da tarefa>
Conclusão: <critério verificável e caminho da entrega, quando houver artefato>
```

## Exemplos

| Resultado | Situação | Conduta |
| --- | --- | --- |
| Certo | O agente vai criar uma branch | O `AGENTS.md` indica a leitura de `.agents/padrao-commit-branch.md` antes da criação |
| Certo | O usuário pede duas análises independentes | Atribua a cada subagente uma responsabilidade, os arquivos relevantes e um critério de conclusão |
| Errado | A tarefa pede uma correção pequena e localizada | Acionar um subagente para uma revisão de rotina sem pedido ou instrução aplicável |
| Errado | O usuário pede revisão de um diff sem solicitar análises sobrepostas | Acionar `reviewer` e `code-reviewer` simultaneamente sobre o mesmo diff |

## Fluxo passo a passo

### Estruturar ou revisar o AGENTS.md

1. Identifique a raiz do repositório e o escopo da tarefa. Leia os `AGENTS.md` aplicáveis da raiz até a área afetada e mantenha as instruções específicas no diretório que elas cobrem.
2. SE uma regra vale para todo o escopo, ENTÃO mantenha-a em **Regras sempre ativas**. SE a regra só se aplica a uma atividade, ENTÃO indique na tabela quando consultar o módulo que a contém.
3. Confirme que cada gatilho descreve uma ação concreta, que cada caminho aponta para um arquivo existente e que o arquivo principal ficou dentro do limite de linhas.

### Decidir e conduzir a delegação

1. Resolva tarefas pequenas no agente principal por padrão. SE o usuário pedir delegação explicitamente ou uma instrução aplicável a exigir, ENTÃO confirme o benefício e delimite a atribuição antes de delegar.
2. Selecione apenas o papel necessário. SE precisar consultar o catálogo humano, ENTÃO leia a entrada relevante em `~/.codex/agents/Agentes-Codex.md`. Use esforço `low` para busca ou síntese, `medium` para implementação ou rotina e `high` apenas para análise crítica.
3. Envie a atribuição no formato acima. Use contexto mínimo se a ferramenta permitir, incluindo as instruções obrigatórias. Respeite as permissões da sessão e preserve as alterações de outros agentes e do usuário.
4. Reutilize os resultados já disponíveis e encerre a atribuição quando o critério de conclusão for atendido. Solicite ao subagente uma resposta de até 15 linhas e 200 palavras com escopo, achados ou resultado, referências, validação e limitações. Oriente-o a preservar achados críticos e declarar lacunas de cobertura. SE houver artefato, ENTÃO peça ao subagente que salve a versão completa no arquivo atribuído e retorne o caminho com um resumo.
5. Consolide os resultados de forma breve no agente principal. SE uma atribuição autorizada precisar de contexto reutilizável, ENTÃO use `context-manager`. SE várias saídas extensas ou conflitantes justificarem uma chamada adicional autorizada, ENTÃO use `knowledge-synthesizer` e limite a síntese a 200 palavras.
