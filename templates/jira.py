#!/usr/bin/env python3
"""
Automacao de transicoes no Jira a partir de eventos do GitHub.

Para que serve: recebe o modo (iniciar/pr-aberto/pr-mergeado) e o nome da
branch do workflow jira-automation.yml, extrai o identificador da issue do
nome da branch e chama a API do Jira para mover o card de status.

Template reutilizavel. Copie para .github/workflows/scripts/jira.py,
preencha as constantes marcadas com <PLACEHOLDER> logo abaixo e apague
este parágrafo. Chamado pelo workflow jira-automation.yml deste mesmo
diretorio de templates.

Modos:
  iniciar       Push que cria uma branch nova (feature/bugfix/fix/hotfix/...)
                -> transiciona a issue para o status "Em andamento".
  pr-aberto     Pull request aberto
                -> transiciona a issue para o status "Em revisao".
  pr-mergeado   Pull request fechado com merge == true
                -> transiciona a issue para o status "Concluido".

A issue e identificada pelo nome da branch, seguindo a convencao
`<tipo>/<prefixo-issue>-<id>-<descricao>` (ver CLAUDE.md do projeto). Uma
unica branch corresponde a uma unica issue - o nome da branch ja e
suficiente, sem chamadas a API do GitHub.

Variaveis de ambiente (lidas apenas quando a branch bate com a convencao):
  JIRA_BASE_URL       URL base do Jira, ex: https://sua-organizacao.atlassian.net
  JIRA_USER_EMAIL     Email Atlassian com permissao de transicao
  JIRA_API_TOKEN      Token gerado em id.atlassian.com -> Security -> API tokens

Filosofia: best-effort. Se a branch nao seguir a convencao de prefixo (ex.:
push em develop/master), a automacao nao faz nada e sai com sucesso. Falha
na chamada ao Jira (rede, HTTP, transicao invalida) e logada e reflete no
exit code, mas essa run e informativa - nao e um check obrigatorio de PR e
por isso nunca trava o desenvolvimento.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request

# <PLACEHOLDER> — prefixo de issue usado no nome das branches deste
# repositorio (o mesmo {{PREFIXO_ISSUE}} do CLAUDE.md), em minusculo.
# Exemplo: `feature/sa-16-retentativa-...` -> "SA-16" se ISSUE_KEY_PREFIX = "sa"
ISSUE_KEY_PREFIX = "<PREFIXO_ISSUE>"

# <PLACEHOLDER> — IDs de transicao do workflow Jira do projeto. Sao
# especificos de cada projeto: descubra-os chamando
# GET /rest/api/3/issue/{key}/transitions em uma issue real, nunca adivinhe.
TRANSITION_EM_ANDAMENTO = "<ID_TRANSICAO_EM_ANDAMENTO>"
TRANSITION_EM_REVISAO = "<ID_TRANSICAO_EM_REVISAO>"
TRANSITION_CONCLUIDO = "<ID_TRANSICAO_CONCLUIDO>"

MODO_TO_TRANSITION: dict[str, str] = {
    "iniciar": TRANSITION_EM_ANDAMENTO,
    "pr-aberto": TRANSITION_EM_REVISAO,
    "pr-mergeado": TRANSITION_CONCLUIDO,
}

# `feature/<prefixo>-16-retentativa-...` -> "<PREFIXO>-16"
ISSUE_KEY_NA_BRANCH_REGEX = re.compile(
    rf"{re.escape(ISSUE_KEY_PREFIX)}-(\d+)", re.IGNORECASE
)


def extrair_key_da_branch(nome_branch: str | None) -> str | None:
    """Extrai o identificador da issue a partir do nome da branch.

    Retorna None quando a branch nao segue a convencao deste repositorio
    (ex.: `develop`, `master`, ou uma branch sem `<prefixo>-<id>` no nome).
    """
    m = ISSUE_KEY_NA_BRANCH_REGEX.search(nome_branch or "")
    if not m:
        return None
    return f"{ISSUE_KEY_PREFIX.upper()}-{m.group(1)}"


def _basic_auth_header(email: str, token: str) -> str:
    raw = f"{email}:{token}".encode()
    return "Basic " + base64.b64encode(raw).decode()


def transicionar(base_url: str, email: str, token: str, issue_key: str, transition_id: str) -> bool:
    url = f"{base_url.rstrip('/')}/rest/api/3/issue/{issue_key}/transitions"
    data = json.dumps({"transition": {"id": transition_id}}).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", _basic_auth_header(email, token))
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"OK {issue_key} -> transition {transition_id} (HTTP {resp.getcode()})")
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        print(f"FALHA {issue_key} -> transition {transition_id} (HTTP {e.code}): {body}")
        return False
    except urllib.error.URLError as e:
        print(f"FALHA {issue_key} -> transition {transition_id}: network error: {e.reason}")
        return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Transiciona a issue Jira correspondente a branch.")
    parser.add_argument("modo", choices=sorted(MODO_TO_TRANSITION))
    parser.add_argument("--branch", required=True, help="Nome da branch (ex.: feature/<prefixo>-16-...)")
    args = parser.parse_args(argv)

    issue_key = extrair_key_da_branch(args.branch)
    if issue_key is None:
        print(f"Branch '{args.branch}' nao segue a convencao {ISSUE_KEY_PREFIX}-<id>, nada a fazer.")
        return 0

    base_url = os.environ["JIRA_BASE_URL"]
    email = os.environ["JIRA_USER_EMAIL"]
    token = os.environ["JIRA_API_TOKEN"]
    transition_id = MODO_TO_TRANSITION[args.modo]

    ok = transicionar(base_url, email, token, issue_key, transition_id)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
