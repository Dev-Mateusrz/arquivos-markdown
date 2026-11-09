Atualizado: 09/11/2026
# Organização arquitetural de um projeto frontend

Ao criar um novo frontend, agrupe o código por funcionalidades e mantenha as dependências orientadas pelas regras abaixo. Os caminhos representam o **projeto destino**. A árvore usa React e TypeScript como exemplo; preserve as convenções do framework escolhido e adapte extensões, componentes e mecanismos de estado quando a stack for diferente.

## 1. Organize o projeto por funcionalidades

Use uma organização por fatias de funcionalidade: mantenha juntos interface, integração, regras, tipos e testes que mudam pelo mesmo motivo de negócio. Reserve as pastas globais para composição da aplicação e recursos realmente compartilhados.

```text
projeto/
├── public/                         # Arquivos públicos servidos diretamente
├── src/
│   ├── app/                        # Composição, inicialização e roteamento
│   │   ├── routes/                 # Registro e composição de rotas em uma SPA
│   │   │   └── orders.tsx
│   │   ├── layouts/                # Estruturas de navegação da aplicação
│   │   └── provider.tsx            # Provedores necessários à aplicação
│   ├── components/                 # UI compartilhada, sem regras de negócio
│   │   ├── ui/                     # Botões, campos, diálogos e outras primitivas
│   │   └── feedback/               # Indicadores, mensagens e estados visuais
│   ├── config/                     # Configuração de ambiente e da aplicação
│   ├── features/
│   │   ├── auth/                   # Exemplo de funcionalidade
│   │   ├── users/                  # Exemplo de perfil e apresentação de usuários
│   │   └── orders/                 # Exemplo de funcionalidade
│   │       ├── api/                # Operações e integração de dados de pedidos
│   │       ├── components/         # UI específica de pedidos
│   │       ├── screens/            # Telas que compõem essa funcionalidade
│   │       ├── hooks/              # Hooks próprios do fluxo
│   │       ├── model/              # Validação, mapeamentos e modelos internos da UI
│   │       ├── stores/             # Estado compartilhado local à funcionalidade
│   │       ├── types/              # DTOs de entrada e saída da API
│   │       └── index.ts            # Entrada pública explícita da funcionalidade
│   ├── hooks/                      # Hooks reutilizáveis sem dependência de negócio
│   ├── lib/                        # Adaptadores e bibliotecas configuradas
│   ├── stores/                     # Estado de cliente realmente global
│   ├── styles/                     # Tokens, tema e estilos globais
│   ├── testing/                    # Utilitários e mocks compartilhados de testes
│   ├── types/                      # Tipos genuinamente compartilhados
│   └── utils/                      # Funções genéricas e puras
└── tests/
    └── e2e/                        # Jornadas completas da aplicação
```

Substitua `auth`, `users` e `orders` pelas capacidades reais do sistema. Crie somente os diretórios necessários: uma funcionalidade pequena não precisa começar com todas essas subdivisões. Preserve as pastas nativas de rotas e arquivos públicos quando o framework estabelecer outros caminhos.

Comece com uma estrutura simples dentro de cada funcionalidade e separe responsabilidades à medida que surgirem arquivos com propósitos distintos. Não instale bibliotecas apenas para preencher a árvore. Organize a documentação pelo [guia de documentação](documentação.md).

## 2. Defina onde cada código deve ficar

| Código ou responsabilidade | Local no projeto | Regra de organização |
|---|---|---|
| Inicialização, roteamento e composição de funcionalidades | `src/app/` | Conectar as partes sem concentrar suas regras de negócio |
| Botão, campo, modal, estrutura visual genérica | `src/components/` | Sem conhecer pedidos, usuários do domínio ou endpoints específicos |
| Card de pedido, formulário e ações de pedidos | `src/features/orders/components/` | Permanecer junto da funcionalidade que determina seu comportamento |
| Tela completa de uma funcionalidade | `src/features/orders/screens/` | Compor os componentes e estados daquele fluxo |
| Busca, criação ou cancelamento de pedidos | `src/features/orders/api/` | Encapsular transporte, contratos e integração com a estratégia de dados |
| Contratos brutos de entrada e saída da API | `src/features/orders/types/` | Manter DTOs separados dos modelos de tela e formulário |
| Regras, esquemas de validação e mapeamentos de pedidos | `src/features/orders/model/` | Validar e transformar os contratos brutos para o uso interno |
| Tipos de estado da tela, formulário e modelos de apresentação | `src/features/orders/model/` | Representar as necessidades da UI sem alterar o contrato da API |
| Estado e hooks exclusivos de pedidos | Dentro de `src/features/orders/` | Não promover para uma pasta global por conveniência de importação |
| Cliente HTTP, configuração do cache ou adaptador externo | `src/lib/` | Compartilhar infraestrutura sem importar funcionalidades |
| Formatação e validação genéricas | `src/utils/` | Não depender da interface nem de uma funcionalidade |
| Testes e histórias de um componente | Junto do código correspondente | Manter o ciclo de manutenção local à responsabilidade testada |

