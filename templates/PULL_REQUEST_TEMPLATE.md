# Modelo de Pull Request — {{NOME_DO_SISTEMA}}

> **Para que serve:** garantir que todo PR chegue para revisão com o mínimo de informação necessária — o que mudou, como foi testado, o que cobre e o que falta — em vez de descrições vazias tipo "ajustes". Reduz ida e volta de revisor pedindo contexto que devia estar na descrição.
>
> **Template reutilizável.** Copie para `.github/pull_request_template.md` (ou `.github/PULL_REQUEST_TEMPLATE.md`) na raiz do repositório, substitua os `{{PLACEHOLDERS}}` e apague os blocos `<!-- guia: ... -->` e a seção "Como adaptar" ao final. O GitHub preenche automaticamente a descrição de todo PR novo com o conteúdo deste arquivo.
>
> Este arquivo é referenciado pela seção "Abrindo Pull Request" do `CLAUDE.md`. Quando o modelo mudar aqui, atualize a referência lá.

## Placeholders deste template

| Placeholder | Significado | Exemplo |
|---|---|---|
| `{{SHELL_PADRAO}}` | Shell usado nos exemplos de comando | `powershell` ou `bash` |
| `{{CMD_BUILD_BACKEND}}` | Comando de build do backend | `dotnet build ...` |
| `{{CMD_TEST_BACKEND}}` | Comando de teste do backend | `dotnet test ...` |
| `{{CMD_BUILD_FRONTEND}}` | Comando de build do frontend | `pnpm build` |
| `{{CMD_LINT_FRONTEND}}` | Comando de lint do frontend | `pnpm lint` |

<!-- guia: se o projeto não tem uma das camadas (ex: sem frontend), apague as linhas do checklist e do bloco de comandos correspondentes em vez de deixá-las em branco. -->

---

# Resumo

Descreva em poucas linhas o que este PR altera e por quê.

## Tipo de mudança

- [ ] Feature
- [ ] Bugfix
- [ ] Hotfix
- [ ] Refactor
- [ ] Documentação
- [ ] Configuração/infra

## Como testar

Explique os passos usados para validar a mudança.

- [ ] Rodei build local
- [ ] Rodei testes unitários
- [ ] Rodei testes automatizados adicionais, quando aplicável
- [ ] Validei o fluxo principal alterado
- [ ] Inclui prints ou vídeo quando a mudança afeta interface

Comandos executados:

```{{SHELL_PADRAO}}
{{CMD_BUILD_BACKEND}}
{{CMD_TEST_BACKEND}}
```

Se não foram criados testes unitários, explique o motivo:

```text

```

## Cobertura da mudança

- [ ] Cobre regra de negócio alterada
- [ ] Cobre validação/permissão alterada
- [ ] Cobre contrato ou mapeamento de dados alterado
- [ ] Cobre estado de erro/loading/vazio quando aplicável
- [ ] Não se aplica, pois a mudança é somente documental/configuração sem comportamento

## Banco de dados

- [ ] Não altera banco
- [ ] Altera modelo/migration
- [ ] Precisa de seed ou ajuste manual

Detalhes, se houver:

## Impacto visual

- [ ] Não altera interface
- [ ] Altera interface

Prints ou vídeo, se houver:

## Variáveis de ambiente

- [ ] Não adiciona variáveis
- [ ] Adiciona/altera variáveis

Detalhes, se houver:

## Checklist do autor

- [ ] A branch saiu da base correta
- [ ] O PR aponta para a base correta
- [ ] O título do PR está claro
- [ ] Commits seguem Conventional Commits
- [ ] Não inclui chaves, senhas ou dados sensíveis
- [ ] Não inclui arquivos temporários, logs, dumps locais ou screenshots soltos

---

## Como adaptar este template a um novo projeto

<!-- guia: apague esta seção inteira depois de preencher. -->

1. **Substitua os placeholders** da tabela do topo e apague a tabela.
2. **Ajuste os comandos executados** para a stack real do projeto (backend, frontend, ou ambos).
3. **Remova checklists que não se aplicam.** Um projeto só-backend não precisa de "Impacto visual"; um projeto sem banco não precisa de "Banco de dados" — apague a seção inteira em vez de deixar todos os itens desmarcados.
4. **Mantenha alinhado com o `CLAUDE.md`.** A seção "Abrindo Pull Request" do `CLAUDE.md` referencia este arquivo — se um checklist mudar aqui, confirme que a referência lá ainda faz sentido.
