#!/usr/bin/env node
// Template reutilizável. Copie para `.github/scripts/jira-sync.mjs` em CADA
// repositório do projeto (backend e frontend usam o MESMO arquivo, byte a
// byte — quem diferencia o comportamento é a variável de ambiente REPO_ROLE
// definida no workflow que chama este script, não o script em si).
// Substitua os placeholders e apague este comentário. É invocado pelo
// workflow `jira-pipeline-backend.yml` / `jira-pipeline-frontend.yml` deste
// mesmo docs-template.
//
// Placeholders deste template:
//   {{PREFIXO_ISSUE_MAIUSCULO}}   chave/prefixo do projeto no Jira, usado como fallback (ex.: SG)
//   {{COLUNA_EM_DESENVOLVIMENTO}} nome EXATO da coluna "em desenvolvimento" no board
//   {{COLUNA_EM_REVISAO}}         nome EXATO da coluna "em teste/revisão" no board
//   {{COLUNA_CONCLUIDO}}          nome EXATO da coluna "concluído" no board
//   {{BRANCH_DESENVOLVIMENTO}}    branch base de desenvolvimento          (ex.: develop)
//   {{BRANCH_PRODUCAO}}           branch de produção                      (ex.: main)
//   {{ROTULO_FULLSTACK}}          rótulo do Jira que trava o card até as duas pontas chegarem (ex.: fullstack)
//   {{DOMINIO_TRACKER}}           domínio do Jira, sem protocolo           (ex.: suaempresa.atlassian.net)
//   {{NOME_DO_SISTEMA}}           nome do sistema, usado só num comentário

/**
 * jira-sync.mjs — move os cards do Jira automaticamente conforme o fluxo de branches.
 *
 *   push em feat|fix|hotfix|...                          ->  {{COLUNA_EM_DESENVOLVIMENTO}}
 *   PR aprovado + mergeado em {{BRANCH_DESENVOLVIMENTO}}  ->  {{COLUNA_EM_REVISAO}}
 *   PR mergeado em {{BRANCH_PRODUCAO}}                    ->  {{COLUNA_CONCLUIDO}}
 *
 * O ID do card sai do nome da branch, do título/descrição do PR e das mensagens de
 * commit (ex.: `feat({{PREFIXO_ISSUE_MAIUSCULO}}-42): ...`, `hotfix/{{PREFIXO_ISSUE_MAIUSCULO}}-42-corrige-x`).
 * Vários cards no mesmo push/PR são movidos juntos.
 *
 * Card com o rótulo `{{ROTULO_FULLSTACK}}` no Jira só avança quando os DOIS repositórios
 * chegarem na mesma etapa. O estado fica em rótulos no próprio card
 * (`testes-backend`, `entregue-frontend`…), então um repo nunca precisa
 * enxergar o outro. Voltar a desenvolver limpa os selos e reinicia o ciclo.
 *
 * Sem dependências: usa só o fetch nativo do Node 20+.
 * Roda no GitHub Actions (lê o payload em GITHUB_EVENT_PATH).
 */

import { readFileSync } from 'node:fs'

const env = process.env

// ---------------------------------------------------------------- configuração
/**
 * Aceita tanto `https://{{DOMINIO_TRACKER}}` quanto a URL do board copiada do
 * navegador (`.../jira/software/projects/{{PREFIXO_ISSUE_MAIUSCULO}}/boards/562`) — só o host importa.
 */
function baseUrl(raw) {
  const valor = (raw || '').trim()
  if (!valor) return ''
  try {
    const { origin, pathname } = new URL(valor)
    if (pathname && pathname !== '/') {
      // `warn` ainda não existe neste ponto do módulo; anota direto.
      console.log(`::warning::JIRA_BASE_URL tinha um caminho ("${pathname}") — usando apenas ${origin}.`)
    }
    return origin
  } catch {
    return valor.replace(/\/+$/, '')
  }
}