Promova um recurso a compartilhado quando houver uso real em contextos independentes e uma responsabilidade estável. Duas partes visualmente parecidas podem ter regras distintas; não crie um componente global cheio de condições de negócio apenas para evitar repetição.

Não transforme `utils/`, `lib/`, `hooks/` ou `types/` em depósitos genéricos. Se um arquivo exige conhecer uma funcionalidade para ser entendido, mantenha-o nela. Ativos exclusivos podem permanecer junto da funcionalidade; reserve `public/` para o que precisa de um endereço público direto.

Dentro de uma funcionalidade, reserve `types/` estritamente aos DTOs de transporte, como `OrderDto` em `types/order.dto.ts`. Mantenha esquemas Zod/Yup ou equivalentes, mapeadores, tipos de formulário e modelos de apresentação em `model/`, como `OrderViewModel` em `model/order.model.ts`. Quando um tipo puder ser inferido de um esquema, prefira essa inferência a uma declaração duplicada. Props específicas de um componente podem permanecer junto de sua implementação.

Use contratos gerados a partir da fonte canônica quando disponíveis, sem criar outra cópia manual dos DTOs. A pasta global `src/types/` não deve receber contratos e estados específicos das funcionalidades apenas para facilitar sua importação.

## 3. Proteja as fronteiras de dependência

Adote esta política de importação no projeto:

| Origem da importação | Pode depender de | Não pode depender de |
|---|---|---|
| `app/` | Entradas públicas das funcionalidades e recursos compartilhados | Arquivos privados de funcionalidades |
| Uma funcionalidade | Seus próprios arquivos e recursos compartilhados | `app/` ou outra funcionalidade, mesmo por sua entrada pública |
| Recursos compartilhados | Outros recursos compartilhados necessários, sem ciclos | `features/` ou `app/` |

Quando uma tela precisar de duas funcionalidades, faça a composição na camada da aplicação. Passe dados, callbacks ou componentes pelos contratos públicos. Não crie uma dependência circular entre funcionalidades para resolver essa composição.

### Entrada pública da funcionalidade

Exponha apenas o que os consumidores precisam. Nesta base, use uma entrada pequena `index.ts`, com exportações nomeadas e explícitas:

```typescript
// src/features/orders/index.ts
export { OrdersScreen } from './screens/orders-screen';
export { OrderCard } from './components/order-card';
export type { OrderViewModel } from './model/order.model';
```

```typescript
// src/app/routes/orders.tsx
import { OrdersScreen } from '@/features/orders';

// Não acessar os detalhes privados a partir de app/:
// import { OrdersScreen } from '@/features/orders/screens/orders-screen';
```

### Caminhos de importação

- Dentro da própria funcionalidade, use obrigatoriamente caminhos relativos (`./` ou `../`) para consumir seus arquivos internos, sem retornar pelo seu `index.ts`.
- Dentro de uma funcionalidade, reserve o alias global `@/` ao consumo de recursos compartilhados, como `@/components/ui/button`, `@/lib/api-client` e `@/config/env`.
- Não use `@/features/...` nem `@/app/...` dentro de uma funcionalidade. Caminhos relativos que escapem para outra funcionalidade ou para `app/` também continuam proibidos.
- A camada `app/` pode usar `@/features/orders` e outras entradas públicas para realizar a composição. Essa permissão não se estende às funcionalidades.
- Configure o alias de forma consistente no TypeScript, no bundler e nos testes. A convenção visual facilita a revisão, mas não substitui a verificação das fronteiras por lint.

Evite `export *` e arquivos globais que reexportem a aplicação inteira.

Se houver código exclusivo de servidor e de cliente, mantenha entradas públicas distintas, como `server.ts` e `client.ts`, e impeça que uma entrada de cliente exporte módulos de servidor. Não misture ambientes em um único barrel. Verifique ciclos, isolamento de ambiente e impacto no build; a existência de `index.ts` não aplica essas proteções automaticamente.

