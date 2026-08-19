<!--
Template reutilizável. Copie para `docs/acesso.md` no repositório de
frontend, substitua os {{PLACEHOLDERS}} e apague este comentário e a seção
"Como adaptar" ao final.

Este documento assume Next.js (App Router) com sessão em cookie httpOnly
gerida pelo próprio Next como BFF (backend-for-frontend) na frente de uma
API separada. Se o novo projeto usa outro mecanismo de sessão (ex.: token no
localStorage, provedor de identidade externo tipo Auth0/Keycloak), reescreva
a seção "A sessão vive em cookie httpOnly" com a arquitetura real — não force
o padrão de cookie httpOnly nesse caso.
-->

# Acesso: login, cadastro e aprovação

Como o frontend autentica e como o cadastro {{DESCRICAO_MODALIDADE_CADASTRO}} funciona. O backend está em
`{{REPO_BACKEND}}`; aqui fica só o que é do lado do navegador.

## A sessão vive em cookie httpOnly

O navegador **não fala com a API diretamente** nas chamadas REST. Ele fala com o Next, que guarda
os tokens em cookies `httpOnly` e repassa. O token nunca chega ao JavaScript — um XSS não
rouba a sessão de ninguém.

```
navegador ──▶ Next (Server Action / Route Handler) ──▶ API {{FRAMEWORK_BACKEND}}
              cookie httpOnly com os tokens
```

Verificável: depois do login, `document.cookie` não mostra nenhum cookie de sessão.

### Duas regras da plataforma que moldam o desenho

**Cookie só pode ser escrito em Server Action ou Route Handler.** Um Server Component que
descobre o token vencido durante o render não pode renovar sozinho. Por isso:

| Função | Onde usar | Escreve cookie? |
| --- | --- | --- |
| `tokenValido()` | Server Component, render | Não — só lê |
| `tokenParaAcao()` | Server Action | Sim, renova se preciso |
| `renovarSessao()` | Server Action, Route Handler | Sim |

Quando a página encontra o token vencido, ela redireciona para uma rota de renovação
(`/sessao/renovar?destino=…`), que renova e devolve o usuário ao lugar de origem.

**Renovar sem conseguir gravar derruba a sessão.** A renovação rotaciona o token: se o novo
não for persistido, a chamada seguinte apresenta o antigo, o servidor trata como reúso e
revoga a família inteira.

**Módulo `"use server"` só exporta função assíncrona.** Estados iniciais de formulário devem
viver num módulo separado das actions; exportá-los do arquivo de actions quebra o build.

## Quem barra o quê

| Camada | O que faz | O que **não** faz |
| --- | --- | --- |
| Middleware do Next | Sem cookie de sessão, qualquer rota do sistema devolve `/login` | Não valida assinatura, não olha perfil, não fala com a API |
| `exigirSessao()` nas páginas | Confirma a sessão contra `/auth/me` antes de renderizar; renova quando dá | Não decide permissão fina |
| API de backend | Autoriza de verdade, a cada requisição | — |

O middleware é a checagem otimista de que fala a documentação do Next: ele existe para a
pessoa não ver a casca do app carregar e só então descobrir que caiu fora. Rotas públicas
típicas: `/login`, `/cadastro` e a rota de renovação de sessão.

A sidebar mostra a sessão real — nome, e-mail, nível de acesso e {{CAMPO_CONTEXTO}} vêm de
uma função de leitura de sessão do lado do servidor. **Sair da conta** deve ser um `form` com
Server Action, não um link: sair revoga o token de renovação no servidor antes de apagar o
cookie.

## Contexto ativo e troca de vínculo

<!-- guia: esta seção só se aplica quando o usuário pode ter mais de um contexto (unidade,
tenant, organização) e precisa trocar entre eles sem logar de novo. Apague se o sistema tiver
um contexto só por usuário. -->

Toda permissão do sistema depende do {{CAMPO_CONTEXTO}} em que a pessoa está atuando — quem não
sabe onde está não sabe o que pode fazer. Por isso o contexto aparece **sempre**, visível no
cabeçalho.

Quem tem mais de um {{CAMPO_CONTEXTO}} troca pelo menu da conta, sem novo login. A troca não é
cosmética: a API encerra a família de tokens antiga e emite outra já no contexto escolhido, e
os cookies são regravados antes de a tela recarregar. Com um contexto só, a seção nem aparece.

## Padrão de tela: gestão de usuários

<!-- guia: use este esqueleto para a tela administrativa de usuários/permissões. Ajuste as
abas ao que o projeto realmente precisa. -->

Tudo que é de gestão de pessoas mora numa tela só. Cada linha da tabela é um **vínculo** —
quem atua em mais de um contexto aparece mais de uma vez — com um menu de ações para editar e
inativar.

A ficha abre em abas típicas:

| Aba | O que faz |
| --- | --- |
| Dados | Campos editáveis do cadastro. Identificadores (e-mail, documento) ficam à vista num bloco travado |
| Permissões | Duas colunas — disponíveis e concedidas — com concessão por arrasto ou por clique (cada cartão também é um botão de verdade, para quem usa teclado ou leitor de tela) |
| Auditoria | Tudo que a pessoa fez e o que fizeram com ela, com autor, {{CAMPO_CONTEXTO}}, IP e data/hora |

