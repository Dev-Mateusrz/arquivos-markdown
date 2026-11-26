# Modelos de uma feature

Criar uma pasta NNN-nome-da-feature em 02-features. Produzir somente o documento da etapa atual, seguindo as [instruções do projeto](AGENTS.md).

Os campos entre colchetes são instruções de preenchimento do modelo. Removê-los ou resolvê-los antes de apresentar um documento como pronto para revisão.

## Modelo de spec.md — Specify

### Identificação

- Título: [NNN — nome da feature].
- Status: [rascunho para revisão / aprovado, com referência à aprovação].
- Fontes: [links para o contexto aplicável].
- Dependências: [features ou capacidades necessárias].

### Objetivo e resultado esperado

[Problema específico, usuário e resultado observável.]

### Escopo e histórias

- US-NNN-01: Como [ator], quero [ação] para [benefício].
- [Listar as capacidades incluídas e os dados necessários.]

### Regras e requisitos

- REQ-NNN-01: QUANDO [evento], O SISTEMA DEVE [resultado observável].
- REQ-NNN-02: ENQUANTO [condição], O SISTEMA DEVE [comportamento].
- [Para regra permanente, usar O SISTEMA DEVE sem inventar um evento.]

Definir validações, limites, estados vazios, falhas relevantes e efeitos sobre regras compartilhadas. Especificar comportamento sem escolher bibliotecas ou endpoints nesta etapa.

### Critérios de aceite

- CA-NNN-01 → REQ-NNN-01: [cenário inicial, ação e resultado esperado].
- [Incluir caminho principal, entradas inválidas e exceções importantes.]

### Fora de escopo e pontos de revisão

[Limites desta feature e decisões pendentes que impedem o planejamento.]

## Modelo de design.md — Plan

### Identificação e decisões de entrada

[Feature, versão da spec aprovada, referências à arquitetura e decisões que sustentam o plano.]

### Solução proposta

[Responsabilidades de frontend e backend, dados, contratos e integrações necessárias. Justificar as escolhas.]

### Fluxos e estados

[Navegação, informações, componentes, acessibilidade, carregamento, vazio, sucesso e erros. Usar diagramas quando ajudarem.]

### Impacto e arquivos afetados

[Caminhos reais ou novos caminhos explicitamente planejados; dependências, compatibilidade e alterações de dados.]

### Plano de verificação

[Relacionar requisitos aos cenários de verificação. Registrar os comandos exatos e existentes; definir os novos comandos durante a preparação do ambiente.]

### Pontos para revisão

[Decisões e riscos concretos do plano que precisam de revisão antes das tarefas.]

## Modelo de tasks.md — Tasks

### Identificação

[Feature e referências à spec e ao design aprovados.]

### Checklist de implementação

- [ ] T-NNN-01 — [resultado pequeno e verificável]. Requisitos: [REQ-NNN-xx]. Dependências: [tarefas anteriores ou nenhuma]. Verificação: [comando real e resultado esperado].
- [ ] T-NNN-02 — [próximo resultado]. Requisitos: [REQ-NNN-xx]. Dependências: [T-NNN-01]. Verificação: [comando real e resultado esperado].

### Registro de execução

[Para cada tarefa executada, registrar verificação e resultado. Marcar somente após cumprir os critérios. Informar falhas ou impedimentos com precisão.]