Esta política adapta o isolamento de funcionalidades do Bulletproof React com entradas públicas explícitas. A referência atual do Bulletproof desencoraja barrels amplos; portanto, mantenha a superfície de exportação pequena. Se o framework ou bundler exigir entradas diretas, declare os módulos públicos permitidos e proteja-os no lint, preservando a mesma fronteira.

### Composição entre funcionalidades sem importações cruzadas

Quando `OrderCard` precisar apresentar um usuário, receba os dados simples necessários por props ou ofereça um slot de conteúdo. Não importe o componente nem o tipo de domínio privado de `users` dentro de `orders`.

Exemplo de componente que oferece um slot por função, sem conhecer a funcionalidade de usuários:

```tsx
// src/features/orders/components/order-card.tsx
import type { ReactNode } from 'react';

type OrderCardProps = {
  title: string;
  renderUserAvatar?: () => ReactNode;
};

export function OrderCard({ title, renderUserAvatar }: OrderCardProps) {
  return (
    <article>
      {renderUserAvatar?.()}
      <h2>{title}</h2>
    </article>
  );
}
```

A página da aplicação importa as duas entradas públicas e conecta as partes. Neste exemplo, considere que `users` expõe `UserAvatar` com a prop `userId`; os valores são ilustrativos:

```tsx
// src/app/routes/orders.tsx
import { OrderCard } from '@/features/orders';
import { UserAvatar } from '@/features/users';

export function OrdersPage() {
  return (
    <OrderCard
      title="Pedido de exemplo"
      renderUserAvatar={() => <UserAvatar userId="user-42" />}
    />
  );
}
```

Se bastarem nome e imagem, passe props simples em vez de um componente. Quando houver coordenação entre funcionalidades, mantenha o estado dessa interação no ancestral comum de `app/` e distribua valores e callbacks. Não mova código de negócio para uma store global apenas para contornar o isolamento.

O callback de renderização acima pressupõe composição no mesmo ambiente de cliente. Em aplicações com Server Components, funções comuns não podem ser passadas livremente do servidor ao cliente: coloque a composição interativa em um componente de cliente ou use slots de elementos compatíveis com essa fronteira, conforme o framework.

## 4. Componha componentes, telas e layouts

- Mantenha componentes genéricos responsáveis por apresentação e interação de UI. Eles podem controlar foco, expansão ou seleção local; não precisam ser componentes sem qualquer estado.
- Coloque componentes que conhecem regras de negócio dentro da funcionalidade. Separe operações de dados e regras reutilizáveis da marcação visual; evite componentes que concentrem transporte, cache, validação, navegação e apresentação.
- Use uma tela para compor os componentes de seu fluxo e tratar carregamento, erro, vazio e sucesso. Quando o framework oferecer limites de carregamento e erro, use também seus mecanismos nativos.
- Mantenha a estrutura comum de navegação nos layouts da aplicação. Um layout exclusivo de uma funcionalidade pode ficar nela e ser composto pela rota.
- Faça os layouts receberem o conteúdo por composição: `children`, slots ou o mecanismo do roteador adotado, como `Outlet`. Evite que uma casca genérica importe componentes privados de negócio.
- Use composição de componentes, inclusive Compound Components quando houver partes coordenadas com uma interface clara. Não aplique o padrão a um elemento simples sem necessidade.
- Preserve semântica, navegação por teclado e estados acessíveis ao compor a UI. Reutilizar uma biblioteca visual não elimina a verificação do comportamento final.

## 5. Organize as rotas conforme o framework

Em uma SPA com roteador declarativo, use `app/routes/` para registrar rotas, compor telas e layouts e conectar carregamento ou proteção de navegação. Mantenha regras de domínio e transporte nas funcionalidades correspondentes.

No Next.js App Router, use os arquivos nativos de `app/`, como `page.tsx` e `layout.tsx`, em vez de criar um segundo sistema de roteamento em `app/routes/`. Um adaptador de rota pode ficar em `src/app/orders/page.tsx` e compor a funcionalidade de pedidos. Respeite grupos e segmentos do framework quando necessários.

Use os recursos de navegação e tipagem oferecidos pelo roteador escolhido. Centralize a construção de URLs quando ela for manual e valide parâmetros e dados externos em tempo de execução. Tipagem estática não garante que uma URL recebida do navegador seja válida.

