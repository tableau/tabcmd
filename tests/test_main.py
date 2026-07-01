import subprocess
import sys
import unittest


class TestPythonMTabcmd(unittest.TestCase):
    def test_python_m_tabcmd_no_args_exits_zero(self):
        result = subprocess.run(
            [sys.executable, "-m", "tabcmd"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, msg=f"stderr: {result.stderr}\nstdout: {result.stdout}")

    def test_python_m_tabcmd_help_exits_zero(self):
        result = subprocess.run(
            [sys.executable, "-m", "tabcmd", "--help"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, msg=f"stderr: {result.stderr}\nstdout: {result.stdout}")
        self.assertIn("tabcmd", result.stdout)

    def test_python_m_tabcmd_help_subcommand_exits_zero(self):
        result = subprocess.run(
            [sys.executable, "-m", "tabcmd", "help"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, msg=f"stderr: {result.stderr}\nstdout: {result.stdout}")


if __name__ == "__main__":
    unittest.main()
