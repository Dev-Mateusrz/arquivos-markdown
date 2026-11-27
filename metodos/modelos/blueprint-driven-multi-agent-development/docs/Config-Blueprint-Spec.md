> **Instrução para a IA (Meta-Prompt de Setup e Execução):** Este documento é um **guia operacional de instalação, configuração e execução** para integrar *Blueprint-Driven Multi-Agent Development* (BMAD), *Spec-Driven Development* (SDD) e *GitHub Spec Kit* (`specify`) em um projeto. Ao utilizá-lo para inicializar ou configurar um ambiente, **não execute comandos cegamente nem copie nomes ilustrativos** (`copilot`, `001-autenticacao`, `openapi-typescript`, `Orval`, `openapi.yaml`). Inspecione primeiro o sistema e o diretório atual para verificar:
> 1. **Ambiente, Ferramentas e Integração Real:** Verifique quais ferramentas já estão instaladas (`python`, `uv`, `node`, `npm`, `git`, `specify`), qual IDE ou agente de IA está ativo no momento (para ajustar a flag `--integration` e a seleção do `skills add`) e se o repositório já possui pastas do Spec Kit (`.specify/`), BMAD (`_bmad/`) ou specs (`.specs/`).
> 2. **Topologia do Projeto (Multi-Repo vs. Monorepo):** Identifique se o projeto opera como um *Umbrella Workspace* (com repositórios separados de `backend/` e `frontend/` clonados internamente e ignorados no `.gitignore`) ou como um repositório único, adaptando a estrutura de pastas e o `AGENTS.md` / `CLAUDE.md` à topologia real.
> 3. **Estado da Stack e Contratos:** Verifique se o projeto é *Greenfield* com stack em aberto (onde o *Analyst* e o *PM* operam sem viés tecnológico para que o *Architect* decida a stack antes de gravá-la via `/speckit-constitution`) ou se já existe uma stack/contrato definido (REST/OpenAPI, GraphQL, gRPC, AsyncAPI).
>
> A partir dessa verificação, execute o setup e conduza as fases de forma incremental e determinística, garantindo estritamente:
> - **Respeito aos Quality Gates Humanos:** Nunca avance automaticamente da arquitetura para a criação de contratos ou código sem antes apresentar a stack e os ADRs do *Architect* para aprovação explícita do usuário.
> - **Isolamento de Contexto entre Sessões:** Oriente ou inicie sessões limpas na transição entre personas (*Analyst* → *PM* → *Architect* → *SM* → *Dev* → *QA*) e isole as tarefas de backend (`tasks-be.md`) e frontend (`tasks-fe.md`) antes da implementação.


Atualização 27/11/2026

# Configurando Spec-Driven + Blueprint-Driven + GitHub Spec Kit

Esse arquivo é um guia passo-a-passo de como instalar, configurar e usar o Blueprint-Driven, Specs-Driven e GitHub Spec Kit em um novo projeto frontend + backend.

Para instalar, configurar e usar o BMAD Method junto com o GitHub Spec Kit em um projeto Frontend + Backend do zero, você deve montar um Umbrella Workspace (repositório guarda-chuva) que centraliza as ferramentas via CLI (specify-cli e skills CLI) e isola os repositórios de código.

### Passo 1 - Pré-requisitos do Ambiente

Instalar essas 3 ferramentas:

> Python 3.11+ e uv (usados tanto pelo GitHub Spec Kit quanto pelos scripts Python auxiliares do BMAD).

> Node.js 20.12+ e npm (usados pela CLI de instalação de skills do BMAD).

> Git e sua IDE / Agente de IA suportado (Claude Code, Cursor, GitHub Copilot, Codex, etc.).

### Passo 2 - Instalação das CLIs
Crie o repositório central de governança (onde ficarão as specs, contratos e personas) antes de criar os repositórios de código:

```text
# 1. Instale a CLI do GitHub Spec Kit globalmente via uv e inicialize no diretório atual
uv tool install specify-cli
specify init . --integration copilot   # Troque 'copilot' por: claude, cursor, gemini, etc.

# 2. Instale o BMAD Method via Skills CLI (core-tools + method principal)
npx skills add bmad-code-org/BMAD-METHOD/skills/core-tools --skill '*'
npx skills add bmad-code-org/BMAD-METHOD/skills/method --skill '*'
```

Nota: Durante o npx skills add, selecione a mesma ferramenta de IA que você escolheu no specify init.

### Passo 3 - Configuração do Setup e Estrutura Multi-Repo

Com os pacotes instalados, abra o seu agente de IA dentro do espaço de trabalho e configure a ponte entre as duas ferramentas:  
  
