> **Instrução para a IA (Meta-Prompt):** Este documento é um **guia de referência de mercado** para estruturar regras de criação e revisão de Pull Requests. Ao utilizá-lo para gerar o arquivo `.agents/padrao-pullrequest.md` de um repositório, **não copie nomes fictícios ou valores de exemplo** (`SA-142`, `develop`, `main`). Inspecione primeiro o repositório atual para verificar se já existe um template oficial (como `.github/pull_request_template.md`), qual é a branch de destino padrão, quais comandos de validação local existem e quais evidências são exigidas pela camada do projeto (front-end ou back-end), gerando um arquivo de regras determinístico e adaptado à realidade do repositório.


As melhores práticas de mercado para Pull Requests hoje tratam o PR como um pacote de revisão pequeno, autoexplicativo e validado automaticamente antes de chegar a um humano, especialmente com o aumento do volume de código gerado por IA.

Abaixo está o que times de engenharia de alta performance aplicam e como isso se estrutura na prática:


## Boas Práticas

- Limite de 200 a 400 linhas: Estudos e guias modernos apontam que revisões acima de 400 linhas perdem drasticamente a capacidade de detectar falhas. Com IA gerando código rápido, manter PRs pequenos e atômicos é a principal defesa contra regressões.

- Separação de preocupações: Nunca misture refatoração estrutural ou renomeação de arquivos com mudança de regra de negócio no mesmo PR. Se a entrega for grande, use Stacked PRs (PRs empilhados em etapas pequenas).

- Draft PR para trabalho em andamento: Use Draft Pull Request enquanto ainda estiver validando ou aguardando pipeline, evitando gastar tempo dos revisores com código inacabado.

### Estrutura Eficiente do Pull Request

Um PR de alta qualidade responde ao "porquê" e ao "como validar" sem obrigar o revisor a adivinhar a intenção olhando apenas o diff:

- Título Semântico (Conventional Commit): Segue o formato < tipo >(< escopo >): < descrição no imperativo > (ex: feat(agenda): adiciona filtro por status de atendimento). Isso garante que, ao usar Squash and Merge, o histórico principal continue limpo e rastreável.

- Resumo Objetivo (Contexto + Mudanças): Explica a motivação da alteração e o impacto arquitetural, sempre vinculando a issue correspondente (ex: Closes SA-142 ou link do Jira).

- Roteiro de Validação / Testes: Passo a passo reproduzível para testar a funcionalidade, indicando cenários cobertos por testes automatizados e casos de borda verificados.

- Evidências Obrigatórias por Camada:
  -  Front-end / UI: Screenshots (antes e depois) ou vídeo/GIF curto mostrando o fluxo funcionando.
  - Back-end / Banco: Contratos de API alterados, migrations de banco de dados e alertas explícitos caso haja Breaking Change ou necessidade de deploy coordenado.

### Higiene Pré-PR (Shift-Left e Autorrevisão)

Antes de solicitar revisão (ou autorizar a IA a abrir o PR), o autor deve cumprir três etapas:

1. Autorrevisão do Diff: Ler o próprio git diff antes de publicar para eliminar console.log, código morto, comentários temporários e arquivos não relacionados.

2. Quality Gates Locais: Executar localmente build, lint, typecheck e testes unitários/integração antes de subir o código, evitando que a pipeline falhe por erros triviais.

3. Auditoria de Segurança: Verificar se nenhuma credencial, .env, token ou dado sensível entrou no commit.


## Boas Práticas Específicas para PRs com IA

- Revisão guiada pelo Ticket: O revisor (humano ou agente) deve ler a issue/critérios de aceite antes de olhar o diff, validando se o comportamento atende ao negócio e não apenas se o código compila.

- Responsabilidade Humana: O desenvolvedor que abre o PR precisa compreender e ser capaz de explicar cada decisão do código gerado pela IA, validando testes e edge cases manualmente.

- Limpeza de Trailers Automáticos: Remover assinaturas padrão de ferramentas como Generated with... ou Co-Authored-By: de bots antes de submeter o PR.

- Automação na Primeira Camada: Usar linters, análise estática, scanners de segredos e revisores automatizados (como CodeRabbit ou Copilot) para pegar problemas mecânicos, deixando os revisores humanos focados em arquitetura, segurança e regras de negócio.

## Estrutura do PullRequest

## Resumo e Motivação
```
<!-- Descreva em 2 a 4 linhas o que foi alterado e por que essa mudança é necessária. -->


**Issue vinculada:** <!-- Ex: Closes SA-142 ou link do Jira -->

---

## Tipo de Mudança
- [ ] `feat`: Nova funcionalidade
- [ ] `fix`: Correção de bug
- [ ] `refactor`: Refatoração de código (sem alterar comportamento)
- [ ] `perf`: Melhoria de performance
- [ ] `docs` / `chore` / `test`: Documentação, manutenção ou testes
- [ ] `BREAKING CHANGE`: Quebra de compatibilidade (exige deploy coordenado)

---

## Principais Alterações Técnicas
<!-- Liste objetivamente os módulos, endpoints, componentes ou regras modificadas. -->
*
*

---

## Como Testar e Validar
<!-- Passo a passo reproduzível para o revisor validar a entrega localmente ou em homologação. -->
1. Acesse `<rota / endpoint>`.
2. Execute `<ação com os dados X>`.
3. Verifique se `<resultado esperado ocorre>`.

---

## Evidências (Obrigatório para UI / Contratos)
<!-- Front-end: anexe prints (Antes/Depois) ou vídeo curto. Back-end: cole exemplo de payload/resposta ou evidência dos testes. -->


---

## Checklist Pré-Revisão (Autor)
- [ ] O título do PR segue o padrão Conventional Commit (`<tipo>(<escopo>): <descrição>`).
- [ ] Executei localmente `build`, `lint` e `testes` sem falhas.
- [ ] Revisei o próprio `git diff` e removi logs temporários, código morto ou comentários desnecessários.
- [ ] Confirmei que nenhum segredo, token ou arquivo `.env` foi incluído.
- [ ] Caso haja alteração de banco de dados (*migration*) ou contrato de API, ela está documentada acima.


```
