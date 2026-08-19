# {{NOME_ORGANIZACAO}}

### {{DESCRICAO_ORGANIZACAO}}

<!--
Template reutilizável. Copie para o repositório central/`.github` da
organização como `README.md` (ou `profile/README.md`, se for o perfil
público da org no GitHub), substitua os {{PLACEHOLDERS}} e apague este
comentário e a seção "Como adaptar" ao final.

Placeholders deste template:
  {{NOME_ORGANIZACAO}}        Nome/sigla da organização no GitHub          (ex.: SUBG-SMS)
  {{DESCRICAO_ORGANIZACAO}}   Nome por extenso da organização/área          (ex.: Subsecretaria de Gestão — Secretaria Municipal de Saúde)
  {{BRANCH_PRODUCAO}}         Branch de produção                            (ex.: main)
  {{BRANCH_DESENVOLVIMENTO}}  Branch de homologação/staging                 (ex.: develop)
  {{FERRAMENTA_TRACKER}}      Ferramenta de gestão de tarefas                (ex.: Jira)
  {{CHAVE_PROJETO_TRACKER}}   Chave/prefixo usado nas issues                 (ex.: SUBG-123)
  {{SERVIDOR_DEV}}            Nome do ambiente de desenvolvimento/testes     (ex.: devsubg)
  {{SERVIDOR_PROD}}           Nome do ambiente de produção                   (ex.: subg)
  {{FERRAMENTA_CONTAINER}}    Ferramenta de containerização preferida        (ex.: Docker)

Este documento é o "CLAUDE.md da organização": regras que valem para todo
repositório novo, antes mesmo de ele ganhar seu próprio CLAUDE.md/CONTRIBUTING.md
específico. Onde as duas coisas se sobrepõem (padrão de branch, de commit), o
arquivo do repositório manda no detalhe; este arquivo garante que a base seja
a mesma em todo lugar.
-->

Bem-vindo à organização **{{NOME_ORGANIZACAO}}**.
Este repositório central define os **padrões oficiais de desenvolvimento**, garantindo consistência, segurança e escalabilidade em todos os projetos.

---

## 📦 Padronização de Repositórios

Todos os repositórios devem seguir obrigatoriamente a seguinte convenção de nomenclatura:

- `backend-{nome}` → Serviços backend (APIs, workers, etc.)
- `frontend-{nome}` → Aplicações frontend (web, mobile, etc.)
- `fullstack-{nome}` → Projetos monorepo (frontend + backend)

> Exemplo:
> - `backend-auth`
> - `frontend-portal`
> - `fullstack-agendamento`

---

## 🌿 Padrões de Branch

Estrutura obrigatória de branches:

- `{{BRANCH_PRODUCAO}}` → Produção
- `{{BRANCH_DESENVOLVIMENTO}}` → Homologação / staging
- `feat/*` → Novas funcionalidades
- `fix/*` → Correções de bugs
- `hotfix/*` → Correções urgentes em produção

> Exemplo:
> - `feat/login-social`
> - `fix/erro-token-expirado`
> - `hotfix/falha-pagamento`

---

## 📝 Padrões de Commit

Utilizamos o padrão **Conventional Commits** para manter histórico organizado e rastreável:

- `feat:` → Nova funcionalidade
- `fix:` → Correção de bug
- `hotfix:` → Correção crítica em produção
- `docs:` → Documentação
- `ci:` → Alterações em pipelines e automações

> Exemplo:
> ```
> feat: adiciona autenticação com JWT
> fix: corrige validação de CPF
> docs: atualiza instruções de instalação
> ```

<!-- guia: se a organização usa o padrão "ID do card no commit" (ver CLAUDE.md dos
repositórios individuais), diga isso aqui também — é a regra que faz a automação
mover o card sozinha, e vale a pena repetir no documento que todo projeto novo lê primeiro. -->

---

## 🏗️ Infraestrutura e Containerização

Atualmente, a infraestrutura conta com dois servidores internos:

- **{{SERVIDOR_DEV}}** → Ambiente de desenvolvimento e testes
- **{{SERVIDOR_PROD}}** → Ambiente de produção

Todos os projetos devem ser preparados para execução em ambiente containerizado (preferencialmente {{FERRAMENTA_CONTAINER}}), garantindo:

- Padronização de ambientes
- Facilidade de deploy
- Isolamento de dependências

---

## 🧪 Testes e Qualidade

Todos os projetos devem obrigatoriamente conter:

- Testes unitários
- Cobertura mínima adequada (definida por projeto)
- Revisão de código via Pull Request

Objetivos:

- Reduzir regressões
- Aumentar confiabilidade
- Garantir qualidade do código

---

## ⚙️ Metodologia Ágil

Utilizamos o **{{FERRAMENTA_TRACKER}}** como ferramenta oficial de gestão de tarefas.

Nosso fluxo segue princípios ágeis:

- Todas as demandas devem estar registradas no {{FERRAMENTA_TRACKER}}
- Cada task deve possuir:
  - Descrição clara
  - Critérios de aceitação
  - Responsável definido
- O desenvolvimento deve sempre estar vinculado a uma task
- Commits e Pull Requests devem referenciar o ID da tarefa

> Exemplo:
> ```
> feat: implementa cadastro de usuários [{{CHAVE_PROJETO_TRACKER}}]
> ```

---

## 🤝 Contribuições

Para contribuir com qualquer projeto:

1. Criar uma branch a partir da `{{BRANCH_DESENVOLVIMENTO}}`
2. Seguir o padrão de nomenclatura de branches
3. Realizar commits no padrão definido
4. Abrir um Pull Request para `{{BRANCH_DESENVOLVIMENTO}}`
5. Aguardar revisão obrigatória

> Nenhum código deve ser enviado diretamente para `{{BRANCH_PRODUCAO}}`

---

## 📚 Documentação

Todos os projetos, **sem exceção**, devem conter um arquivo `README.md` com:

- Descrição do projeto
- Tecnologias utilizadas
- Instruções de execução
- Variáveis de ambiente
- Exemplos de uso (quando aplicável)

---

## 🚨 Diretrizes Gerais

- Código limpo e legível é obrigatório
- Segurança deve ser considerada desde o início
- Evitar duplicação de código
- Sempre priorizar performance e escalabilidade

---

## 📌 Considerações Finais

Este documento é **obrigatório** para todos os projetos da organização.
O não cumprimento dos padrões pode resultar em bloqueio de merges ou revisões.

---

**{{NOME_ORGANIZACAO}}**
{{DESCRICAO_ORGANIZACAO}}

<!--
Como adaptar este template a uma nova organização (apague este bloco):
1. Substitua os placeholders do topo.
2. Se a organização não usa dois servidores fixos (dev/prod), reescreva a
   seção de infraestrutura para descrever o pipeline real (ex.: cloud
   gerenciada, CI que builda e publica sozinho).
3. Se cada projeto tiver seu próprio CLAUDE.md/CONTRIBUTING.md (recomendado —
   ver os templates deste mesmo repositório), deixe claro aqui que este
   documento é a base comum, e que o arquivo do repositório manda em caso de
   detalhe específico.
-->
