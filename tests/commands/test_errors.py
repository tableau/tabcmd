import unittest
from unittest import mock

import requests

from tabcmd.commands.constants import Errors


class ErrorsTests(unittest.TestCase):
    def test_connection_error_exits_with_status_1_without_the_exit_builtin(self):
        # the `exit` builtin comes from the site module and does not exist in a PyInstaller build
        with mock.patch("builtins.exit", side_effect=NameError("exit")):
            with self.assertRaises(SystemExit) as raised:
                Errors.check_common_error_codes_and_explain(mock.MagicMock(), requests.exceptions.ConnectionError("x"))
        assert raised.exception.code == 1

    def test_logging_failure_is_written_to_stderr(self):
        logger = mock.MagicMock()
        logger.error.side_effect = RuntimeError("logging broke")
        logger.info.side_effect = RuntimeError("logging broke")
        with mock.patch("sys.stderr") as stderr, mock.patch("sys.stdout") as stdout:
            with self.assertRaises(SystemExit):
                Errors.exit_with_error(logger, message="failed")
        written = "".join(call.args[0] for call in stderr.write.call_args_list)
        assert "Error during log call from exception" in written
        assert "Exiting..." in written
        assert "Exiting..." not in "".join(call.args[0] for call in stdout.write.call_args_list)


if __name__ == "__main__":
    unittest.main()
