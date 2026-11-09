#!/usr/bin/env python3
"""Jira Cloud REST v3, Python 3.10+, somente biblioteca padrão.

Copie sem alterações para .github/workflows/scripts/jira.py em cada repositório.
Configure secrets/variables conforme README.md deste conjunto de templates.
A branch identifica uma única issue; nenhuma consulta ao GitHub é necessária.
Falhas de integração são informativas e retornam zero (best-effort).
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass


MODOS = ("iniciar", "pr-aberto", "pr-mergeado")
TIPOS_BRANCH = "feat,feature,bugfix,fix,hotfix,chore,docs,refactor,test,perf,ci,build"


class ErroIntegracao(Exception):
    """Erro esperado, sem conteúdo de respostas ou credenciais nos logs."""


def lista_env(nome: str, padrao: str = "") -> list[str]:
    return [item.strip() for item in os.environ.get(nome, padrao).split(",") if item.strip()]


def extrair_key_da_branch(nome_branch: str | None) -> str | None:
    """Aceita apenas tipo/PREFIXO-numero-descricao e prefixos autorizados."""
    prefixos = lista_env("JIRA_PREFIXOS")
    tipos = lista_env("JIRA_TIPOS_BRANCH", TIPOS_BRANCH)
    if not prefixos or not tipos:
        return None
    if any(not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", p) for p in prefixos):
        raise ErroIntegracao("JIRA_PREFIXOS inválido; use chaves separadas por vírgula.")
    alternativa = "|".join(re.escape(p) for p in prefixos)
    chaves = re.findall(rf"(?<![A-Za-z0-9_])({alternativa})-([1-9][0-9]*)(?![0-9])",
                        nome_branch or "", re.IGNORECASE)
    # Evita vincular por acidente uma branch com duas chaves, mesmo repetidas.
    if len(chaves) != 1:
        return None
    padrao = rf"({'|'.join(re.escape(t) for t in tipos)})/({alternativa})-([1-9][0-9]*)-[a-z0-9]+(?:-[a-z0-9]+)*"
    match = re.fullmatch(padrao, nome_branch or "", re.IGNORECASE)
    return f"{match[2].upper()}-{match[3]}" if match else None


def validar_base_url(valor: str) -> str:
    url = urllib.parse.urlsplit(valor)
    if (url.scheme != "https" or not url.hostname or url.username or url.password
            or url.path not in ("", "/") or url.query or url.fragment):
        raise ErroIntegracao("JIRA_BASE_URL deve ser a origem HTTPS, sem caminho ou credenciais.")
    return valor.rstrip("/")


class SemRedirecionamento(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Nunca encaminhar Authorization para outro destino.
        return None


class Jira:
    def __init__(self, base_url: str, email: str, token: str):
        self.base_url = base_url
        self.auth = "Basic " + base64.b64encode(f"{email}:{token}".encode()).decode()
        self.opener = urllib.request.build_opener(SemRedirecionamento())

    def request(self, metodo: str, caminho: str, dados: dict | None = None) -> dict:
        request = urllib.request.Request(
            self.base_url + "/rest/api/3" + caminho,
            data=json.dumps(dados).encode() if dados is not None else None,
            method=metodo,
            headers={"Authorization": self.auth, "Accept": "application/json",
                     "Content-Type": "application/json"},
        )
        try:
            with self.opener.open(request, timeout=15) as response:
                corpo = response.read()
                resultado = json.loads(corpo) if corpo else {}
                if not isinstance(resultado, dict):
                    raise ErroIntegracao("Resposta inesperada do Jira; operação interrompida.")
                return resultado
        except urllib.error.HTTPError as erro:
            raise ErroIntegracao(f"Jira respondeu HTTP {erro.code}; sem retentativa automática.") from None
        except (urllib.error.URLError, OSError, ValueError):
            raise ErroIntegracao("Falha de rede, timeout ou JSON inválido; sem retentativa automática.") from None


@dataclass(frozen=True)
class Regra:
    transicao: str
    destino: str
    origens: frozenset[str]
    campo_conclusao: str
    valor_conclusao: str


def carregar_regra(modo: str) -> Regra:
    iniciais = lista_env("JIRA_STATUS_INICIAIS")
    fazendo = os.environ.get("JIRA_STATUS_FAZENDO", "").strip()
    analise = os.environ.get("JIRA_STATUS_ANALISE", "").strip()
    feito = os.environ.get("JIRA_STATUS_FEITO", "").strip()
    sufixo, destino, origens = {
        "iniciar": ("INICIO", fazendo, iniciais),
        "pr-aberto": ("ANALISE", analise, [*iniciais, fazendo]),
        "pr-mergeado": ("CONCLUSAO", feito, [analise]),
    }[modo]
    transicao = os.environ.get(f"JIRA_TRANSITION_ID_{sufixo}", "").strip()
    ids = [*iniciais, fazendo, analise, feito, transicao]
    if not iniciais or any(not re.fullmatch(r"[0-9]+", valor) for valor in ids):
        raise ErroIntegracao("Configure IDs numéricos de status e a transição deste modo.")
    if len(set([fazendo, analise, feito])) != 3 or set(iniciais) & {fazendo, analise, feito}:
        raise ErroIntegracao("Status iniciais, Fazendo, Em análise e Feito devem ser distintos.")
    campo = os.environ.get("JIRA_CAMPO_CONCLUSAO", "").strip()
    valor = os.environ.get("JIRA_VALOR_CONCLUSAO", "").strip()
    if campo and not re.fullmatch(r"customfield_[0-9]+", campo):
        raise ErroIntegracao("JIRA_CAMPO_CONCLUSAO deve ter o formato customfield_12345.")
    return Regra(transicao, destino, frozenset(origens), campo, valor)


def obter_estado(jira: Jira, key: str, regra: Regra) -> tuple[str, bool, bool]:
    campos = "status" + ("," + regra.campo_conclusao if regra.campo_conclusao else "")
    dados = jira.request("GET", f"/issue/{key}?" + urllib.parse.urlencode({"fields": campos}))
    fields = dados.get("fields")
    if not isinstance(fields, dict) or not isinstance(fields.get("status"), dict):
        raise ErroIntegracao("Resposta sem campos/status válidos; status preservado.")
    status = fields["status"]
    categoria = status.get("statusCategory")
    if not status.get("id") or not isinstance(categoria, dict) or not categoria.get("key"):
        raise ErroIntegracao("Resposta sem ID/categoria de status; status preservado.")
    valor = fields.get(regra.campo_conclusao)
    # Suporta texto de linha única ou seleção única; listas/ADF não liberam.
    if isinstance(valor, dict):
        valor = valor.get("value")
    liberado = bool(regra.campo_conclusao and regra.valor_conclusao
                    and isinstance(valor, str) and valor == regra.valor_conclusao)
    return str(status["id"]), categoria["key"] == "done", liberado


def tentar_transicao(jira: Jira, key: str, modo: str, regra: Regra) -> str:
    atual, encerrado, liberado = obter_estado(jira, key, regra)
    if atual == regra.destino:
        return "Status de destino já atingido; nenhuma transição enviada."
    if encerrado or atual not in regra.origens:
        return "Status preservado: origem fora das permitidas para este evento."
    if modo == "pr-mergeado" and not liberado:
        return "Frente mergeada; conclusão global pendente de liberação explícita no Jira."
    transicoes = jira.request("GET", f"/issue/{key}/transitions").get("transitions", [])
    if not isinstance(transicoes, list) or any(not isinstance(t, dict) for t in transicoes):
        raise ErroIntegracao("Resposta sem transições válidas; status preservado.")
    valida = any(str(t.get("id")) == regra.transicao
                 and isinstance(t.get("to"), dict)
                 and str(t["to"].get("id")) == regra.destino for t in transicoes)
    if not valida:
        return "Transição indisponível ou destino divergente; status preservado."
    # Reduz a janela de concorrência; validadores no Jira são a autoridade final.
    recente, encerrado, liberado = obter_estado(jira, key, regra)
    if recente != atual or encerrado or (modo == "pr-mergeado" and not liberado):
        return "Estado alterado durante a execução; status preservado para reconciliação."
    jira.request("POST", f"/issue/{key}/transitions", {"transition": {"id": regra.transicao}})
    return f"Transição {regra.transicao} aplicada; status de destino {regra.destino}."


def registrar_evento(jira: Jira, key: str, modo: str, branch: str, resultado: str, pr_url: str) -> None:
    repo = os.environ.get("GITHUB_REPOSITORY", "execução local")
    evento = {"iniciar": "Implementação iniciada", "pr-aberto": "Revisão iniciada",
              "pr-mergeado": "Frente do repositório concluída por merge"}[modo]
    linhas = [f"{evento} — {repo}", f"Issue: {key}; branch: {branch}", resultado]
    if pr_url:
        linhas.append("PR: " + pr_url)
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com").rstrip("/")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    if run_id and repo != "execução local":
        linhas.append(f"Execução: {server}/{repo}/actions/runs/{run_id}")
    conteudo = []
    for linha in linhas:
        node = {"type": "text", "text": linha}
        if linha.startswith(("PR: ", "Execução: ")):
            node["marks"] = [{"type": "link", "attrs": {"href": linha.split(": ", 1)[1]}}]
        conteudo.append({"type": "paragraph", "content": [node]})
    jira.request("POST", f"/issue/{key}/comment",
                 {"body": {"type": "doc", "version": 1, "content": conteudo}})


def executar(args: argparse.Namespace) -> None:
    key = extrair_key_da_branch(args.branch)
    if key is None:
        print("IGNORADO: branch sem uma única issue autorizada ou configuração de prefixos ausente.")
        return
    print(f"Issue identificada por convenção: {key}.")
    nomes = ("JIRA_BASE_URL", "JIRA_USER_EMAIL", "JIRA_API_TOKEN")
    valores = [os.environ.get(nome, "").strip() for nome in nomes]
    ausentes = [nome for nome, valor in zip(nomes, valores) if not valor]
    if ausentes:
        print("IGNORADO: credenciais/configuração ausentes: " + ", ".join(ausentes))
        return
    base_url = validar_base_url(valores[0])
    jira = Jira(base_url, valores[1], valores[2])
    regra = carregar_regra(args.modo)
    # O link do PR é obrigatório para não perder rastreabilidade no fechamento.
    if args.modo != "iniciar" and not re.fullmatch(r"https://[^\s/?#]+/[^\s/?#]+/[^\s/?#]+/pull/[1-9][0-9]*", args.pr_url):
        raise ErroIntegracao("Informe --pr-url com a URL HTTPS do pull request.")
    resumo = os.environ.get("GITHUB_STEP_SUMMARY", "")
    if resumo:
        try:
            with open(resumo, "a", encoding="utf-8") as arquivo:
                arquivo.write(f"\nIssue Jira: [{key}]({base_url}/browse/{key}) · evento `{args.modo}`\n")
        except OSError:
            print("AVISO: não foi possível gravar o link da issue no resumo do GitHub.")
    try:
        resultado = tentar_transicao(jira, key, args.modo, regra)
    except ErroIntegracao as erro:
        # Mesmo se a transição falhar, tenta preservar o evento e o link do PR.
        resultado = f"AVISO: {erro} Status não confirmado; verificar no Jira."
    print(f"{key}: {resultado}")
    registrar_evento(jira, key, args.modo, args.branch, resultado, args.pr_url)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("modo", choices=MODOS)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--pr-url", default="")
    args = parser.parse_args(argv)
    try:
        executar(args)
    except (ErroIntegracao, ValueError) as erro:
        # ValueError externo pode conter dados da configuração: não o reproduzir.
        mensagem = str(erro) if isinstance(erro, ErroIntegracao) else "Configuração ou resposta inválida."
        print(f"AVISO best-effort: {mensagem}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