const JIRA_BASE_URL = baseUrl(env.JIRA_BASE_URL)
const JIRA_USER_EMAIL = env.JIRA_USER_EMAIL || ''
const JIRA_API_TOKEN = env.JIRA_API_TOKEN || ''
const PROJECT_KEY = (env.JIRA_PROJECT_KEY || '{{PREFIXO_ISSUE_MAIUSCULO}}').toUpperCase()

// Nomes exatos dos status no board do {{NOME_DO_SISTEMA}}. Só mexa aqui se renomearem a coluna.
const STATUS_DEV = env.JIRA_STATUS_DEV || '{{COLUNA_EM_DESENVOLVIMENTO}}'
const STATUS_TEST = env.JIRA_STATUS_TEST || '{{COLUNA_EM_REVISAO}}'
const STATUS_DONE = env.JIRA_STATUS_DONE || '{{COLUNA_CONCLUIDO}}'

const BRANCH_DEVELOP = env.BRANCH_DEVELOP || '{{BRANCH_DESENVOLVIMENTO}}'
const BRANCH_MAIN = env.BRANCH_MAIN || '{{BRANCH_PRODUCAO}}'

// Merge na {{BRANCH_DESENVOLVIMENTO}} sem review aprovado NÃO move o card (regra do time).
const REQUIRE_APPROVAL = (env.REQUIRE_APPROVAL || 'true') !== 'false'
const POST_COMMENT = (env.JIRA_COMMENT || 'true') !== 'false'

// --- trava dos cards que atravessam as duas pontas -------------------------
// Card com o rótulo `{{ROTULO_FULLSTACK}}` só anda quando os DOIS repositórios chegarem na
// mesma etapa. Cada merge grava um selo (`testes-backend`, `entregue-frontend`…)
// no próprio card — é lá que o estado mora, sem um repo precisar enxergar o outro.
const FULLSTACK_LABEL = env.FULLSTACK_LABEL || '{{ROTULO_FULLSTACK}}'
const FULLSTACK_ROLES = (env.FULLSTACK_ROLES || 'backend,frontend')
  .split(',')
  .map((r) => r.trim().toLowerCase())
  .filter(Boolean)

/** Qual ponta é este repositório: vem do workflow, ou é deduzida do nome do repo. */
const REPO_ROLE = (() => {
  if (env.REPO_ROLE) return env.REPO_ROLE.trim().toLowerCase()
  const nome = (env.GITHUB_REPOSITORY || '').toLowerCase()
  return FULLSTACK_ROLES.find((papel) => nome.includes(papel)) || ''
})()

const MARKERS = ['testes', 'entregue'].flatMap((etapa) =>
  FULLSTACK_ROLES.map((papel) => `${etapa}-${papel}`),
)

const GITHUB_TOKEN = env.GITHUB_TOKEN || ''
const REPO = env.GITHUB_REPOSITORY || ''
const SERVER_URL = env.GITHUB_SERVER_URL || 'https://github.com'
const EVENT_NAME = env.GITHUB_EVENT_NAME || ''
const EVENT_PATH = env.GITHUB_EVENT_PATH || ''

// -------------------------------------------------------------------- helpers
const notice = (m) => console.log(`::notice::${m}`)
const warn = (m) => console.log(`::warning::${m}`)
const fail = (m) => {
  console.log(`::error::${m}`)
  process.exit(1)
}

/** Compara nomes de status ignorando acento, caixa e espaço extra. */
const normalize = (s) =>
  String(s || '')
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '') // tira acentos: "Itens concluídos" == "ITENS CONCLUIDOS"
    .trim()
    .replace(/\s+/g, ' ')
    .toUpperCase()

