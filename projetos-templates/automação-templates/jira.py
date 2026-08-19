#!/usr/bin/env python3
"""
Automacao de transicoes no Jira a partir de eventos do GitHub.

Template reutilizavel. Salve como `.github/workflows/scripts/jira.py`,
substitua os placeholders abaixo e apague este aviso.

Placeholders deste arquivo:
  {{PREFIXO_ISSUE}}             prefixo da issue, minusculo, usado na branch (ex.: sedm)
  {{PREFIXO_ISSUE_MAIUSCULO}}   mesmo prefixo, maiusculo, usado no Jira      (ex.: SEDM)
  {{JIRA_TRANSITION_ID_INICIO}}     ID da transicao para a coluna "Fazendo"/em desenvolvimento
  {{JIRA_TRANSITION_ID_ANALISE}}    ID da transicao para a coluna "Em analise"/revisao
  {{JIRA_TRANSITION_ID_CONCLUSAO}}  ID da transicao para a coluna "Feito"/concluido

Os tres IDs de transicao sao especificos do workflow configurado no board do
Jira do projeto. Para descobri-los, chame (com a mesma credencial usada por
este script):

  GET {JIRA_BASE_URL}/rest/api/3/issue/{issueKey}/transitions

e leia o campo `id` de cada transicao disponivel para uma issue naquele
estado.

Modos:
  iniciar       Push que cria uma branch nova (feature/bugfix/fix/hotfix/...)
                -> transiciona a issue para "Fazendo" ({{JIRA_TRANSITION_ID_INICIO}}).
  pr-aberto     Pull request aberto
                -> transiciona a issue para "Em analise" ({{JIRA_TRANSITION_ID_ANALISE}}).
  pr-mergeado   Pull request fechado com merge == true
                -> transiciona a issue para "Feito" ({{JIRA_TRANSITION_ID_CONCLUSAO}}).

A issue e identificada pelo nome da branch, seguindo a convencao deste
repositorio: `<tipo>/{{PREFIXO_ISSUE}}-<id>-<descricao>` (ver CLAUDE.md). Uma
unica branch corresponde a uma unica issue - o nome da branch ja e
suficiente, sem chamadas a API do GitHub.

Variaveis de ambiente (lidas apenas quando a branch bate com a convencao):
  JIRA_BASE_URL       https://{{DOMINIO_TRACKER}}
  JIRA_USER_EMAIL     Email Atlassian com permissao de transicao
  JIRA_API_TOKEN      Token gerado em id.atlassian.com -> Security -> API tokens

Filosofia: best-effort. Se a branch nao seguir a convencao `{{PREFIXO_ISSUE}}-<id>`
(ex.: push em {{BRANCH_DESENVOLVIMENTO}}/{{BRANCH_PRODUCAO}}), a automacao nao faz nada e sai com
sucesso. Falha na chamada ao Jira (rede, HTTP, transicao invalida) e logada e
reflete no exit code, mas essa run e informativa - nao e um check obrigatorio
de PR e por isso nunca trava o desenvolvimento.
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

# IDs de transicao do workflow Jira do projeto (documentados no CLAUDE.md e
# confirmados via a chamada GET .../transitions descrita no docstring acima).
TRANSITION_FAZENDO = "{{JIRA_TRANSITION_ID_INICIO}}"
TRANSITION_EM_ANALISE = "{{JIRA_TRANSITION_ID_ANALISE}}"
TRANSITION_FEITO = "{{JIRA_TRANSITION_ID_CONCLUSAO}}"

MODO_TO_TRANSITION: dict[str, str] = {
    "iniciar": TRANSITION_FAZENDO,
    "pr-aberto": TRANSITION_EM_ANALISE,
    "pr-mergeado": TRANSITION_FEITO,
}

# `feature/{{PREFIXO_ISSUE}}-16-retentativa-...` -> "{{PREFIXO_ISSUE_MAIUSCULO}}-16"
ISSUE_KEY_NA_BRANCH_REGEX = re.compile(r"{{PREFIXO_ISSUE}}-(\d+)", re.IGNORECASE)


def extrair_key_da_branch(nome_branch: str | None) -> str | None:
    """Extrai o identificador da issue a partir do nome da branch.

    Retorna None quando a branch nao segue a convencao deste repositorio
    (ex.: `{{BRANCH_DESENVOLVIMENTO}}`, `{{BRANCH_PRODUCAO}}`, ou uma branch sem
    `{{PREFIXO_ISSUE}}-<id>` no nome).
    """
    m = ISSUE_KEY_NA_BRANCH_REGEX.search(nome_branch or "")
    if not m:
        return None
    return f"{{PREFIXO_ISSUE_MAIUSCULO}}-{m.group(1)}"


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
    parser.add_argument("--branch", required=True, help="Nome da branch (ex.: feature/{{PREFIXO_ISSUE}}-16-...)")
    args = parser.parse_args(argv)

    issue_key = extrair_key_da_branch(args.branch)
    if issue_key is None:
        print(f"Branch '{args.branch}' nao segue a convencao {{PREFIXO_ISSUE}}-<id>, nada a fazer.")
        return 0

    base_url = os.environ["JIRA_BASE_URL"]
    email = os.environ["JIRA_USER_EMAIL"]
    token = os.environ["JIRA_API_TOKEN"]
    transition_id = MODO_TO_TRANSITION[args.modo]

    ok = transicionar(base_url, email, token, issue_key, transition_id)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
