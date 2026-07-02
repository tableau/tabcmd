import os
import subprocess
import sys
import tempfile
import unittest


class TestPythonMTabcmd(unittest.TestCase):
    def test_python_m_tabcmd_no_args_exits_zero(self):
        result = subprocess.run(
            [sys.executable, "-m", "tabcmd"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, msg=f"stderr: {result.stderr}\nstdout: {result.stdout}")

    def test_python_m_tabcmd_help_exits_zero(self):
        result = subprocess.run(
            [sys.executable, "-m", "tabcmd", "--help"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, msg=f"stderr: {result.stderr}\nstdout: {result.stdout}")
        self.assertIn("usage:", result.stdout.lower())

    def test_python_m_tabcmd_help_subcommand_exits_zero(self):
        result = subprocess.run(
            [sys.executable, "-m", "tabcmd", "help"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, msg=f"stderr: {result.stderr}\nstdout: {result.stdout}")

    def test_import_error_exits_one(self):
        # Build a minimal fake tabcmd package in a temp directory.
        # Running python -m tabcmd from that directory makes the fake package
        # take precedence ('' is first on sys.path), so tabcmd.tabcmd raises
        # ImportError and __main__.py must catch it, print the error, and exit 1.
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_pkg = os.path.join(tmpdir, "tabcmd")
            os.makedirs(fake_pkg, exist_ok=True)
            # __init__.py — empty, makes it a package
            open(os.path.join(fake_pkg, "__init__.py"), "w").close()
            # tabcmd.py — raises ImportError on import
            with open(os.path.join(fake_pkg, "tabcmd.py"), "w") as f:
                f.write('raise ImportError("test error")\n')
            # __main__.py — copy of the real entry-point so -m tabcmd works
            real_main = os.path.join(os.path.dirname(__file__), "..", "tabcmd", "__main__.py")
            with open(real_main) as src, open(os.path.join(fake_pkg, "__main__.py"), "w") as dst:
                dst.write(src.read())

            # Strip PYTHONPATH so the installed package cannot interfere
            env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}

            result = subprocess.run(
                [sys.executable, "-m", "tabcmd"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=tmpdir,
                env=env,
            )
        self.assertEqual(result.returncode, 1, msg=f"stderr: {result.stderr}\nstdout: {result.stdout}")
        self.assertIn("Exception thrown importing tabcmd", result.stderr)


if __name__ == "__main__":
    unittest.main()
