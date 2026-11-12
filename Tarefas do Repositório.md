## Fazer:

[] Organizar e padronizar todos os arquivos da pasta Templates.

[] - Organizar e padronizar todos a pasta Agentes.

[] - Criar Pasta padronizada de Specs

[] - Criar Pasta padronizada de (Documentação, Arquitetura, Interface, Qualidade e Segurança)

## SubAgentes Codex Base
[] - Reviewer (04-Quality-Secuity): Especificamente para revisões estilo Pull Request, verificando correção lógica, regressões e falhas evidentes.
[] - Code-Reviewer (04-Quality-Secuity): Complementa o reviewer atuando como guardião de qualidade geral, legibilidade e boas práticas.
[] - Security-Auditor (04-Quality-Secuity): Vasculha vulnerabilidades, falhas de autenticação e exposição de dados sensíveis.
[] - Architect-Reviewer 04-(Quality-Secuity): Garante que as mudanças respeitam as fronteiras da arquitetura e não introduzem acoplamento indevido.
[] - Code-Mapper (01-Core-Development): Excelente para mapear caminhos de execução e entender rapidamente quem é dono de qual parte do código antes de propor mudanças.
[] - Docs-Researcher (10-Research-Analysis): Como o próprio README destaca nos fluxos de exemplo, ele verifica a documentação oficial das APIs e frameworks que o patch utiliza, evitando alucinações.

## SubAgentes Codex Backend
[] - Performance-Enginner  (04-Quality-Security): Identifica gargalos de processamento, uso excessivo de memória e problemas de concorrência.
[] - Database-Optimizer (05-Data-AI): Focado em performance de banco de dados, ajudando a detectar queries lentas, problemas de N+1 e falta de índices.
[] - Sql-Pro (02-Language-Specialists): Especialista na escrita e revisão de consultas SQL complexas e migrações.
[] - Api-Designer (01-Core-Development): Ideal para revisar contratos REST e GraphQL, garantindo padronização de payloads, status codes e retrocompatibilidade.
[] - Backend-Developer (01-Core-Development): 
[] - Qa-Expert (04-Quality-Security): Avalia a cobertura e a qualidade dos testes automatizados de unidade e integração.


## SubAgentes Codex Frontend
[] - Accessibility-Tester (04-Quality-Security): Verifica conformidade com padrões de acessibilidade (a11y), HTML semântico e atributos ARIA
[] - Anti-Ui-Slop-Reviewer (04-Quality-Security): Um diferencial muito útil desse repositório: atua como um filtro final de acabamento visual para evitar interfaces genéricas ou mal estruturadas.
[] - Ui-Ux-Tester (04-Quality-Security): Focado em testes funcionais exaustivos de fluxos de interface e experiência do usuário.
[] - Browser-Debugger (04-Quality-Security): Excelente para investigar e reproduzir bugs específicos do lado do cliente diretamente no navegador.
[] - Design-Bridge (01-Core-Development): Muito útil caso você trabalhe com arquivos de especificação visual (DESIGN.md) para validar se o código implementado segue o design.
[] - Frontend-Developer (01-Core-Development)
[] - MicroServices-Architect (01-Core-Development)
[] - Mobile-Developer (01-Core-Development)

## SubAgentes Codex Refatoração
[] - Refactoring-Specialist (06-Developer-Experience): Excelente para atuar depois que uma feature funciona. Ele identifica oportunidades de simplificar funções complexas e melhorar a estrutura sem alterar o comportamento.
[] - Dependency-Manager (06-Developer-Experience): Recomendado para revisar alterações em arquivos de pacotes (package.json, pom.xml, requirements.txt), verificando conflitos de versão e dependências desnecessárias.
[] - Legacy-Modernizer (06-Developer-Experience): Útil quando você precisa mexer em partes antigas de um sistema e quer atualizar padrões sem quebrar o que já existe.

## SubAgentes Codex Documentação
[] - Api-Documenter (07-Specialized-Domains): Gera e revisa especificações técnicas de endpoints (como OpenAPI/Swagger), garantindo que os exemplos e tipos batam com o código real.
[] - Documentation-Enginner (06-Developer-Experience): 
[] - Readme-Generator (06-Developer-Experience): 

## SubAgentes Codex Debug e Testes
[] - Debugger (04-Quality-Security): Especialista em investigar a causa raiz de falhas complexas, analisando fluxos de dados e estados antes de sugerir qualquer correção.
[] - Error-Detective (04-Quality-Security): Focado especificamente em analisar stack traces, logs de erro e exceções para identificar padrões de falha.
[] - Test-Automator (04-Quality-Security): Complementa o qa-expert ajudando a estruturar suítes de testes automatizados e configurar frameworks de teste no projeto.

## SubAgentes Codex Outras
[] - Docker-Expert (03-Infrastructure): Ótimo para revisar Dockerfile e docker-compose.yml, garantindo imagens leves, seguras e builds rápidos.
[] - DevOps-Enginner (03-Infrastructure): Útil para validar arquivos de CI/CD (como .github/workflows), verificando se as etapas de build, teste e deploy estão eficientes.
[] - Git-Workflow-Manager (06-Developer-Experience): Ajuda a organizar estratégias de branches, resolução de conflitos complexos e padronização de commits
[] - Ponder-Reviewer (04-quality-security) — Um revisor de múltiplas passadas que faz uma análise deliberativa mais profunda, ideal para Pull Requests críticos ou muito grandes.
[] - knowledge-synthesizer (09-meta-orchestration) — Excelente para atuar como o consolidador final quando você dispara 3 ou 4 subagentes em paralelo, resumindo todos os pareceres em uma lista única e acionável.
[] - • context-manager (09-meta-orchestration) — Ajuda a otimizar quais informações são passadas entre os agentes em repositórios muito extensos.



