import argparse
import pytest
import unittest
from tabcmd.commands.auth.session import Session

try:
    from tests.e2e import credentials
except ImportError:
    credentials = None


# pytest -v tests/e2e/integration_tests.py
class E2EJsonTests(unittest.TestCase):
    def test_save_then_read(self):
        test_session = Session()
        test_session.username = "USN"
        test_session.server = "SRVR"
        test_session._save_session_to_json()
        new_session = Session()
        new_session._read_from_json()
        assert new_session.username == "USN", new_session.username
        assert hasattr(new_session, "password") is False, new_session
        assert new_session.server == "SRVR", new_session.server


@pytest.mark.skipif(
    not credentials,
    reason="'No credentials file found to run tests against a live server",
)
class E2EServerTests(unittest.TestCase):

    saved_site_id = ""

    def test_log_in(self):
        if not credentials:
            return
        # TODO current test command doesn't recognize skips - change to proper pytest
        # TODO and then we can get rid of the check above
        args = argparse.Namespace(
            server=credentials.server,
            site=credentials.site,
            token_name=credentials.token_name,
            token=credentials.token,
            username=None,
            password=None,
            logging_level=None,
            no_certcheck=True,
            prompt=True,
            no_prompt=False,
            proxy=None,
            no_cookie=False,
        )
        test_session = Session()
        test_session.create_session(args)
        assert test_session.auth_token is not None
        assert test_session.site_id is not None
        assert test_session.user_id is not None
        E2EServerTests.saved_site_id = test_session.site_id

    def test_reuse_session(self):
        if not credentials:
            return
        # TODO current test command doesn't recognize skips - change to proper pytest
        # TODO and then we can get rid of the check above
        args = argparse.Namespace(
            server=None,
            site=None,
            token_name=None,
            token=None,
            username=None,
            password=None,
            logging_level=None,
            no_certcheck=True,
            prompt=True,
            no_prompt=False,
            proxy=None,
            no_cookie=False,
        )
        test_session = Session()
        test_session.create_session(args)
        assert test_session.auth_token is not None
        assert test_session.site_id is not None
        assert test_session.user_id is not None
        assert test_session.site_id == E2EServerTests.saved_site_id
