import types
import unittest
from unittest import mock

from tests.e2e import setup_e2e

FAKE_TOKEN = "fake-secret-token-value"


class TestLoginDoesNotPrintSecrets(unittest.TestCase):
    def setUp(self):
        fake_credentials = types.SimpleNamespace(
            server="https://example.invalid", site="site", token=FAKE_TOKEN, token_name="token-name"
        )
        patcher = mock.patch.object(setup_e2e, "credentials", fake_credentials)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_login_does_not_print_token_value(self):
        with (
            mock.patch.object(setup_e2e.subprocess, "check_call") as check_call,
            mock.patch("builtins.print") as fake_print,
        ):
            setup_e2e.login()

        printed = " ".join(str(arg) for call in fake_print.call_args_list for arg in call.args)
        self.assertNotIn(FAKE_TOKEN, printed)
        self.assertIn(FAKE_TOKEN, check_call.call_args.args[0])

    def test_failed_login_error_does_not_contain_token_value(self):
        failure = setup_e2e.subprocess.CalledProcessError(1, ["tabcmd", "--token-value", FAKE_TOKEN])
        with (
            mock.patch.object(setup_e2e.subprocess, "check_call", side_effect=failure),
            mock.patch("builtins.print"),
        ):
            with self.assertRaises(setup_e2e.subprocess.CalledProcessError) as raised:
                setup_e2e.login()

        self.assertEqual(1, raised.exception.returncode)
        self.assertNotIn(FAKE_TOKEN, str(raised.exception))
        self.assertNotIn(FAKE_TOKEN, str(raised.exception.cmd))
        self.assertIsNone(raised.exception.__cause__)
        self.assertTrue(raised.exception.__suppress_context__)