Trate autenticação e autorização nos pontos efetivos de acesso aos dados e operações. Um redirecionamento de interface ou a ausência de um botão não substitui a verificação de permissão do serviço.

## 6. Separe operações de dados e tipos de estado

Em `features/<funcionalidade>/api/`, mantenha funções de operação e integração com o mecanismo de dados adotado, consumindo os contratos de entrada/saída de `types/`. Use o cliente compartilhado de `lib/` para detalhes transversais; mantenha regras e endpoints específicos na funcionalidade.

Preserve a forma bruta do contrato em `types/`. Coloque em `model/` os esquemas de validação, as funções de transformação e os tipos internos de tela ou formulário. Um campo recebido como texto, por exemplo, pode ser validado e convertido para uma representação apropriada à UI sem redefinir silenciosamente o DTO original.

Organize esse fluxo como resposta da API → validação e mapeamento → modelo interno → apresentação. Faça a conversão na fronteira de consumo ou na seleção dos dados, usando funções de `model/`, para evitar que cada componente interprete o payload por conta própria. Essa separação organiza as responsabilidades; não exige criar cópias de estado em stores diferentes.

Para operações no cliente que precisem de cache, sincronização ou invalidação, use TanStack Query, SWR ou o mecanismo definido no projeto. Com TanStack Query, coloque os hooks de query/mutation junto das operações da funcionalidade e mantenha chaves e políticas de invalidação coerentes.

Não espalhe `fetch`/Axios e controle manual de cache pelos componentes visuais. Em frameworks com loaders, ações ou Server Components, operações podem ser funções executadas no servidor ou no roteador; não transforme obrigatoriamente cada requisição em um hook de cliente.

| Natureza do estado | Onde manter |
|---|---|
| Interação de um único componente | Estado local, próximo de quem o utiliza |
| Interação compartilhada por componentes próximos | Ancestral comum ou mecanismo de composição adequado |
| Coordenação entre funcionalidades distintas | Ancestral comum na camada `app/`, com props, slots e callbacks pelas entradas públicas |
| Filtro, busca ou paginação que precisa ser compartilhável por URL | Parâmetros da rota, com leitura e validação centralizadas |
| Dados remotos | Cache ou mecanismo de dados definido para o projeto |
| Estado de cliente complexo de uma funcionalidade | Store ou reducer local à funcionalidade, quando necessário |
| Preferência ou estado de cliente transversal | Provedor ou store global de escopo explícito |

Use Zustand quando houver necessidade real de uma store; ele não é obrigatório para abrir um modal ou compartilhar um valor simples. Não replique dados remotos e de sessão em uma store apenas para torná-los globais. Defina uma fonte responsável por cada estado e derive valores calculáveis em vez de sincronizar cópias.

Para um estado compartilhado por várias funcionalidades, `app/` pode oferecer um controlador ou contexto de composição. As funcionalidades devem receber os valores e ações por seus contratos, sem importar esse contexto de `app/` nem conhecer os detalhes internos umas das outras.

Em aplicações com servidor, preserve a fronteira de execução: segredos e módulos exclusivos de servidor ficam fora das entradas consumidas pelo navegador. No Next.js, não torne toda a árvore cliente apenas para acomodar um provedor; mantenha a fronteira onde a interação for necessária.

## 7. Mantenha estilos, nomes e testes próximos do uso

Use a solução de estilos acordada no projeto. Tailwind, CSS Modules e bibliotecas visuais são opções de implementação, não requisitos desta organização. Mantenha tokens e tema compartilhados em um ponto central, e estilos específicos junto de seu componente ou funcionalidade.

Use nomes que revelem a responsabilidade, como `order-card.tsx`, `get-orders.ts` e `use-orders.ts`. Preserve as convenções de arquivos do framework. Nomeie componentes e tipos conforme as convenções da linguagem e evite arquivos como `helpers2.ts` ou `common.ts` sem propósito definido.

Coloque testes de regras, hooks e componentes junto do código correspondente, por exemplo `order-card.test.tsx`. Reserve `testing/` para utilitários de teste compartilhados e `tests/e2e/` para jornadas que atravessam a aplicação. Se houver Storybook, mantenha histórias junto dos componentes e use seu catálogo como fonte de referência visual, conforme o [guia de documentação](documentação.md).

## 8. Siga este fluxo ao implementar uma funcionalidade