1. Inicialize o BMAD no chat do agente:
Peça ao agente: "Rode o setup do bmad (bmad setup)". Isso criará a pasta _bmad/ e _bmad-output/ com as personas (Analyst, PM, Architect, SM, Dev, QA) e templates.

2. Organize as pastas de governança e .gitignore:
Crie uma pasta .specs/ (onde viverão constitution.md, contracts/ e features/).

2. Crie o AGENTS.md (ou CLAUDE.md) na raiz:
Crie este arquivo na raiz do workspace para ditar a regra de integração entre as ferramentas:
- Instrua que o BMAD conduz a fase de descoberta, requisitos e arquitetura (_bmad-output/).
- Instrua que o GitHub Spec Kit (.specify/) conduz a execução contratual de cada feature (/speckit-specify → /speckit-plan → /speckit-tasks → /speckit-implement → /speckit-converge).
- Proíba qualquer agente de escrever código antes que o contrato .specs/contracts/openapi.yaml esteja aprovado.

### Passo 4 - Uso na Prática - Fase 1 (Descoberta e Escolha da Stack)
Inicie o fluxo deixando o BMAD descobrir o produto e escolher a melhor stack sem viés prévio. Abra uma sessão limpa de chat para cada persona:
1. Constituição Inicial Agnóstica:
No chat do agente, rode:
```text
/speckit-constitution Crie princípios globais focados em arquitetura limpa, API-first (OpenAPI), cobertura de testes e isolamento estrito entre backend e frontend. Não defina linguagens ou frameworks ainda.
```

2. Descoberta de Negócio (Persona: Mary - Analyst):
Acione a skill de Analyst do BMAD, explique a ideia do seu sistema, público-alvo e restrições.
	- Resultado: _bmad-output/project-brief.md.
3. Requisitos e SLAs (Persona: John - PM):
Em uma nova sessão limpa, acione o PM do BMAD para ler o project-brief.md e gerar o documento de requisitos funcionais e não-funcionais (latência, escala, segurança).
	- Resultado: _bmad-output/prd.md.

4. Escolha da Stack e Topologia (Persona: Winston - Architect):
Em uma nova sessão limpa, acione o Architect do BMAD para ler o prd.md, avaliar trade-offs e decidir a stack de Backend, Frontend e Banco de Dados, gerando a arquitetura e os ADRs.
	- Quality Gate (Você): Revise o arquivo gerado. Aprovada a stack, rode /speckit-constitution novamente para gravar as tecnologias escolhidas como lei permanente do projeto.


### Passo 5: Uso na Prática — Fase 2 (Materialização dos Contratos)

Agora que a stack está definida (exemplo: Python/FastAPI no Back e Next.js/TypeScript no Front):
1. Peça ao Architect do BMAD para criar o contrato base .specs/contracts/openapi.yaml com os schemas principais e padrões de resposta de erro.


### Passo 6: Uso na Prática — Fase 3 (Ciclo de Desenvolvimento por Feature)

Para cada funcionalidade listada no prd.md, execute o pipeline do GitHub Spec Kit alternando as personas em sessões limpas:

1.Especificar (Persona: PM / PO):
```text
/speckit-specify Crie a especificação da feature 001-autenticacao com base no prd.md, contendo histórias de usuário e critérios de aceite Given/When/Then agnósticos de tecnologia.
```

2.Auditar e Clarificar (Persona: Scrum Master):  Rode /speckit-clarify e /speckit-analyze para identificar lacunas na regra de negócio ou conflitos com a constitution.md antes de planejar.

3.Planejar e Atualizar Contrato (Persona: Architect):
```text
/speckit-plan Crie o plano técnico da feature 001-autenticacao e atualize o arquivo .specs/contracts/openapi.yaml com os novos endpoints.
```

4.Fatiar Tarefas Isoladas (Persona: Scrum Master):
```text
/speckit-tasks Gere as tarefas atômicas divididas explicitamente em dois arquivos: tasks-be.md (para backend/) e tasks-fe.md (para frontend/).
```

5.Execução Paralela (Persona: Amelia - Dev):
- No Frontend: Rode um gerador de código (como openapi-typescript ou Orval) lendo .specs/contracts/openapi.yaml para gerar tipos e mocks. Abra uma sessão limpa apontando apenas para frontend/ + tasks-fe.md e rode /speckit-implement.
- No Backend: Abra outra sessão limpa apontando apenas para backend/ + tasks-be.md e rode /speckit-implement.

6.Auditoria Final (Persona: QA):
Na raiz do workspace, rode /speckit-converge. O agente verificará se o código implementado nos dois repositórios converge 100% com a spec.md e com o contrato openapi.yaml.