import unittest
from unittest.mock import MagicMock

from tabcmd.commands.constants import Errors, Constants
import tableauserverclient

class ConstantsTest(unittest.TestCase):
    def setUp(self):
        self.logger = MagicMock()

    def test_check_common_error_codes_and_explain_expired_session(self):
        exception = Exception("Session expired")
        exception.code = Constants.invalid_credentials
        Errors.check_common_error_codes_and_explain(self.logger, exception)
        self.logger.error.assert_called_with("Your session has expired")

    def test_check_common_error_codes_and_explain_server_response_error(self):
        exception = tableauserverclient.ServerResponseError("Server error", summary="Server error", detail="Detailed server error")
        Errors.check_common_error_codes_and_explain(self.logger, exception)
        self.logger.error.assert_called_with(exception)

    def test_check_common_error_codes_and_explain_other_exception(self):
        exception = ValueError("Invalid value")
        Errors.check_common_error_codes_and_explain(self.logger, exception)
        self.logger.exception.assert_called_with(exception)


if __name__ == "__main__":
    unittest.main()