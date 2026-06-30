import ast
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent


class VersionConsistencyTests(unittest.TestCase):
    def test_version_py_fallback_matches_pyproject_write_to(self):
        """The fallback import in version.py must match the write_to path in pyproject.toml."""
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        match = re.search(r'write_to\s*=\s*"([^"]+)"', pyproject)
        self.assertIsNotNone(match, "write_to not found in [tool.setuptools_scm] in pyproject.toml")

        write_to_path = match.group(1)  # e.g. "tabcmd/_version.py"
        expected_module = write_to_path.replace("/", ".").removesuffix(".py")  # e.g. "tabcmd._version"

        version_py = (ROOT / "tabcmd" / "version.py").read_text(encoding="utf-8")
        tree = ast.parse(version_py)

        fallback_modules = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                fallback_modules.append(node.module)

        self.assertIn(
            expected_module,
            fallback_modules,
            "version.py does not import from '{}' (the write_to path in pyproject.toml). "
            "If write_to was changed, update the fallback import in tabcmd/version.py.".format(expected_module),
        )
