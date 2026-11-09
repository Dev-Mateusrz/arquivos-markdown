"""Regressões de segurança e fluxo; API simulada, nenhuma chamada real ao Jira."""

import contextlib
import io
import os
import tempfile
import unittest
import urllib.error
from collections import deque
from pathlib import Path
from unittest.mock import MagicMock, patch

import jira


CONFIG = {
    "JIRA_PREFIXOS": "PROJ,OPS",
    "JIRA_BASE_URL": "https://jira.example.test",
    "JIRA_USER_EMAIL": "bot@example.test",
    "JIRA_API_TOKEN": "token-ficticio",
    "JIRA_STATUS_INICIAIS": "1,2",
    "JIRA_STATUS_FAZENDO": "3",
    "JIRA_STATUS_ANALISE": "4",
    "JIRA_STATUS_FEITO": "5",
    "JIRA_TRANSITION_ID_INICIO": "11",
    "JIRA_TRANSITION_ID_ANALISE": "21",
    "JIRA_TRANSITION_ID_CONCLUSAO": "31",
    "JIRA_CAMPO_CONCLUSAO": "customfield_12345",
    "JIRA_VALOR_CONCLUSAO": "Liberado",
    "GITHUB_REPOSITORY": "org/repo",
    "GITHUB_RUN_ID": "123",
}
PR = "https://github.com/org/repo/pull/7"
BRANCH = "feature/proj-42-validar-acesso"


def estado(status="1", valor=None, categoria="indeterminate"):
    return {"fields": {
        "status": {"id": status, "statusCategory": {"key": categoria}},
        "customfield_12345": valor,
    }}


class JiraSimulado:
    def __init__(self, estados, transicao="11", destino="3"):
        self.estados = deque(estados)
        self.transicoes = [{"id": transicao, "to": {"id": destino}}]
        self.chamadas = []

    def request(self, metodo, caminho, dados=None):
        self.chamadas.append((metodo, caminho, dados))
        if metodo == "GET" and "?" in caminho:
            resposta = self.estados.popleft()
            if isinstance(resposta, Exception):
                raise resposta
            return resposta
        if metodo == "GET":
            return {"transitions": self.transicoes}
        return {}

    @property
    def escritas(self):
        return [c for c in self.chamadas if c[0] == "POST"]


class AutomacaoTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, CONFIG, clear=True)
        self.env.start()
        self.addCleanup(self.env.stop)

    def executar(self, modo, fake=None, branch=BRANCH, pr_url=PR):
        with patch.object(jira, "Jira", return_value=fake) as construtor:
            with contextlib.redirect_stdout(io.StringIO()) as saida:
                codigo = jira.main([modo, "--branch", branch, "--pr-url", pr_url])
        self.assertEqual(codigo, 0)
        return saida.getvalue(), construtor

    def test_multiplos_prefixos_e_caixa(self):
        for branch, key in [(BRANCH, "PROJ-42"), ("fix/OPS-9-ajustar", "OPS-9")]:
            with self.subTest(branch=branch):
                self.assertEqual(jira.extrair_key_da_branch(branch), key)

    def test_branch_invalida_ambigua_ou_nao_autorizada(self):
        for branch in [None, "main", "release/proj-42-entregar", "fix/OUTRO-1-ajustar",
                       "fix/xproj-42-ajustar", "fix/proj-0-ajustar", "fix/proj-042-ajustar",
                       "fix/proj-42", "fix/proj-42-ajustar-ops-7", "fix/proj-42-proj-42",
                       'fix/proj-42-$(comando)', "fix/proj-42-ajustar\n"]:
            with self.subTest(branch=branch):
                self.assertIsNone(jira.extrair_key_da_branch(branch))

    def test_tipo_customizado(self):
        os.environ["JIRA_TIPOS_BRANCH"] = "delivery"
        self.assertEqual(jira.extrair_key_da_branch("delivery/ops-1-implementar"), "OPS-1")
        self.assertIsNone(jira.extrair_key_da_branch(BRANCH))

    def test_sem_prefixos_nao_acessa_api(self):
        del os.environ["JIRA_PREFIXOS"]
        _, construtor = self.executar("iniciar")
        construtor.assert_not_called()

    def test_sem_secrets_nao_acessa_api(self):
        for nome in ("JIRA_BASE_URL", "JIRA_USER_EMAIL", "JIRA_API_TOKEN"):
            with self.subTest(nome=nome), patch.dict(os.environ, {nome: ""}):
                saida, construtor = self.executar("iniciar")
                construtor.assert_not_called()
                self.assertIn("ausentes", saida)

    def test_branch_ignorada_antes_das_credenciais(self):
        _, construtor = self.executar("iniciar", branch="main")
        construtor.assert_not_called()

    def test_origem_https_sem_caminho_nem_credenciais(self):
        self.assertEqual(jira.validar_base_url("https://jira.example.test/"), CONFIG["JIRA_BASE_URL"])
        for url in ["http://jira.test", "https://user:token@jira.test", "https://jira.test/browse",
                    "https://jira.test?token=segredo", "https://jira.test#fragmento"]:
            with self.subTest(url=url), self.assertRaises(jira.ErroIntegracao):
                jira.validar_base_url(url)

    def test_id_invalido_nao_consulta_api(self):
        os.environ["JIRA_TRANSITION_ID_INICIO"] = "{{ID}}"
        fake = JiraSimulado([])
        self.executar("iniciar", fake)
        self.assertEqual(fake.chamadas, [])

    def test_etapas_sobrepostas_sao_recusadas(self):
        os.environ["JIRA_STATUS_INICIAIS"] = "1,4"
        with self.assertRaises(jira.ErroIntegracao):
            jira.carregar_regra("iniciar")

    def test_inicio_avanca_somente_de_status_inicial(self):
        for status in ("1", "2"):
            with self.subTest(status=status):
                fake = JiraSimulado([estado(status), estado(status)])
                jira.tentar_transicao(fake, "PROJ-42", "iniciar", jira.carregar_regra("iniciar"))
                self.assertEqual(fake.escritas, [
                    ("POST", "/issue/PROJ-42/transitions", {"transition": {"id": "11"}})])

    def test_inicio_atrasado_nao_regride_card(self):
        for status, categoria in [("3", "indeterminate"), ("4", "indeterminate"),
                                  ("5", "done"), ("99", "indeterminate")]:
            with self.subTest(status=status):
                fake = JiraSimulado([estado(status, categoria=categoria)])
                jira.tentar_transicao(fake, "PROJ-42", "iniciar", jira.carregar_regra("iniciar"))
                self.assertEqual(fake.escritas, [])

    def test_categoria_done_nao_reabre_mesmo_com_origem_configurada(self):
        fake = JiraSimulado([estado("1", categoria="done")])
        jira.tentar_transicao(fake, "PROJ-42", "iniciar", jira.carregar_regra("iniciar"))
        self.assertEqual(fake.escritas, [])

    def test_pr_pode_iniciar_revisao_de_a_fazer_ou_fazendo(self):
        for status in ("1", "2", "3"):
            with self.subTest(status=status):
                fake = JiraSimulado([estado(status), estado(status)], "21", "4")
                jira.tentar_transicao(fake, "PROJ-42", "pr-aberto", jira.carregar_regra("pr-aberto"))
                self.assertEqual(fake.escritas[0][2], {"transition": {"id": "21"}})

    def test_merge_pendente_comenta_frente_sem_concluir(self):
        fake = JiraSimulado([estado("4", "Pendente")])
        saida, _ = self.executar("pr-mergeado", fake)
        self.assertIn("pendente", saida)
        self.assertEqual(len(fake.escritas), 1)
        self.assertTrue(fake.escritas[0][1].endswith("/comment"))
        comentario = fake.escritas[0][2]["body"]
        self.assertEqual(comentario["type"], "doc")
        texto = str(comentario)
        self.assertIn(PR, texto)
        self.assertIn("org/repo", texto)
        self.assertIn("/actions/runs/123", texto)

    def test_merge_sem_valor_explicito_nunca_conclui(self):
        for valor in (None, "", "liberado", "Pendente", True, ["Liberado"], {"id": "1"}):
            with self.subTest(valor=valor):
                fake = JiraSimulado([estado("4", valor)])
                jira.tentar_transicao(fake, "PROJ-42", "pr-mergeado", jira.carregar_regra("pr-mergeado"))
                self.assertEqual(fake.escritas, [])

    def test_merge_sem_configuracao_de_trava_nao_conclui(self):
        for nome in ("JIRA_CAMPO_CONCLUSAO", "JIRA_VALOR_CONCLUSAO"):
            with self.subTest(nome=nome), patch.dict(os.environ, {nome: ""}):
                fake = JiraSimulado([estado("4", "Liberado")])
                jira.tentar_transicao(fake, "PROJ-42", "pr-mergeado", jira.carregar_regra("pr-mergeado"))
                self.assertEqual(fake.escritas, [])

    def test_merge_liberado_aceita_texto_ou_selecao_unica(self):
        for valor in ("Liberado", {"value": "Liberado"}):
            with self.subTest(valor=valor):
                fake = JiraSimulado([estado("4", valor), estado("4", valor)], "31", "5")
                jira.tentar_transicao(fake, "PROJ-42", "pr-mergeado", jira.carregar_regra("pr-mergeado"))
                self.assertEqual(fake.escritas[0][2], {"transition": {"id": "31"}})

    def test_merge_nao_pula_etapa_de_revisao(self):
        fake = JiraSimulado([estado("3", "Liberado")])
        jira.tentar_transicao(fake, "PROJ-42", "pr-mergeado", jira.carregar_regra("pr-mergeado"))
        self.assertEqual(fake.escritas, [])

    def test_transicao_indisponivel_destino_incorreto_ou_resposta_invalida(self):
        for transicoes in ([], [{"id": "11", "to": {"id": "99"}}],
                           [{"id": "11", "to": "inválido"}], "inválido"):
            with self.subTest(transicoes=transicoes):
                fake = JiraSimulado([estado()])
                fake.transicoes = transicoes
                self.executar("iniciar", fake)
                self.assertTrue(all(c[1].endswith("/comment") for c in fake.escritas))

    def test_mudanca_concorrente_de_status_aborta_escrita(self):
        fake = JiraSimulado([estado("1"), estado("4")])
        resultado = jira.tentar_transicao(fake, "PROJ-42", "iniciar", jira.carregar_regra("iniciar"))
        self.assertIn("alterado", resultado)
        self.assertEqual(fake.escritas, [])

    def test_revogacao_concorrente_da_liberacao_aborta_conclusao(self):
        fake = JiraSimulado([estado("4", "Liberado"), estado("4", "Pendente")], "31", "5")
        jira.tentar_transicao(fake, "PROJ-42", "pr-mergeado", jira.carregar_regra("pr-mergeado"))
        self.assertEqual(fake.escritas, [])

    def test_resposta_sem_status_valido_nao_transiciona(self):
        for resposta in ({}, {"fields": None}, {"fields": {"status": {"id": "1"}}}):
            with self.subTest(resposta=resposta):
                fake = JiraSimulado([resposta])
                self.executar("iniciar", fake)
                self.assertTrue(all(c[1].endswith("/comment") for c in fake.escritas))

    def test_falha_de_transicao_ainda_tenta_comentar_evento(self):
        fake = JiraSimulado([jira.ErroIntegracao("Jira respondeu HTTP 503.")])
        saida, _ = self.executar("pr-mergeado", fake)
        self.assertIn("503", saida)
        self.assertTrue(fake.escritas[0][1].endswith("/comment"))

    def test_falha_do_comentario_continua_best_effort(self):
        fake = MagicMock()
        fake.request.side_effect = jira.ErroIntegracao("Jira respondeu HTTP 403.")
        saida, _ = self.executar("pr-mergeado", fake)
        self.assertIn("best-effort", saida)

    def test_pr_sem_link_recusado_antes_de_qualquer_escrita(self):
        fake = JiraSimulado([])
        self.executar("pr-mergeado", fake, pr_url="")
        self.assertEqual(fake.chamadas, [])

    def test_resumo_do_github_liga_issue_ao_evento(self):
        fake = JiraSimulado([estado("4", "Pendente")])
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "summary.md"
            os.environ["GITHUB_STEP_SUMMARY"] = str(caminho)
            self.executar("pr-mergeado", fake)
            self.assertIn("[PROJ-42](https://jira.example.test/browse/PROJ-42)", caminho.read_text(encoding="utf-8"))

    def test_http_timeout_json_e_redirect_sao_best_effort_sem_vazar_resposta(self):
        cliente = jira.Jira(CONFIG["JIRA_BASE_URL"], CONFIG["JIRA_USER_EMAIL"], CONFIG["JIRA_API_TOKEN"])
        for falha in (TimeoutError("segredo"), urllib.error.URLError("segredo"),
                      urllib.error.HTTPError("https://jira.test", 429, "segredo", {}, io.BytesIO(b"segredo"))):
            with self.subTest(falha=type(falha).__name__):
                with patch.object(cliente.opener, "open", side_effect=falha):
                    with self.assertRaises(jira.ErroIntegracao) as erro:
                        cliente.request("GET", "/issue/PROJ-42")
                self.assertNotIn("segredo", str(erro.exception))
        for corpo in (b"segredo", b"[]"):
            with self.subTest(corpo=corpo):
                response = MagicMock()
                response.__enter__.return_value.read.return_value = corpo
                with patch.object(cliente.opener, "open", return_value=response):
                    with self.assertRaises(jira.ErroIntegracao):
                        cliente.request("GET", "/issue/PROJ-42")
        self.assertIsNone(jira.SemRedirecionamento().redirect_request(None, None, 302, "", {}, "https://outro.test"))


if __name__ == "__main__":
    unittest.main()
