# SUBG-SMS  
### Subsecretaria de Gestão — Secretaria Municipal de Saúde

Bem-vindo à organização **SUBG-SMS**.  
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

- `main` → Produção
- `develop` → Homologação / staging
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
- `doc:` → Documentação
- `ci/cd:` → Alterações em pipelines e automações

> Exemplo:
> ```
> feat: adiciona autenticação com JWT
> fix: corrige validação de CPF
> doc: atualiza instruções de instalação
> ```

---

## 🏗️ Infraestrutura e Containerização

Atualmente, a infraestrutura conta com dois servidores internos:

- **devsubg** → Ambiente de desenvolvimento e testes
- **subg** → Ambiente de produção

Todos os projetos devem ser preparados para execução em ambiente containerizado (preferencialmente Docker), garantindo:

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

Utilizamos o **Jira** como ferramenta oficial de gestão de tarefas.

Nosso fluxo segue princípios ágeis:

- Todas as demandas devem estar registradas no Jira
- Cada task deve possuir:
  - Descrição clara
  - Critérios de aceitação
  - Responsável definido
- O desenvolvimento deve sempre estar vinculado a uma task
- Commits e Pull Requests devem referenciar o ID da tarefa

> Exemplo:
> ```
> feat: implementa cadastro de usuários [SUBG-123]
> ```

---

## 🤝 Contribuições

Para contribuir com qualquer projeto:

1. Criar uma branch a partir da `develop`
2. Seguir o padrão de nomenclatura de branches
3. Realizar commits no padrão definido
4. Abrir um Pull Request para `develop`
5. Aguardar revisão obrigatória

> Nenhum código deve ser enviado diretamente para `main`

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

**SUBG-SMS**  
Subsecretaria de Gestão  
Secretaria Municipal de Saúde
