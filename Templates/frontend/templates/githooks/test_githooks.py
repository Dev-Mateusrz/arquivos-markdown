"""Testa os templates em repositórios descartáveis, sem alterar o Git desta biblioteca."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parent
GIT = shutil.which("git")
NODE = shutil.which("node")
SH = shutil.which("sh") or next((str(p) for p in (
    Path("C:/Program Files/Git/usr/bin/sh.exe"),
    Path("C:/Program Files/Git/bin/sh.exe"),
) if p.exists()), None)


@unittest.skipUnless(GIT and NODE and SH, "Git, Node e shell POSIX são necessários")
class HooksTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hooks com espaços ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.hooks = self.root / ".githooks"
        self.hooks.mkdir()
        self.env = os.environ.copy()
        for name in ("SKIP_GIT_HOOKS", "ALLOW_DIRECT_PUSH", "HOOK_PACKAGE_MANAGER", "JIRA_PROJECT_KEY", "CI",
                     "SKIP_DEPENDENCY_AUDIT", "AUTO_INSTALL_AFTER_MERGE", "HOOK_INSTALL_SCRIPTS",
                     "HOOK_TEST_STATUS", "HOOK_TEST_FAIL_SCRIPT"):
            self.env.pop(name, None)
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=str(self.root / "no-global"))
        mapping = {
            "config-frontend.txt": "config.sh",
            "pre-commit-frontend.txt": "pre-commit",
            "prepare-commit-msg-frontend.txt": "prepare-commit-msg",
            "commit-msg-frontend.txt": "commit-msg",
            "pre-push-frontend.txt": "pre-push",
            "post-merge-frontend.txt": "post-merge",
            "install.mjs.txt": "install.mjs",
        }
        for source, name in mapping.items():
            text = (SOURCE / source).read_text(encoding="utf-8")
            for old, new in (("{{PREFIXO_ISSUE_MAIUSCULO}}", "SMS"),
                             ("{{BRANCH_PRODUCAO}}", "main"),
                             ("{{BRANCH_DESENVOLVIMENTO}}", "develop")):
                text = text.replace(old, new)
            (self.hooks / name).write_text(text, encoding="utf-8", newline="\n")
        self.bin = self.root / "bin"
        self.bin.mkdir()
        manager = self.bin / "npm"
        manager.write_text(
            '#!/bin/sh\nprintf "%s\\n" "$*" >> "$HOOK_TEST_LOG"\n'
            'if IFS= read -r line; then exit 9; fi\n'
            'if [ -n "${HOOK_TEST_FAIL_SCRIPT:-}" ] && [ "${2:-}" = "$HOOK_TEST_FAIL_SCRIPT" ]; then exit 7; fi\n'
            'exit "${HOOK_TEST_STATUS:-0}"\n',
            encoding="utf-8", newline="\n")
        manager.chmod(0o755)
        shutil.copy2(manager, self.bin / "pnpm")
        self.log = self.root / "checks.log"
        self.env["HOOK_TEST_LOG"] = self.log.as_posix()
        # Git acrescenta suas ferramentas POSIX ao invocar hooks. Reproduz isso
        # nas chamadas diretas do shell, inclusive a partir de PowerShell.
        self.env["PATH"] = os.pathsep.join((str(self.bin), str(Path(SH).parent), self.env["PATH"]))
        self.git("init", "-q", "-b", "feature/SMS-42-exemplo")
        self.git("config", "user.name", "Hook Tests")
        self.git("config", "user.email", "hooks@example.test")
        self.git("commit", "-q", "--allow-empty", "-m", "feat(SMS-1): inicializa teste")
        self.message = self.root / "mensagem com espaços.txt"

    def run_command(self, args, *, input="", ok=True, env=None):
        result = subprocess.run(args, cwd=self.root, env=env or self.env, input=input,
                                text=True, encoding="utf-8", capture_output=True)
        if ok:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def git(self, *args, **kwargs):
        return self.run_command([GIT, *args], **kwargs)

    def hook(self, name, *, message=None, source=None, input="", ok=True, env=None):
        args = [SH, (self.hooks / name).as_posix()]
        if message is not None:
            self.message.write_text(message, encoding="utf-8", newline="\n")
            args.append(self.message.as_posix())
        if source is not None:
            args.append(source)
        return self.run_command(args, input=input, ok=ok, env=env)

    def prepare(self, text, source=None):
        self.hook("prepare-commit-msg", message=text, source=source)
        return self.message.read_text(encoding="utf-8")

    def push_line(self, destination, sha="a" * 40):
        return f"HEAD {sha} {destination} {'b' * len(sha)}\n"

    def test_sintaxe_posix_dos_quatro_hooks_e_config(self):
        for name in ("config.sh", "pre-commit", "prepare-commit-msg", "commit-msg", "pre-push", "post-merge"):
            with self.subTest(name=name):
                self.run_command([SH, "-n", str(self.hooks / name)])

    def test_preparo_preserva_tipo_escrito_e_breaking_change(self):
        for original, expected in (("fix: corrige cadastro", "fix(SMS-42): corrige cadastro\n"),
                                   ("feat!: muda contrato", "feat(SMS-42)!: muda contrato\n")):
            with self.subTest(original=original):
                self.assertEqual(self.prepare(original), expected)

    def test_preparo_vazio_e_comentarios(self):
        text = self.prepare("# instrução sem chave\n")
        self.assertEqual(text, "feat(SMS-42): \n# instrução sem chave\n")

    def test_escopo_existente_recebe_trailer_idempotente(self):
        once = self.prepare("feat(ui): cria cadastro\n\nCorpo preservado\n")
        self.assertIn("feat(ui): cria cadastro", once)
        self.assertEqual(once.count("Refs: SMS-42"), 1)
        self.assertEqual(self.prepare(once), once)

    def test_mensagem_nao_convencional_recebe_refs_mas_e_recusada(self):
        text = self.prepare("mensagem sem padrão")
        self.assertIn("Refs: SMS-42", text)
        self.assertNotEqual(self.hook("commit-msg", message=text, ok=False).returncode, 0)

    def test_chave_existente_e_preservada(self):
        text = "feat(SMS-420): mantém chave explícita\n"
        self.assertEqual(self.prepare(text), text)

    def test_comentario_nao_conta_como_chave(self):
        text = self.prepare("feat: cria cadastro\n# SMS-42 apenas comentário\n")
        self.assertTrue(text.startswith("feat(SMS-42):"))
        result = self.hook("commit-msg", message="feat: cria cadastro\n# SMS-42\n", ok=False)
        self.assertNotEqual(result.returncode, 0)

    def test_comment_char_customizado_e_linhas_iniciais(self):
        self.git("config", "core.commentChar", ";")
        text = self.prepare("; instruções\n\nfix: corrige cadastro\n")
        self.assertIn("fix(SMS-42): corrige cadastro", text)
        self.hook("commit-msg", message=text)

    def test_fontes_geradas_nao_sao_reescritas(self):
        for source in ("merge", "squash", "commit"):
            with self.subTest(source=source):
                text = "mensagem histórica sem padrão\n"
                self.assertEqual(self.prepare(text, source), text)

    def test_autosquash_e_revert_preservados(self):
        for text in ('Revert "mudança anterior"\n', 'fixup! feat: corrige teste\n',
                     'squash! feat: corrige teste\n', 'amend! feat: corrige teste\n'):
            with self.subTest(text=text):
                self.assertEqual(self.prepare(text), text)
                self.hook("commit-msg", message=text)

    def test_merge_generico_nao_recebe_isencao_por_prefixo(self):
        self.assertNotEqual(self.hook("commit-msg", message="Merge qualquer coisa", ok=False).returncode, 0)
        (self.root / ".git/MERGE_HEAD").write_text("a" * 40 + "\n")
        self.hook("commit-msg", message="Merge branch 'outra'")

    def test_squash_gerado_e_reconhecido(self):
        (self.root / ".git/SQUASH_MSG").write_text("Squashed commit\n")
        self.hook("commit-msg", message="Squashed commit of the following:")

    def test_amend_com_mensagem_normal_continua_validado(self):
        text = self.prepare("título inválido", "commit")
        self.assertNotEqual(self.hook("commit-msg", message=text, ok=False).returncode, 0)

    def test_branch_sem_chave_ambigua_ou_detached_nao_injeta(self):
        for branch in ("main", "feature/SMS-0-teste", "feature/XSMS-42-teste",
                       "feature/SMS-42-teste-SMS-43", "release/SMS-42-teste"):
            with self.subTest(branch=branch):
                self.git("symbolic-ref", "HEAD", "refs/heads/" + branch)
                self.assertEqual(self.prepare("feat: cria cadastro\n"), "feat: cria cadastro\n")
        self.git("symbolic-ref", "HEAD", "refs/heads/feature/SMS-42-exemplo")
        self.git("checkout", "--detach", "-q", "HEAD")
        self.assertEqual(self.prepare("feat: cria cadastro\n"), "feat: cria cadastro\n")

    def test_chave_minuscula_na_branch(self):
        self.git("symbolic-ref", "HEAD", "refs/heads/bugfix/sms-99-exemplo")
        self.assertEqual(self.prepare(""), "fix(SMS-99): \n")

    def test_validacao_de_titulo_e_limites_da_chave(self):
        for text in ("feat(SMS-42): cria cadastro", "fix(ui)!: muda contrato\n\nRefs: SMS-42\n"):
            self.hook("commit-msg", message=text)
        for text in ("", "feat(SMS-42): abc", "feat: cria cadastro\nRefs: XSMS-42",
                     "feat: cria cadastro\nRefs: SMS-0", "feat: cria cadastro\nRefs: SMS-042",
                     "feat: cria cadastro\nRefs: SMS-42x"):
            with self.subTest(text=text):
                self.assertNotEqual(self.hook("commit-msg", message=text, ok=False).returncode, 0)

    def test_titulo_ascii_com_100_e_101_caracteres(self):
        prefix = "feat(SMS-42): "
        self.hook("commit-msg", message=prefix + "a" * (100 - len(prefix)))
        self.assertNotEqual(self.hook("commit-msg", message=prefix + "a" * (101 - len(prefix)), ok=False).returncode, 0)

    def test_pre_commit_vazio_nao_chama_gerenciador(self):
        self.hook("pre-commit")
        self.assertFalse(self.log.exists())

    def test_pre_commit_com_stage_e_falha_do_script(self):
        (self.root / "arquivo com espaços.ts").write_text("export const valor = 1;\n")
        self.git("add", "--", "arquivo com espaços.ts")
        self.hook("pre-commit")
        self.assertIn("run hooks:pre-commit", self.log.read_text())
        self.env["HOOK_TEST_STATUS"] = "4"
        self.assertEqual(self.hook("pre-commit", ok=False).returncode, 4)

    def dependency_change(self, lockfile="package-lock.json"):
        (self.root / "package.json").write_text('{"name":"teste"}\n')
        (self.root / lockfile).write_text("lock inicial\n")
        self.git("add", "package.json", lockfile)
        self.git("commit", "-qm", "chore(SMS-42): adiciona dependências")
        before = self.git("rev-parse", "HEAD").stdout.strip()
        (self.root / lockfile).write_text("lock atualizado\n")
        self.git("add", lockfile)
        self.git("commit", "-qm", "chore(SMS-42): atualiza dependências")
        self.git("update-ref", "ORIG_HEAD", before)

    def test_auditoria_so_roda_quando_lockfile_esta_no_stage(self):
        (self.root / "package.json").write_text('{}\n')
        self.git("add", "package.json")
        self.hook("pre-commit")
        self.assertEqual(self.log.read_text().splitlines(), ["run hooks:pre-commit"])
        (self.root / "package-lock.json").write_text('{}\n')
        self.git("add", "package-lock.json")
        self.hook("pre-commit")
        self.assertEqual(self.log.read_text().splitlines()[-2:],
                         ["run hooks:pre-commit", "run hooks:audit"])

    def test_auditoria_falha_e_bypass_nao_pula_lint(self):
        (self.root / "pnpm-lock.yaml").write_text("lockfileVersion: 9\n")
        self.git("add", "pnpm-lock.yaml")
        self.env["HOOK_TEST_FAIL_SCRIPT"] = "hooks:audit"
        self.assertEqual(self.hook("pre-commit", ok=False).returncode, 7)
        self.env["SKIP_DEPENDENCY_AUDIT"] = "1"
        self.hook("pre-commit")
        self.assertEqual(self.log.read_text().splitlines()[-1], "run hooks:pre-commit")

    def test_lockfile_parcialmente_staged_nao_audita_conteudo_errado(self):
        (self.root / "package-lock.json").write_text("stage\n")
        self.git("add", "package-lock.json")
        (self.root / "package-lock.json").write_text("disco diferente\n")
        self.assertNotEqual(self.hook("pre-commit", ok=False).returncode, 0)
        self.assertNotIn("run hooks:audit", self.log.read_text())

    def test_manifest_workspace_nao_rastreado_impede_auditoria(self):
        (self.root / "package-lock.json").write_text("stage\n")
        self.git("add", "package-lock.json")
        nested = self.root / "packages/com espaços"
        nested.mkdir(parents=True)
        (nested / "package.json").write_text('{}\n')
        self.assertNotEqual(self.hook("pre-commit", ok=False).returncode, 0)
        self.assertNotIn("run hooks:audit", self.log.read_text())

    def test_post_merge_instala_npm_com_lockfile_e_limpa_lock(self):
        self.dependency_change()
        self.hook("post-merge", source="0")
        self.assertEqual(self.log.read_text().splitlines(), ["ci --ignore-scripts"])
        self.assertFalse((self.root / ".git/frontend-install.lock").exists())

    def test_post_merge_instala_pnpm_e_permite_lifecycle_explicito(self):
        self.dependency_change("pnpm-lock.yaml")
        self.env["HOOK_PACKAGE_MANAGER"] = "pnpm"
        self.hook("post-merge", source="0")
        self.env["HOOK_INSTALL_SCRIPTS"] = "1"
        self.hook("post-merge", source="0")
        self.assertEqual(self.log.read_text().splitlines(),
                         ["install --frozen-lockfile --ignore-scripts", "install --frozen-lockfile"])

    def test_post_merge_sem_mudanca_de_dependencia_nao_instala(self):
        self.git("update-ref", "ORIG_HEAD", "HEAD")
        self.hook("post-merge", source="0")
        self.assertFalse(self.log.exists())

    def test_post_merge_adiado_com_mudancas_locais(self):
        self.dependency_change()
        (self.root / "package.json").write_text('{"local":true}\n')
        self.hook("post-merge", source="0")
        self.git("add", "package.json")
        self.hook("post-merge", source="0")
        self.assertFalse(self.log.exists())

    def test_post_merge_nao_instala_com_arquivo_dependencia_nao_rastreado(self):
        self.dependency_change()
        (self.root / "pnpm-lock.yaml").write_text("local\n")
        self.hook("post-merge", source="0")
        self.assertFalse(self.log.exists())

    def test_post_merge_aviso_quando_desativado_squash_ou_lock_concorrente(self):
        self.dependency_change()
        self.env["AUTO_INSTALL_AFTER_MERGE"] = "0"
        self.hook("post-merge", source="0")
        self.env["AUTO_INSTALL_AFTER_MERGE"] = "1"
        self.hook("post-merge", source="1")
        (self.root / ".git/frontend-install.lock").mkdir()
        self.hook("post-merge", source="0")
        self.assertFalse(self.log.exists())

    def test_post_merge_falha_de_instalacao_informa_sem_desfazer_merge(self):
        self.dependency_change()
        head = self.git("rev-parse", "HEAD").stdout
        self.env["HOOK_TEST_STATUS"] = "8"
        result = self.hook("post-merge", source="0")
        self.assertIn("instalação falhou", result.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD").stdout, head)
        self.assertFalse((self.root / ".git/frontend-install.lock").exists())

    def test_fast_forward_real_dispara_instalacao_uma_vez(self):
        (self.root / "package.json").write_text('{}\n')
        (self.root / "package-lock.json").write_text("inicial\n")
        self.git("add", "package.json", "package-lock.json")
        self.git("commit", "-qm", "chore(SMS-42): adiciona dependências")
        self.git("checkout", "-qb", "feature/SMS-43-deps")
        (self.root / "package-lock.json").write_text("atualizado\n")
        self.git("commit", "-qam", "chore(SMS-43): atualiza dependências")
        self.git("checkout", "-q", "feature/SMS-42-exemplo")
        self.run_command([NODE, str(self.hooks / "install.mjs")])
        self.git("merge", "--ff-only", "feature/SMS-43-deps")
        self.assertEqual(self.log.read_text().splitlines(), ["ci --ignore-scripts"])

    def test_push_para_main_develop_ou_exclusao_protegida_e_bloqueado(self):
        for ref, sha in (("refs/heads/main", "a" * 40), ("refs/heads/develop", "a" * 64),
                         ("refs/heads/main", "0" * 40)):
            with self.subTest(ref=ref, sha=sha):
                result = self.hook("pre-push", input=self.push_line(ref, sha), ok=False)
                self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.log.exists())

    def test_push_considera_todas_refs_antes_de_rodar_checks(self):
        text = self.push_line("refs/heads/feature/a") + self.push_line("refs/heads/main")
        self.assertNotEqual(self.hook("pre-push", input=text, ok=False).returncode, 0)
        self.assertFalse(self.log.exists())

    def test_push_permitido_tags_e_multiplas_refs_rodar_uma_vez(self):
        text = self.push_line("refs/heads/feature/a") + self.push_line("refs/tags/main")
        self.hook("pre-push", input=text)
        self.assertEqual(self.log.read_text().splitlines(), ["run hooks:pre-push"])

    def test_push_apenas_exclusao_nao_necessita_checks(self):
        self.hook("pre-push", input=self.push_line("refs/heads/feature/a", "0" * 64))
        self.assertFalse(self.log.exists())

    def test_allow_direct_push_nao_pula_validacao(self):
        self.env["ALLOW_DIRECT_PUSH"] = "1"
        self.env["HOOK_TEST_STATUS"] = "5"
        result = self.hook("pre-push", input=self.push_line("refs/heads/main"), ok=False)
        self.assertEqual(result.returncode, 5)
        self.assertTrue(self.log.exists())

    def test_bypass_total_inclui_preparo(self):
        self.env["SKIP_GIT_HOOKS"] = "1"
        self.assertEqual(self.prepare("feat: cria cadastro"), "feat: cria cadastro")
        self.hook("commit-msg", message="sem padrão")
        self.hook("pre-push", input=self.push_line("refs/heads/main"))

    def test_instalador_e_idempotente_e_commit_real_funciona(self):
        (self.root / "package.json").write_text(json.dumps({"scripts": {}}))
        for _ in range(2):
            self.run_command([NODE, str(self.hooks / "install.mjs")])
        self.assertEqual(self.git("config", "--get", "core.hooksPath").stdout.strip(), ".githooks")
        self.git("commit", "--allow-empty", "-m", "feat: cria cadastro")
        self.assertEqual(self.git("log", "-1", "--format=%s").stdout.strip(), "feat(SMS-42): cria cadastro")

    def test_instalador_ci_e_conflito_de_hooks_path(self):
        self.git("config", "core.hooksPath", ".husky/_")
        result = self.run_command([NODE, str(self.hooks / "install.mjs")], ok=False)
        self.assertNotEqual(result.returncode, 0)
        self.env["CI"] = "true"
        self.run_command([NODE, str(self.hooks / "install.mjs")])
        self.assertEqual(self.git("config", "--get", "core.hooksPath").stdout.strip(), ".husky/_")

    def test_rotina_de_ci_aceita_intervalo_valido_e_recusa_commit_invalido(self):
        workflow = (SOURCE.parent / "github/workflows/frontend-ci.yml").read_text(encoding="utf-8")
        section = workflow.split("- name: Validar mensagens de commits do PR", 1)[1]
        block = re.search(r"run: \|\n((?:          .*\n)+)", section)
        self.assertIsNotNone(block)
        script = self.root / "check-ci.sh"
        script.write_text("\n".join(line[10:] for line in block[1].splitlines()) + "\n",
                          encoding="utf-8", newline="\n")
        self.env["BASE_SHA"] = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("commit", "--allow-empty", "-m", "fix(SMS-42): corrige cadastro")
        self.env["HEAD_SHA"] = self.git("rev-parse", "HEAD").stdout.strip()
        self.run_command([SH, script.as_posix()])
        self.git("commit", "--allow-empty", "-m", "mensagem inválida sem chave")
        self.env["HEAD_SHA"] = self.git("rev-parse", "HEAD").stdout.strip()
        result = self.run_command([SH, script.as_posix()], ok=False)
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
