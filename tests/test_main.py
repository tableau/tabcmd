import os
import subprocess
import sys
import tempfile
import textwrap
import unittest

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _repo_env():
    env = dict(os.environ)
    env["PYTHONPATH"] = _REPO_ROOT
    return env


class TestPythonMTabcmd(unittest.TestCase):
    def test_python_m_tabcmd_no_args_exits_zero(self):
        result = subprocess.run(
            [sys.executable, "-m", "tabcmd"],
            capture_output=True,
            text=True,
            timeout=30,
            env=_repo_env(),
        )
        self.assertEqual(result.returncode, 0, msg="stderr: {}\nstdout: {}".format(result.stderr, result.stdout))

    def test_python_m_tabcmd_help_exits_zero(self):
        result = subprocess.run(
            [sys.executable, "-m", "tabcmd", "--help"],
            capture_output=True,
            text=True,
            timeout=30,
            env=_repo_env(),
        )
        self.assertEqual(result.returncode, 0, msg="stderr: {}\nstdout: {}".format(result.stderr, result.stdout))
        self.assertIn("usage:", result.stdout.lower())

    def test_python_m_tabcmd_help_subcommand_exits_zero(self):
        result = subprocess.run(
            [sys.executable, "-m", "tabcmd", "help"],
            capture_output=True,
            text=True,
            timeout=30,
            env=_repo_env(),
        )
        self.assertEqual(result.returncode, 0, msg="stderr: {}\nstdout: {}".format(result.stderr, result.stdout))

    def test_import_error_exits_one(self):
        # Inject a broken tabcmd.tabcmd into sys.modules before running __main__,
        # so the ImportError handler is exercised without relying on sys.path ordering.
        script = textwrap.dedent(
            """\
            import sys
            class _BrokenTabcmd:
                def __getattr__(self, _):
                    raise ImportError("injected failure")
            sys.modules["tabcmd.tabcmd"] = _BrokenTabcmd()
            import runpy
            runpy.run_module("tabcmd", run_name="__main__")
            """
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            script_path = os.path.join(tmpdir, "run.py")
            with open(script_path, "w") as f:
                f.write(script)
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                timeout=30,
                env=_repo_env(),
            )
        self.assertEqual(result.returncode, 1, msg="stderr: {}\nstdout: {}".format(result.stderr, result.stdout))
        self.assertIn("Exception thrown importing tabcmd", result.stderr)


if __name__ == "__main__":
    unittest.main()