/** Extrai os IDs de card ({{PREFIXO_ISSUE_MAIUSCULO}}-123) de qualquer texto, sem repetir. */
function extractKeys(...texts) {
  const re = new RegExp(`\\b${PROJECT_KEY}[-_ ]?(\\d+)\\b`, 'gi')
  const found = new Set()
  for (const text of texts) {
    if (!text) continue
    for (const m of String(text).matchAll(re)) found.add(`${PROJECT_KEY}-${m[1]}`)
  }
  return [...found]
}

/**
 * Só a primeira linha da mensagem do commit.
 *
 * O corpo é onde se explica a decisão, e explicar quase sempre significa citar outro card
 * ("fora do escopo por dependência: {{PREFIXO_ISSUE_MAIUSCULO}}-54", "o {{PREFIXO_ISSUE_MAIUSCULO}}-48 precisa
 * decidir isso"). Lendo o corpo, a automação tratava citação como autoria e arrastava junto
 * cards que ninguém tocou — num caso real isso concluiu cards inteiros sem uma linha de
 * código escrita.
 *
 * O assunto é fonte confiável porque o hook `prepare-commit-msg` injeta o ID nele a partir
 * do nome da branch, e o `commit-msg` recusa o que sair do padrão.
 */
const assuntoDoCommit = (mensagem) => String(mensagem || '').split('\n', 1)[0]

// ---------------------------------------------------------------- GitHub API
async function gh(path) {
  const res = await fetch(`https://api.github.com${path}`, {
    headers: {
      Authorization: `Bearer ${GITHUB_TOKEN}`,
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
    },
  })
  if (!res.ok) throw new Error(`GitHub ${path} -> ${res.status} ${await res.text()}`)
  return res.json()
}

/**
 * Mesma coisa, seguindo as páginas até acabar.
 *
 * `per_page=100` sozinho é um teto silencioso: numa release grande, os commits mais
 * recentes de um PR extenso — justamente os que carregam o card daquela entrega — podem
 * ficar de fora da primeira página. Uma release não tem tamanho previsível, então o
 * limite não pode ser fixo.
 *
 * O teto de páginas existe só para não girar para sempre se a API repetir uma página; a
 * própria API já corta os commits de um PR em 250.
 */
async function ghTodasAsPaginas(path, maxPaginas = 10) {
  const juntos = []
  const separador = path.includes('?') ? '&' : '?'

  for (let pagina = 1; pagina <= maxPaginas; pagina++) {
    const lote = await gh(`${path}${separador}per_page=100&page=${pagina}`)
    if (!Array.isArray(lote) || lote.length === 0) break
    juntos.push(...lote)
    if (lote.length < 100) break
    if (pagina === maxPaginas) {
      warn(`${path}: parei em ${maxPaginas} páginas (${juntos.length} itens). Pode ter ficado card de fora.`)
    }
  }

  return juntos
}

/**
 * O PR tem aprovação válida?
 * Considera só o último review "com peso" de cada pessoa — um comentário solto
 * depois do approve não derruba a aprovação, mas um "changes requested" derruba.
 */
async function pullRequestApproval(number) {
  const reviews = await gh(`/repos/${REPO}/pulls/${number}/reviews?per_page=100`)
  const relevant = ['APPROVED', 'CHANGES_REQUESTED', 'DISMISSED']
  const latestByUser = new Map()
  for (const r of reviews) {
    if (!relevant.includes(r.state)) continue
    latestByUser.set(r.user?.login || r.id, r)
  }
  const approvers = [...latestByUser.values()]
    .filter((r) => r.state === 'APPROVED')
    .map((r) => r.user?.login)
    .filter(Boolean)
  const blockers = [...latestByUser.values()]
    .filter((r) => r.state === 'CHANGES_REQUESTED')
    .map((r) => r.user?.login)
    .filter(Boolean)
  return { approved: approvers.length > 0 && blockers.length === 0, approvers, blockers }
}

// ------------------------------------------------------------------ Jira API
const jiraAuth = 'Basic ' + Buffer.from(`${JIRA_USER_EMAIL}:${JIRA_API_TOKEN}`).toString('base64')

