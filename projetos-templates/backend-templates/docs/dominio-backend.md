<!--
Template reutilizável. Copie para `docs/dominio.md` no repositório de
backend, substitua os {{PLACEHOLDERS}} e apague este comentário, os exemplos
ilustrativos e a seção "Como adaptar" ao final.

Este documento é o glossário do negócio: os termos que o código, o
rastreador de issues e as conversas com quem pede a funcionalidade usam
todos da mesma forma. Ele é o arquivo mais específico deste conjunto de
templates — praticamente todo o conteúdo é reescrito por projeto. O que
permanece é a ESTRUTURA (o que o sistema faz → conceitos → estrutura
organizacional, se houver → papéis → regras garantidas pelo banco) e o nível
de detalhe esperado.
-->

# Domínio

Vocabulário do {{NOME_DO_SISTEMA}}. Vale ler antes do primeiro card — o código usa esses termos
exatamente como este documento os define.

Fonte: {{FONTE_DOCUMENTO_FUNCIONAL}}.

## O que o sistema faz

{{OBJETIVO_DO_SISTEMA_DETALHADO}}

<!-- guia: diga também o que o sistema NÃO é, se houver confusão comum — "não é ferramenta
de X nem de Y" ajuda tanto quanto dizer o que ele é. -->

## Conceitos

<!-- guia: liste os termos fundamentais do domínio, na ordem em que aparecem no fluxo
principal. Cada linha deve caber numa frase — se precisar de um parágrafo, o termo
provavelmente merece sua própria seção abaixo. -->

| Termo | O que é |
| --- | --- |
| **{{CONCEITO_1}}** | {{DEFINICAO_CONCEITO_1}} |
| **{{CONCEITO_2}}** | {{DEFINICAO_CONCEITO_2}} |
| **{{CONCEITO_3}}** | {{DEFINICAO_CONCEITO_3}} |

Em uma linha: {{RESUMO_RELACAO_ENTRE_CONCEITOS}}.

## Estrutura organizacional

<!-- guia: esta seção só se aplica quando o sistema modela uma hierarquia real (setores,
unidades, equipes). Apague se o domínio for plano (ex.: só "usuário" e "conta"). -->

```
{{NIVEL_1}}
└── {{NIVEL_2}}
    └── {{NIVEL_3}}
        └── {{NIVEL_4}}
```

| {{NIVEL_2}} | Nome | {{ATRIBUTO_ADICIONAL}} |
| --- | --- | --- |
| {{EXEMPLO_1}} | {{NOME_EXEMPLO_1}} | {{VALOR_EXEMPLO_1}} |
| {{EXEMPLO_2}} | {{NOME_EXEMPLO_2}} | {{VALOR_EXEMPLO_2}} |

## Papéis

<!-- guia: um papel por linha, com a responsabilidade em uma frase. Se o mesmo papel muda
de comportamento conforme o contexto (ex.: por vínculo, por tenant), diga isso explicitamente
— é o tipo de regra que se perde fácil na implementação. -->

| Perfil | Papel |
| --- | --- |
| `{{PERFIL_1}}` | {{RESPONSABILIDADE_PERFIL_1}} |
| `{{PERFIL_2}}` | {{RESPONSABILIDADE_PERFIL_2}} |
| `{{PERFIL_3}}` | {{RESPONSABILIDADE_PERFIL_3}} |

## Siglas

<!-- guia: todo domínio de negócio real acumula siglas. Documentá-las aqui evita que cada
pessoa nova pergunte a mesma coisa no chat do time. -->

| Sigla | Significado |
| --- | --- |
| {{SIGLA_1}} | {{SIGNIFICADO_SIGLA_1}} |
| {{SIGLA_2}} | {{SIGNIFICADO_SIGLA_2}} |

## Regras que o banco já garante

<!-- guia: liste as invariantes de negócio que viraram constraint (não só validação de
código) — é a lista que qualquer revisão de schema deveria conferir antes de remover uma
constraint "estranha". Deve concordar com a tabela de constraints em banco-de-dados.md. -->

- {{REGRA_GARANTIDA_1}}
- {{REGRA_GARANTIDA_2}}
- {{REGRA_GARANTIDA_3}}

## Leia também

- [Banco de dados](banco-de-dados.md) — como isso está modelado
- [Decisões](decisoes.md) — onde o modelo se afasta da fonte funcional, e por quê

<!--
Como adaptar este template a um novo projeto (apague este bloco):
1. Preencha "O que o sistema faz" primeiro — é o que dá contexto para todo o
   resto do documento.
2. Escreva "Conceitos" na ordem em que um novo desenvolvedor precisaria
   aprendê-los para entender o primeiro card, não em ordem alfabética.
3. Apague as seções que não se aplicam ("Estrutura organizacional" para um
   domínio plano, "Papéis" para um sistema sem RBAC) em vez de deixá-las com
   placeholder.
4. Mantenha "Regras que o banco já garante" sincronizada com
   banco-de-dados.md — as duas listas devem contar a mesma história por
   ângulos diferentes (o quê vs. como).
-->