1. Identifique o resultado para o usuário, seus critérios de aceite e o domínio responsável. Reaproveite uma funcionalidade existente quando o comportamento pertencer a ela.
2. Defina os contratos de integração e as dependências permitidas antes de distribuir arquivos.
3. Crie operações, regras e tipos locais necessários, sem antecipar abstrações para usos hipotéticos.
4. Implemente componentes e a tela, cobrindo os estados de UI e as restrições do fluxo.
5. Exponha a entrada pública mínima e faça a composição na rota/layout apropriado.
6. Crie os testes proporcionais ao comportamento e conecte as verificações arquiteturais ao lint.
7. Execute os checks aplicáveis, confira a interface e atualize a documentação afetada.

Ao remover uma funcionalidade, revise também rotas, exportações, navegação, testes, flags, permissões e contratos externos relacionados. O isolamento reduz o trabalho de remoção, mas não garante que apagar uma pasta seja suficiente.

## 9. Faça o CI proteger a organização

Configure ESLint ou uma ferramenta de fronteiras compatível para verificar a matriz de dependências e o acesso aos módulos públicos. Com `eslint-plugin-import`, zonas de `import/no-restricted-paths` podem bloquear dependências por caminho resolvido. Restrições de importação podem complementar a proteção dos pontos de entrada.

Cubra imports por alias e caminhos relativos, reexportações e importações de tipos. Verifique também ciclos e limites cliente/servidor com ferramentas compatíveis com a stack; um único padrão textual não garante todas essas verificações. Ao criar novas funcionalidades, atualize as zonas ou use regras que descubram seus limites automaticamente.

No projeto destino, confirme que o lint rejeita pelo menos estes casos em alterações descartáveis:

- Uma funcionalidade importando outra, inclusive por sua entrada pública.
- Um arquivo compartilhado importando uma funcionalidade.
- Uma funcionalidade importando `app/`.
- Um arquivo de funcionalidade consumindo seus próprios módulos por `@/features/...`, em vez de caminhos relativos.
- Uma rota importando um arquivo privado da funcionalidade, por alias ou caminho relativo.
- Uma dependência circular ou um módulo exclusivo de servidor alcançado pelo cliente, conforme os verificadores adotados.

Restaure os casos inválidos depois da verificação. Execute lint arquitetural, tipagem, testes relevantes e build no CI. Configure os checks como obrigatórios na política de merge e não use `continue-on-error` para esconder violações.

Se o projeto já adotar Feature-Sliced Design formalmente, preserve suas camadas e regras próprias e use um validador compatível, como Steiger com o conjunto de regras correspondente. Não misture a árvore deste guia com as camadas do FSD sem uma decisão arquitetural explícita.

## 10. Confira a entrega

Entregue uma estrutura em que seja possível localizar cada funcionalidade, identificar seu contrato público e saber onde compor telas e rotas. Verifique que recursos globais não dependem das funcionalidades, que estados têm responsáveis definidos e que código de servidor não é exportado ao cliente.

Registre a arquitetura aplicada, as adaptações da stack e as verificações realmente executadas na documentação do projeto. A criação das pastas e deste guia não equivale à configuração ou à aprovação dos checks no projeto destino.

## Referências de manutenção

As instruções acima são a política desta base, adaptada das referências; não dependem de uma etapa prévia de leitura desses materiais para serem aplicadas.

- [Bulletproof React — organização por funcionalidades e dependências](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md)
- [Feature-Sliced Design — entradas públicas e limites dos barrels](https://feature-sliced.design/docs/reference/public-api)
- [React — responsabilidade e compartilhamento de estado](https://react.dev/learn/sharing-state-between-components)
- [React — composição por props e conteúdo](https://react.dev/learn/passing-props-to-a-component)
- [React — tipos de componentes e conteúdo renderizável](https://react.dev/learn/typescript)
- [TanStack Query — dados remotos e estado de cliente](https://tanstack.com/query/latest/docs/framework/react/guides/does-this-replace-client-state)
- [Next.js — estrutura do projeto](https://nextjs.org/docs/app/getting-started/project-structure)
- [Next.js — componentes de servidor e cliente](https://nextjs.org/docs/app/getting-started/server-and-client-components)
- [ESLint — restrições por zonas de caminhos](https://github.com/import-js/eslint-plugin-import/blob/main/docs/rules/no-restricted-paths.md)
- [Steiger — validação arquitetural](https://github.com/feature-sliced/steiger)
