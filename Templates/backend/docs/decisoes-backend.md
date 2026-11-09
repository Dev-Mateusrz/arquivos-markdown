<!--
Template reutilizável. Copie para `docs/decisoes.md` no repositório de
backend, apague este comentário, os três exemplos preenchidos abaixo (eles
existem só para calibrar o nível de detalhe esperado) e a seção "Como
adaptar" ao final. A partir daí, o arquivo é vivo: cada decisão de
engenharia relevante ganha uma entrada nova, numerada em sequência, nunca
reescrita — se uma decisão muda, registre a mudança como uma decisão nova
que referencia a anterior (veja o exemplo 3).
-->

# Decisões

Registro do que foi decidido, e principalmente **por quê**. Serve para quem chegar depois não
refazer a discussão — e para reabri-la com conhecimento de causa quando o contexto mudar.

Ordem cronológica. Cada decisão diz também o que se paga por ela.

<!-- guia: o formato de cada entrada é: título curto no cabeçalho, depois os campos
Contexto (por que a decisão foi necessária — pode ser omitido se óbvio), Decisão (o que foi
escolhido, em uma frase que dá pra citar), Por quê (o raciocínio), Preço ou Consequência (o
que se paga, ou o que muda pra quem usa o sistema depois). Nem toda decisão tem os quatro
campos — use os que fizerem sentido. -->

---

## 1. {{TITULO_DECISAO_EXEMPLO_1}}

<!-- guia: apague este exemplo ao adaptar o template. Calibra uma decisão arquitetural. -->

> **Contexto** — Sistema que precisa durar, com regra de negócio densa e prestação de contas
> a um órgão de controle externo.
>
> **Decisão** — Camadas `Domain`, `Application`, `Infrastructure`, `Api`, com as dependências
> apontando para dentro. `Domain` sem nenhuma dependência externa.
>
> **Preço** — Mais projetos para navegar, e `Application` nasce vazio até o primeiro caso de
> uso.

---

## 2. {{TITULO_DECISAO_EXEMPLO_2}}

<!-- guia: apague este exemplo ao adaptar o template. Calibra uma decisão de modelagem de
dados com trade-off explícito. -->

> **Decisão** — Cadastros pequenos e estáveis usam `int` identity; o que circula fora do
> sistema (aparece em URL, é referenciado externamente) usa `uuid` numa variante ordenável
> no tempo.
>
> **Por quê** — `int` lê melhor e é conferível a olho. `uuid` onde o identificador não deve
> ser adivinhável. A variante ordenável no tempo não fragmenta índice como um UUID
> puramente aleatório.
>
> **Preço** — Duas convenções no mesmo modelo. Quem cria uma tabela nova precisa escolher
> qual se aplica.

---

## 3. {{TITULO_DECISAO_EXEMPLO_3}} — supera a decisão 2 em parte

<!-- guia: apague este exemplo ao adaptar o template. Calibra como registrar uma decisão que
revisita uma anterior sem apagá-la — a decisão antiga fica no arquivo, com uma nota apontando
para a nova. -->

> **Contexto** — A decisão 2 assumia que nenhuma tabela de cadastro precisaria ser
> referenciada por sistemas externos. Um novo integrador passou a depender do identificador
> de uma dessas tabelas.
>
> **Decisão** — A tabela `{{TABELA_EXEMPLO}}` migra de `int` identity para `uuid`, mantendo o
> `int` antigo como coluna de compatibilidade por um período de transição.
>
> **Consequência** — Toda referência interna a essa tabela precisou ser revisada. A migration
> não é trivialmente reversível — documentado explicitamente, ao contrário da maioria das
> migrations deste projeto.

---

## Leia também

- [Arquitetura](arquitetura.md) · [Banco de dados](banco-de-dados.md) · [Configuração](configuracao.md) · [API](api.md)

<!--
Como adaptar este template a um novo projeto (apague este bloco):
1. Apague os três exemplos preenchidos acima antes do primeiro uso real —
   eles são calibragem, não conteúdo. A numeração recomeça em 1 com a
   primeira decisão real do projeto.
2. Nunca reescreva uma entrada antiga para "corrigi-la". Se uma decisão muda,
   crie uma entrada nova que referencia a anterior (ver exemplo 3) — o
   histórico de como o pensamento mudou é tão valioso quanto a decisão atual.
3. Uma decisão vale um registro quando: (a) alguém vai perguntar "por que
   está assim?" mais de uma vez, (b) existe uma alternativa óbvia que foi
   descartada, ou (c) a escolha tem um preço que só aparece depois. Decisão
   óbvia sem alternativa plausível não precisa de entrada.
4. Cite o card/issue relacionado quando houver — facilita achar a discussão
   original.
-->