**Identificadores de login (e-mail, documento) aparecem, mas não se editam** — mudá-los não é
editar cadastro, é apontar a conta para outra pessoa.

Concessão de permissão nova só passa a valer no próximo login ou renovação — a permissão
efetiva viaja no token, e a janela é a validade dele.

## Trilha de auditoria

Existe um serviço que grava **quem fez, o quê, sobre quem, quando e de onde**. Duas decisões
que valem registro:

- **Auditoria nunca derruba a operação.** Se a gravação falhar, o erro vai para o log e a ação
  segue. O contrário significaria recusar um login porque a trilha estava indisponível.
- **A trilha grava em contexto próprio**, fora da transação da requisição principal.
  Compartilhar faria um rollback da operação apagar o registro de que ela foi tentada.

## Cadastro por convite

<!-- guia: esta seção só se aplica quando o cadastro é fechado (por convite) em vez de
aberto. Apague ou reescreva se o sistema tiver auto-cadastro livre. -->

```
/gerenciar/usuarios  quem gerencia cria o link (modal: duração e nº de pessoas)
      ↓
/cadastro/[codigo]   formulário, com o contexto do convite
      ↓
tela de espera       atualiza sozinha quando a decisão sai
      ↓
/login               a pessoa entra com a senha que cadastrou
```

O convite não carrega perfil — só define **onde** a pessoa se cadastra, **por quanto tempo**
vale e **quantas pessoas** podem usá-lo. O perfil é escolhido só na aprovação, por quem
conhece a pessoa.

**Isso é conveniência, não segurança.** Toda validação do formulário no navegador é espelho de
uma regra do domínio; quem decide é a API, e o erro do servidor é repassado com a mensagem
exata do campo que falhou, não traduzido para um "dados inválidos" genérico.

## Tempo real

<!-- guia: esta seção só se aplica quando o projeto usa WebSocket/SignalR/equivalente. Apague
se não houver atualização em tempo real. -->

| Tela | Como atualiza | Por quê |
| --- | --- | --- |
| {{TELA_TEMPO_REAL_1}} | WebSocket | {{MOTIVO_TEMPO_REAL_1}} |
| {{TELA_TEMPO_REAL_2}} | Recarga periódica | {{MOTIVO_RECARGA_PERIODICA}} |

Se o canal de WebSocket exige identificar quem está ouvindo, mas o token de acesso vive num
cookie `httpOnly` que nunca chega ao JavaScript, considere um **ticket de curta duração**: pedido
ao servidor Next (que enxerga o cookie) e entregue ao navegador só na hora de conectar, com
audiência própria e validade de segundos — não o token da sessão.

## CORS

As chamadas REST servidor-a-servidor não precisam de CORS. **Uma conexão que sai direto do
navegador (WebSocket, upload direto) precisa.** As origens permitidas ficam configuradas no
backend, por ambiente.

## Política de conteúdo (CSP)

<!-- guia: mantenha esta seção se o projeto usa CSP com nonce por requisição — é uma decisão
fácil de fazer errado (aplicar a política só na resposta, sem nonce na requisição, faz o
navegador bloquear o próprio app). -->

A CSP precisa nascer no middleware/proxy, não em configuração estática, quando exige um nonce
novo a cada requisição. O framework precisa **ler o cabeçalho da própria requisição** para
descobrir o nonce e carimbá-lo nos scripts que emite — aplicar a política só na resposta faz
o navegador bloquear o próprio app, que renderiza mas nunca hidrata.

Duas escolhas que costumam parecer frouxas e não são:

- `script-src` não deveria levar `'unsafe-inline'`. Prefira `'nonce-…'` e `'strict-dynamic'`.
- `style-src` com `'unsafe-inline'` pode ser necessário se o framework serializa estilo
  inline no HTML do servidor — estilo inline desfigura a tela, não executa código nem lê
  cookie, então o risco é de outra natureza que o de script inline.

`connect-src` precisa incluir a URL da API e a variante `ws://`/`wss://` dela, se houver
WebSocket. **Se essa variável divergir do endereço real, a conexão morre bloqueada e sem
aviso visível na tela.**

## Configuração

`.env.local` (ignorado pelo git):

```
API_BASE_URL=http://localhost:{{PORTA_BACKEND_DEV}}
{{PREFIXO_VAR_AMBIENTE}}_API_BASE_URL=http://localhost:{{PORTA_BACKEND_DEV}}
```

`API_BASE_URL` é usado pelo servidor do Next. `{{PREFIXO_VAR_AMBIENTE}}_API_BASE_URL` vai para o
navegador — só deve existir se algo (ex.: WebSocket) precisa conectar direto, sem passar pelo
Next.

Se a porta divergir da porta real do backend em desenvolvimento, o login falha com um erro
genérico de conexão — o Next não alcança a API e não tem como distinguir isso de a API estar
fora do ar.

<!--
Como adaptar este template a um novo projeto (apague este bloco):
1. Substitua os placeholders.
2. Apague as seções marcadas como condicionais (contexto múltiplo, convite,
   tempo real) se o projeto não tiver esse caso.
3. Se a sessão não for cookie httpOnly + BFF, reescreva a primeira seção do
   zero — é a premissa de que todo o resto do documento depende.
-->