async function jira(path, options = {}) {
  const res = await fetch(`${JIRA_BASE_URL}/rest/api/3${path}`, {
    ...options,
    headers: {
      Authorization: jiraAuth,
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
  })
  const text = await res.text()
  if (!res.ok) {
    const err = new Error(`Jira ${options.method || 'GET'} ${path} -> ${res.status} ${text}`)
    err.status = res.status
    throw err
  }
  return text ? JSON.parse(text) : null
}

/** Monta um parágrafo em ADF (formato exigido pela API v3 do Jira). */
function adf(parts) {
  return {
    body: {
      type: 'doc',
      version: 1,
      content: [
        {
          type: 'paragraph',
          content: parts.map((p) =>
            p.href
              ? { type: 'text', text: p.text, marks: [{ type: 'link', attrs: { href: p.href } }] }
              : { type: 'text', text: p.text },
          ),
        },
      ],
    },
  }
}

/** Acrescenta e remove rótulos sem tocar no resto do card. */
async function setLabels(key, { add = [], remove = [] }) {
  const labels = [...add.map((l) => ({ add: l })), ...remove.map((l) => ({ remove: l }))]
  if (!labels.length) return
  try {
    await jira(`/issue/${key}`, { method: 'PUT', body: JSON.stringify({ update: { labels } }) })
  } catch (e) {
    warn(
      `Não consegui gravar os rótulos em ${key} (a conta da automação precisa de "Edit Issues"): ${e.message}`,
    )
  }
}

/** Move o card para `targetStatus`. Só chame depois de conferir o status atual. */
async function transition(key, current, targetStatus) {
  const { transitions } = await jira(`/issue/${key}/transitions`)
  const match = transitions.find((t) => normalize(t.to?.name) === normalize(targetStatus))
  if (!match) {
    const nomes = transitions.map((t) => t.to?.name).join(', ')
    warn(`${key}: não há transição para "${targetStatus}". Disponíveis: ${nomes || 'nenhuma'}.`)
    return null
  }

  await jira(`/issue/${key}/transitions`, {
    method: 'POST',
    body: JSON.stringify({ transition: { id: match.id } }),
  })
  notice(`${key}: "${current}" -> "${targetStatus}"`)
  return { key, from: current, to: targetStatus }
}

/**
 * Aplica o plano a um card: grava o selo da ponta, respeita a trava do `fullstack`
 * e só então move o status.
 */
async function applyToIssue(key, { status, parts, stage }) {
  let issue
  try {
    issue = await jira(`/issue/${key}?fields=status,labels,summary`)
  } catch (e) {
    if (e.status === 404) {
      warn(`Card ${key} não existe no Jira — ignorando.`)
      return
    }
    throw e
  }

  const current = issue.fields?.status?.name || ''
  const labels = [...(issue.fields?.labels || [])]
  const fullstack = labels.includes(FULLSTACK_LABEL)

  // Merge: registra que ESTA ponta chegou nesta etapa.
  if (stage === 'testes' || stage === 'entregue') {
    if (!REPO_ROLE) {
      warn(
        `Não sei se este repositório é ${FULLSTACK_ROLES.join(' ou ')} — defina REPO_ROLE no ` +
          `workflow. Seguindo sem registrar o selo de entrega.`,
      )
    } else {
      const selo = `${stage}-${REPO_ROLE}`
      if (!labels.includes(selo)) {
        await setLabels(key, { add: [selo] })
        labels.push(selo)
      }
    }

    // Trava: card marcado como fullstack espera as duas pontas.
    if (fullstack) {
      const faltando = FULLSTACK_ROLES.filter((papel) => !labels.includes(`${stage}-${papel}`))
      if (faltando.length) {
        notice(`${key} é ${FULLSTACK_LABEL} e ainda falta ${faltando.join(', ')} — card não movido.`)
        await comment(key, [
          ...parts,
          {
            text: ` Como o card está marcado como "${FULLSTACK_LABEL}", ele continua em "${current}" ` +
              `até ${faltando.join(' e ')} chegar na mesma etapa.`,
          },
        ])
        return
      }
    }
  }

  if (normalize(current) === normalize(status)) {
    notice(`${key} já está em "${current}" — nada a fazer.`)
    return
  }

  const moved = await transition(key, current, status)
  if (!moved) return

  // Voltar a desenvolver reinicia o ciclo: os selos antigos não podem concluir o
  // card sozinhos na próxima volta.
  if (stage === 'dev') {
    const antigos = MARKERS.filter((m) => labels.includes(m))
    if (antigos.length) {
      await setLabels(key, { remove: antigos })
      notice(`${key}: selos de entrega limpos (${antigos.join(', ')}) — ciclo reiniciado.`)
    }
  }

  await comment(key, parts)
}

async function comment(key, parts) {
  if (!POST_COMMENT) return
  try {
    await jira(`/issue/${key}/comment`, { method: 'POST', body: JSON.stringify(adf(parts)) })
  } catch (e) {
    warn(`Não consegui comentar em ${key}: ${e.message}`)
  }
}

// ---------------------------------------------------------------------- main
async function main() {
  for (const [name, value] of Object.entries({ JIRA_BASE_URL, JIRA_USER_EMAIL, JIRA_API_TOKEN })) {
    if (!value) fail(`Secret ${name} não configurado no repositório.`)
  }

  // Credencial errada faz o Jira responder 404 em todo card — o que é indistinguível
  // de "o card não existe". Conferir a autenticação antes evita caçar número de card à toa.
  try {
    const eu = await jira('/myself')
    notice(`Autenticado no Jira como ${eu.displayName} <${eu.emailAddress || 's/ e-mail visível'}>.`)
  } catch (e) {
    fail(
      `Não consegui autenticar em ${JIRA_BASE_URL}. Confira JIRA_USER_EMAIL (precisa ser o e-mail ` +
        `da conta que gerou o token) e JIRA_API_TOKEN. Resposta: ${e.message}`,
    )
  }

  const event = EVENT_PATH ? JSON.parse(readFileSync(EVENT_PATH, 'utf8')) : {}
  const plan = await buildPlan(event)
  if (!plan) return

  // `parts` fica no plano e vai inteiro para applyToIssue; aqui só interessam estes dois.
  const { keys, status } = plan
  if (!keys.length) {
    warn(
      `Nenhum ID de card (${PROJECT_KEY}-000) encontrado na branch, nos commits ou no PR. ` +
        `Nada foi movido no Jira.`,
    )
    return
  }

  notice(`Cards encontrados: ${keys.join(', ')} -> "${status}"`)
  for (const key of keys) await applyToIssue(key, plan)
}

/** Traduz o evento do GitHub em "quais cards" e "para qual status". */
async function buildPlan(event) {
  // Disparo manual pela aba Actions: informe o card e o status na mão.
  if (EVENT_NAME === 'workflow_dispatch') {
    const alvo = { desenvolvimento: STATUS_DEV, testes: STATUS_TEST, concluido: STATUS_DONE }
    const status = alvo[env.INPUT_STATUS || '']
    if (!status) fail(`Status inválido no disparo manual: "${env.INPUT_STATUS}".`)
    return {
      keys: extractKeys(env.INPUT_ISSUE),
      status,
      stage: 'manual', // intervenção humana: não grava selo nem respeita a trava
      parts: [{ text: `Movido manualmente pela automação do repositório ${REPO}.` }],
    }
  }

  // Push em branch de trabalho -> o card está sendo desenvolvido.
  if (EVENT_NAME === 'push') {
    const branch = (event.ref || '').replace('refs/heads/', '')
    if (branch === BRANCH_DEVELOP || branch === BRANCH_MAIN) return null

    const assuntos = (event.commits || []).map((c) => assuntoDoCommit(c.message))
    const keys = extractKeys(branch, ...assuntos, assuntoDoCommit(event.head_commit?.message))
    const sha = (event.after || '').slice(0, 7)
    return {
      keys,
      status: STATUS_DEV,
      stage: 'dev',
      parts: [
        { text: `${REPO}: novo commit ${sha} na branch `, href: undefined },
        { text: branch, href: `${SERVER_URL}/${REPO}/tree/${branch}` },
        { text: '.' },
      ],
    }
  }

  // PR fechado: só interessa se foi realmente mergeado.
  if (EVENT_NAME === 'pull_request') {
    const pr = event.pull_request || {}
    if (!pr.merged) {
      notice('PR fechado sem merge — nenhum card movido.')
      return null
    }

    const base = pr.base?.ref
    const commits = await ghTodasAsPaginas(`/repos/${REPO}/pulls/${pr.number}/commits`).catch(() => [])

    // Branch, título e assunto dos commits são fontes confiáveis. O corpo do commit e a
    // descrição do PR são texto livre e citam cards que não são deste PR ("relacionado a
    // {{PREFIXO_ISSUE_MAIUSCULO}}-99"): o corpo fica de fora sempre, e a descrição só entra se o resto não der nada.
    let keys = extractKeys(pr.head?.ref, pr.title, ...commits.map((c) => assuntoDoCommit(c.commit?.message)))
    if (!keys.length) {
      keys = extractKeys(pr.body)
      if (keys.length) {
        warn(
          `Nenhum ID na branch, no título ou nos commits do PR #${pr.number}. ` +
            `Usei o que estava na descrição: ${keys.join(', ')}. Coloque o ID no título do PR.`,
        )
      }
    }
    const prLink = { text: `PR #${pr.number}`, href: pr.html_url }

    if (base === BRANCH_DEVELOP) {
      if (REQUIRE_APPROVAL) {
        const { approved, approvers, blockers } = await pullRequestApproval(pr.number)
        if (!approved) {
          const motivo = blockers.length
            ? `há "changes requested" de ${blockers.join(', ')}`
            : 'não houve nenhum review aprovado'
          warn(
            `${REPO} PR #${pr.number} entrou na ${BRANCH_DEVELOP} sem aprovação válida (${motivo}). ` +
              `O card NÃO foi movido para "${STATUS_TEST}".`,
          )
          for (const key of keys) {
            await comment(key, [
              { text: '⚠️ ' },
              prLink,
              {
                text: ` foi mergeado na ${BRANCH_DEVELOP} sem aprovação válida (${motivo}), ` +
                  `então o card continua em desenvolvimento. Peça o review e mova a mão, ou refaça o PR.`,
              },
            ])
          }
          return null
        }
        return {
          keys,
          status: STATUS_TEST,
          stage: 'testes',
          parts: [
            prLink,
            { text: ` aprovado por ${approvers.join(', ')} e mergeado na ${BRANCH_DEVELOP} (${REPO}). Pronto para teste.` },
          ],
        }
      }
      return { keys, status: STATUS_TEST, stage: 'testes', parts: [prLink, { text: ` mergeado na ${BRANCH_DEVELOP} (${REPO}).` }] }
    }

    if (base === BRANCH_MAIN) {
      return {
        keys,
        status: STATUS_DONE,
        stage: 'entregue',
        parts: [prLink, { text: ` mergeado na ${BRANCH_MAIN} (${REPO}). Entrega concluída.` }],
      }
    }

    notice(`PR mergeado em "${base}" — branch fora do fluxo, nenhum card movido.`)
    return null
  }

  notice(`Evento "${EVENT_NAME}" não tratado.`)
  return null
}

main().catch((e) => fail(e.stack || e.message))
