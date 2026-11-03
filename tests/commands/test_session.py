import json
import logging
import os
import stat
import tempfile
from argparse import Namespace
import unittest
from unittest import mock
from unittest.mock import MagicMock

import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session

_isolated_path_patcher = None


def setUpModule():
    # Session() reads ~/tableau_auth.json when constructed, and some tests call
    # end_session_and_clear_data(); keep every test off the developer's real session file.
    global _isolated_path_patcher
    directory = tempfile.mkdtemp()
    _isolated_path_patcher = mock.patch.object(
        Session, "_get_file_path", return_value=os.path.join(directory, "tableau_auth.json")
    )
    _isolated_path_patcher.start()


def tearDownModule():
    if _isolated_path_patcher:
        _isolated_path_patcher.stop()


args_to_mock = Namespace(
    username=None,
    site_name=None,
    password=None,
    password_file=None,
    server=None,
    token_name=None,
    token_value=None,
    token_file=None,
    logging_level=None,
    no_certcheck=None,
    no_prompt=False,
    no_cookie=False,
    certificate=None,
    proxy=None,
    no_proxy=True,
    timeout=None,
)

mock_data_from_json = Namespace(
    token=None,  # this is the session token, not pat
    username=None,
    user_id=None,
    site_name=None,
    site_id=None,
    password=None,
    password_file=None,
    token_file=None,
    server=None,
    personal_access_token_name=None,
    personal_access_token=None,
    last_login_using=None,
    no_cookie=False,
    certificate=None,
    no_cert=True,
    proxy=None,
    no_proxy=True,
    timeout=None,
    no_prompt=False,
)

fakeserver = "http://SRVR".lower()
logger = logging.getLogger("tests")


def _set_mocks_for_json_file_saved_username(mock_json_lib, auth_token, username):
    mock_auth = vars(mock_data_from_json)
    mock_json_lib.load.return_value = {"tableau_auth": [mock_auth]}
    mock_auth["auth_token"] = auth_token
    mock_auth["username"] = username
    mock_auth["server"] = fakeserver
    mock_auth["last_login_using"] = "username"
    mock_auth["no_certcheck"] = True


def _set_mocks_for_json_file_exists(mock_path, mock_json_lib, does_it_exist=True):
    mock_json_lib.JSONDecodeError = ValueError
    path = mock_path()
    path.expanduser.return_value = ""
    path.join.return_value = ""
    path.exists.return_value = does_it_exist

    mock_auth = vars(mock_data_from_json)
    if does_it_exist:
        mock_json_lib.load.return_value = [mock_auth]
    else:
        mock_json_lib.load.return_value = None
    return path


def _set_mock_file_content(mock_load, expected_content):
    mock_load.return_value = expected_content
    return mock_load


@mock.patch("tabcmd.commands.auth.session.json")
@mock.patch("os.path")
@mock.patch("builtins.open")
class JsonTests(unittest.TestCase):
    def test_read_session_from_json(self, mock_open, mock_path, mock_json):
        _set_mocks_for_json_file_exists(mock_path, mock_json)
        _set_mocks_for_json_file_saved_username(mock_json, "AUTHTOKEN", "USERNAME")
        test_session = Session()
        test_session._read_from_json()
        assert hasattr(test_session.auth_token, "AUTHTOKEN") is False, test_session
        assert hasattr(test_session, "password") is False, test_session
        assert test_session.username == "USERNAME"
        assert test_session.server_url == fakeserver, test_session.server_url

    def test_save_session_to_json(self, mock_open, mock_path, mock_json):
        _set_mocks_for_json_file_exists(mock_path, mock_json)
        test_session = Session()
        test_session.username = "USN"
        test_session.server = "SRVR"
        with mock.patch.object(Session, "_save_file") as mock_save:
            test_session._save_session_to_json()
        mock_save.assert_called_once()
        saved = mock_save.call_args[0][0]["tableau_auth"][0]
        assert saved["username"] == "USN"

    def test_clear_session(self, mock_open, mock_path, mock_json):
        _set_mocks_for_json_file_exists(mock_path, mock_json)
        test_session = Session()
        test_session.username = "USN"
        test_session.server_url = "http://srvr"
        test_session.auth_token = "tok"
        test_session.token_value = "pat-secret"
        test_session._clear_data()
        assert test_session.username is None
        assert test_session.server_url is None
        assert test_session.auth_token is None
        assert test_session.token_value is None

    def test_json_not_present(self, mock_open, mock_path, mock_json):
        _set_mocks_for_json_file_exists(mock_path, mock_json, does_it_exist=False)
        mock_open.assert_not_called()

    def test_json_invalid(self, mock_open, mock_path, mock_json):
        _set_mocks_for_json_file_exists(mock_path, mock_json)
        mock_json.load = "just a string"
        test_session = Session()
        assert test_session.username is None


@mock.patch("getpass.getpass")
class BuildCredentialsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # make sure any json data etc is cleared
        Session().end_session_and_clear_data()

    # Set: Create auth credentials
    # This first set of tests has no attributes set
    def test__create_new_token_credential_fails_no_args(self, mock_pass):
        active_session = Session()
        with self.assertRaises(SystemExit):
            active_session._create_new_token_credential()

    def test__create_new_username_credential_fails_no_args(self, mock_pass):
        active_session = Session()
        with self.assertRaises(SystemExit):
            active_session._create_new_credential(None, None)

    # These two already have a username saved and pass in a password as argument
    def test__create_new_token_credential_succeeds_new_token(self, mock_pass):
        test_args = Namespace(**vars(args_to_mock))
        test_args.token_value = "gibberish"
        active_session = Session()
        assert active_session.token_value is None, active_session.token_value
        active_session.token_name = "readable"
        auth = active_session._create_new_token_credential()
        assert auth is not None
        assert mock_pass.is_not_called()

    def test__create_new_username_credential_succeeds_new_password(self, mock_pass):
        test_password = "pword1"
        active_session: Session = Session()
        active_session.username = "user"
        active_session.site_id = ""
        auth = active_session._create_new_credential(test_password, Session.PASSWORD_CRED_TYPE)
        assert auth is not None

    # this one has a token saved
    def test__create_new_token_credential_succeeds_from_self(self, mock_pass):
        active_session = Session()
        active_session.token_value = "gibberish2"
        active_session.token_name = "readable2"
        auth = active_session._create_new_token_credential()
        assert mock_pass.is_not_called()
        assert auth is not None
        assert auth.token_name == "readable2", auth
        assert auth.personal_access_token == "gibberish2", auth

    # this one calls getpass because we don't store the password
    def test__create_new_username_credential_succeeds_from_self(self, mock_pass):
        active_session = Session()
        active_session.username = "user3"
        active_session.site_id = ""
        auth = active_session._create_new_credential(None, Session.PASSWORD_CRED_TYPE)
        mock_pass.assert_called()
        assert auth is not None
        assert auth.username == "user3", auth
        assert auth.password == mock_pass(), auth

    def test__create_new_token_credential_succeeds_from_args(self, mock_pass):
        test_args = Namespace(**vars(args_to_mock))
        test_args.token_value = "gibberish"
        test_args.token_name = "readable"
        active_session = Session()
        active_session._update_session_data(test_args)
        auth = active_session._create_new_token_credential()

    def test__create_new_username_credential_succeeds_from_args(self, mock_pass):
        test_args = Namespace(**vars(args_to_mock))
        test_args.username = "user"
        test_args.password = "pwordddddd"
        active_session = Session()
        active_session._update_session_data(test_args)
        auth = active_session._create_new_credential(test_args.password, Session.PASSWORD_CRED_TYPE)


class PromptingTests(unittest.TestCase):
    def test_show_prompt_if_user_didnt_say(self):
        test_args = Namespace(**vars(args_to_mock))
        mock_session = Session()
        mock_session._update_session_data(test_args)
        assert mock_session._allow_prompt() is True, test_args

    def test_show_prompt_if_user_said_yes(self):
        test_args = Namespace(**vars(args_to_mock))
        test_args.prompt = True
        mock_session = Session()
        mock_session._update_session_data(test_args)
        assert mock_session._allow_prompt() is True, test_args

    def test_dont_show_prompt_if_user_said_no(self):
        test_args = Namespace(**vars(args_to_mock))
        test_args.no_prompt = True
        mock_session = Session()
        mock_session._update_session_data(test_args)
        assert mock_session._allow_prompt() is False, test_args


"""
These tests all call the top-level method create_session, and mock out
the json file, and the TSC.Server calls
"""


@mock.patch("tabcmd.commands.auth.session.json")
@mock.patch("os.path")
@mock.patch("builtins.open")
@mock.patch("getpass.getpass")
class CreateSessionTests(unittest.TestCase):
    @mock.patch("tableauserverclient.Server")
    def test_create_session_first_time_no_args(self, mock_tsc, mock_pass, mock_file, mock_path, mock_json):
        _set_mocks_for_json_file_exists(mock_path, mock_json, does_it_exist=False)

        test_args = Namespace(**vars(args_to_mock))
        new_session = Session()
        with self.assertRaises(SystemExit):
            auth = new_session.create_session(test_args, None)

    @mock.patch("tableauserverclient.Server")
    def test_create_session_first_time_with_token_arg(self, mock_tsc, mock_pass, mock_file, mock_path, mock_json):
        _set_mocks_for_json_file_exists(mock_path, mock_json, does_it_exist=False)
        new_session = Session()
        new_session.tableau_server = mock_tsc()
        _set_mock_signin_validation_succeeds(new_session.tableau_server, "u")

        test_args = Namespace(**vars(args_to_mock))
        test_args.token_name = "tn"
        test_args.token_value = "foo"
        auth = new_session.create_session(test_args, None)
        assert auth is not None, auth
        assert auth.auth_token is not None, auth.auth_token
        assert auth.auth_token.name is not None, auth.auth_token
        assert new_session.token_value == "foo", new_session.token_value
        assert new_session.token_name == "tn", new_session

    @mock.patch("tableauserverclient.Server")
    def test_create_session_first_time_with_password_arg(self, mock_tsc, mock_pass, mock_file, mock_path, mock_json):
        name = "uuuu"
        new_session = Session()
        new_session.tableau_server = mock_tsc()
        _set_mocks_for_json_file_exists(mock_path, mock_json, does_it_exist=False)
        _set_mock_signin_validation_succeeds(new_session.tableau_server, name)

        test_args = Namespace(**vars(args_to_mock))
        test_args.username = name
        test_args.password = "pppp"

        auth = new_session.create_session(test_args, None)
        assert auth is not None, auth
        assert auth.auth_token is not None, auth.auth_token
        assert new_session.username == name, new_session
        mock_tsc.assert_called()

    @mock.patch("tableauserverclient.Server")
    def test_create_session_first_time_with_password_file_as_password(
        self, mock_tsc, mock_pass, mock_file, mock_path, mock_json
    ):
        username = "uuuu"
        _set_mocks_for_json_file_exists(mock_path, mock_json, does_it_exist=False)
        new_session = Session()
        _set_mock_signin_validation_succeeds(mock_tsc(), username)
        test_args = Namespace(**vars(args_to_mock))
        test_args.username = username
        # filename = os.path.join(os.path.dirname(__file__),"test_credential_file.txt")
        # test_args.password_file = os.getcwd()+"/test_credential_file.txt"
        test_args.password_file = "filename"
        with mock.patch("builtins.open", mock.mock_open(read_data="my_password")):
            auth = new_session.create_session(test_args, None)

        assert auth is not None, auth
        assert auth.auth_token is not None, auth.auth_token
        assert new_session.username == username, new_session
        assert new_session.password_file == "filename", new_session
        mock_tsc.assert_called()

    @mock.patch("tableauserverclient.Server")
    def test_create_session_first_time_with_password_file_as_token(
        self, mock_tsc, mock_pass, mock_file, mock_path, mock_json
    ):
        _set_mocks_for_json_file_exists(mock_path, mock_json, does_it_exist=False)
        server = mock_tsc()
        _set_mock_signin_validation_succeeds(server, "testing")
        test_args = Namespace(**vars(args_to_mock))
        test_args.token_name = "mytoken"
        test_args.token_file = "filename"
        with mock.patch("builtins.open", mock.mock_open(read_data="my_token")):
            new_session = Session()
            auth = new_session.create_session(test_args, None)

        assert auth is not None, auth
        assert auth.auth_token is not None, auth.auth_token
        assert new_session.token_file == "filename", new_session
        mock_tsc.assert_called()

    @mock.patch("tableauserverclient.Server")
    def test_load_saved_session_data(self, mock_tsc, mock_pass, mock_file, mock_path, mock_json):
        _set_mocks_for_json_file_exists(mock_path, mock_json)
        _set_mocks_for_json_file_saved_username(mock_json, "auth_token", "username")
        test_args = Namespace(**vars(args_to_mock))
        new_session = Session()
        new_session._update_session_data(test_args)
        assert new_session, new_session
        assert new_session.username == "username", new_session.username
        assert new_session.server_url == fakeserver, new_session.server_url

    @mock.patch("tableauserverclient.Server")
    def test_create_session_with_active_session_saved(self, mock_tsc, mock_pass, mock_file, mock_path, mock_json):
        _set_mocks_for_json_file_exists(mock_path, mock_json)
        _set_mocks_for_json_file_saved_username(mock_json, "auth_token", None)
        test_args = Namespace(**vars(args_to_mock))
        test_args.token_value = "tn"
        test_args.token_name = "tnnnn"
        test_args.no_prompt = False
        new_session = Session()

        auth = new_session.create_session(test_args, None)
        assert auth is not None, auth
        assert auth.auth_token is not None, auth.auth_token
        mock_tsc.assert_called()

    @mock.patch("tableauserverclient.Server")
    def test_create_session_with_saved_expired_username_session(
        self, mock_tsc, mock_pass, mock_file, mock_path, mock_json
    ):
        test_username = "monster"
        server = mock_tsc()
        _set_mocks_for_json_file_exists(mock_path, mock_json)
        _set_mocks_for_json_file_saved_username(mock_json, "auth_token", test_username)
        _set_mock_tsc_sign_in_succeeds(server)
        _set_mock_signin_validation_succeeds(server, test_username)
        test_args = Namespace(**vars(args_to_mock))
        mock_pass.getpass.return_value = "success"
        test_args.password = "eqweqwe"
        new_session = Session()
        auth = new_session.create_session(test_args, None)
        mock_pass.assert_not_called()  # the password was passed in, so no prompt
        assert auth is not None, auth
        assert auth.auth_token is not None, auth.auth_token
        assert auth.auth_token == "cookiieeeee"
        assert new_session.username == test_username, new_session
        server.use_server_version.assert_called()

    @mock.patch("tableauserverclient.Server")
    def test_create_session_server_url_with_server_arg(self, mock_tsc, mock_pass, mock_file, mock_path, mock_json):
        name = "uuuu"
        new_session = Session()
        new_session.tableau_server = mock_tsc()
        _set_mocks_for_json_file_exists(mock_path, mock_json, does_it_exist=False)
        _set_mock_signin_validation_succeeds(new_session.tableau_server, name)

        test_args = Namespace(**vars(args_to_mock))
        test_args.username = name
        test_args.password = "pppp"
        args_server = "https://10ay.online.tableau.com/"
        test_args.server = args_server

        expected_session_server_url = args_server.rstrip("/")

        auth = new_session.create_session(test_args, None)
        assert auth is not None, auth
        assert new_session.server_url == expected_session_server_url

    @mock.patch("tableauserverclient.Server")
    def test_create_session_server_url_with_no_protocol_in_server_arg(
        self, mock_tsc, mock_pass, mock_file, mock_path, mock_json
    ):
        name = "uuuu"
        new_session = Session()
        new_session.tableau_server = mock_tsc()
        _set_mocks_for_json_file_exists(mock_path, mock_json, does_it_exist=False)
        _set_mock_signin_validation_succeeds(new_session.tableau_server, name)

        test_args = Namespace(**vars(args_to_mock))
        test_args.username = name
        test_args.password = "pppp"
        args_server = "10ay.online.tableau.com/"
        test_args.server = args_server

        expected_session_server_url = "https://" + args_server.rstrip("/")

        auth = new_session.create_session(test_args, None)
        assert auth is not None, auth
        assert new_session.server_url == expected_session_server_url

    @mock.patch("tableauserverclient.Server")
    def test_create_session_server_url_with_no_protocol_and_extra_path_in_server_arg(
        self, mock_tsc, mock_pass, mock_file, mock_path, mock_json
    ):
        name = "uuuu"
        new_session = Session()
        new_session.tableau_server = mock_tsc()
        _set_mocks_for_json_file_exists(mock_path, mock_json, does_it_exist=False)
        _set_mock_signin_validation_succeeds(new_session.tableau_server, name)

        test_args = Namespace(**vars(args_to_mock))
        test_args.username = name
        test_args.password = "pppp"
        args_server = "10ay.online.tableau.com/#/sitename/views/viewname"
        test_args.server = args_server

        expected_session_server_url = "https://" + args_server.split("/")[0]

        auth = new_session.create_session(test_args, None)
        assert auth is not None, auth
        assert new_session.server_url == expected_session_server_url

    @mock.patch("tableauserverclient.Server")
    def test_create_session_server_url_with_extra_path_in_server_arg(
        self, mock_tsc, mock_pass, mock_file, mock_path, mock_json
    ):
        name = "uuuu"
        new_session = Session()
        new_session.tableau_server = mock_tsc()
        _set_mocks_for_json_file_exists(mock_path, mock_json, does_it_exist=False)
        _set_mock_signin_validation_succeeds(new_session.tableau_server, name)

        test_args = Namespace(**vars(args_to_mock))
        test_args.username = name
        test_args.password = "pppp"
        args_server = "https://10ay.online.tableau.com/#/sitename/views/viewname"
        test_args.server = args_server

        expected_session_server_url = args_server.split("#")[0].rstrip("/")

        auth = new_session.create_session(test_args, None)
        assert auth is not None, auth
        assert new_session.server_url == expected_session_server_url

    @mock.patch("tableauserverclient.Server")
    def test_create_session_username_only_prompts_for_password(
        self, mock_tsc, mock_pass, mock_file, mock_path, mock_json
    ):
        """When username given, no password, no active session: should prompt via getpass."""
        name = "myuser"
        _set_mocks_for_json_file_exists(mock_path, mock_json, does_it_exist=False)
        new_session = Session()
        new_session.no_prompt = False
        new_session.tableau_server = None  # no active session
        mock_pass.return_value = "prompted_password"
        mock_tsc.return_value.auth.sign_in.return_value = mock.MagicMock()

        test_args = Namespace(**vars(args_to_mock))
        test_args.username = name
        test_args.no_prompt = False

        auth = new_session.create_session(test_args, None)
        assert auth is not None, auth
        mock_pass.assert_called()

    @mock.patch("tableauserverclient.Server")
    def test_create_session_username_only_reuses_existing_session(
        self, mock_tsc, mock_pass, mock_file, mock_path, mock_json
    ):
        """When username given with no password but an active session exists: reuse it, no prompt."""
        name = "myuser"
        _set_mocks_for_json_file_exists(mock_path, mock_json, does_it_exist=False)
        new_session = Session()
        new_session.tableau_server = mock_tsc()
        new_session.user_id = "some-user-id"
        _set_mock_signin_validation_succeeds(new_session.tableau_server, name)

        test_args = Namespace(**vars(args_to_mock))
        test_args.username = name
        test_args.no_prompt = False

        auth = new_session.create_session(test_args, None)
        assert auth is not None, auth
        mock_pass.assert_not_called()

    @mock.patch("tableauserverclient.Server")
    def test_create_session_username_only_no_prompt_exits(self, mock_tsc, mock_pass, mock_file, mock_path, mock_json):
        """When username given, no password, --no-prompt set, no active session: exit with error."""
        name = "myuser"
        _set_mocks_for_json_file_exists(mock_path, mock_json, does_it_exist=False)
        new_session = Session()
        new_session.no_prompt = True
        new_session.tableau_server = None  # no active session

        test_args = Namespace(**vars(args_to_mock))
        test_args.username = name
        test_args.no_prompt = True

        with self.assertRaises(SystemExit):
            new_session.create_session(test_args, None)
        mock_pass.assert_not_called()

    @mock.patch("tableauserverclient.Server")
    def test_create_session_username_and_password_no_prompt(self, mock_tsc, mock_pass, mock_file, mock_path, mock_json):
        """When both username and password are given, getpass should not be called."""
        name = "myuser"
        _set_mocks_for_json_file_exists(mock_path, mock_json, does_it_exist=False)
        new_session = Session()
        new_session.tableau_server = mock_tsc()
        _set_mock_signin_validation_succeeds(new_session.tableau_server, name)

        test_args = Namespace(**vars(args_to_mock))
        test_args.username = name
        test_args.password = "mypassword"
        test_args.no_prompt = False

        auth = new_session.create_session(test_args, None)
        assert auth is not None, auth
        mock_pass.assert_not_called()

    def _saved_session_ids(self):
        """Seed the mocked session file with saved ids; they are reset after the test."""
        patcher = mock.patch.dict(vars(mock_data_from_json), {"site_id": "site-1", "user_id": "user-1"})
        patcher.start()
        self.addCleanup(patcher.stop)

    @mock.patch("tabcmd.commands.auth.session.Session._open_connection_with_opts")
    def test_create_session_reuses_saved_auth_token(self, mock_open_conn, mock_pass, mock_file, mock_path, mock_json):
        """After a prior `tabcmd login`, a subsequent no-args command should
        reattach to the saved auth_token instead of prompting for a password
        (regression test for #463)."""
        _set_mocks_for_json_file_exists(mock_path, mock_json)
        _set_mocks_for_json_file_saved_username(mock_json, "cookieee", "monster")
        self._saved_session_ids()

        restored_server = mock.MagicMock(name="restored_tsc_server")
        _set_mock_signin_validation_succeeds(restored_server, "monster")
        mock_open_conn.return_value = restored_server

        test_args = Namespace(**vars(args_to_mock))
        new_session = Session()
        auth = new_session.create_session(test_args, None)

        restored_server._set_auth.assert_called_once_with("site-1", "user-1", "cookieee")
        restored_server.users.get_by_id.assert_called_once_with("user-1")
        assert auth is restored_server
        mock_pass.assert_not_called()

    @mock.patch("tabcmd.commands.auth.session.Session._open_connection_with_opts")
    def test_create_session_falls_back_when_saved_token_expired(
        self, mock_open_conn, mock_pass, mock_file, mock_path, mock_json
    ):
        """If the saved token is present but no longer accepted by the server,
        we should fall through to the existing credential-recovery path and
        sign in on a fresh connection."""
        _set_mocks_for_json_file_exists(mock_path, mock_json)
        _set_mocks_for_json_file_saved_username(mock_json, "stale-token", "monster")
        self._saved_session_ids()

        stale_server = mock.MagicMock(name="stale_tsc_server")
        stale_server.users.get_by_id.side_effect = Exception("401 Unauthorized")
        fresh_server = mock.MagicMock(name="fresh_tsc_server")
        _set_mock_signin_validation_succeeds(fresh_server, "monster")
        mock_open_conn.side_effect = [stale_server, fresh_server]
        mock_pass.return_value = "prompted_password"

        test_args = Namespace(**vars(args_to_mock))
        new_session = Session()
        auth = new_session.create_session(test_args, None)

        stale_server._set_auth.assert_called_once_with("site-1", "user-1", "stale-token")
        mock_pass.assert_called()
        fresh_server.auth.sign_in.assert_called_once()
        assert auth is fresh_server

    @mock.patch("tabcmd.commands.auth.session.Session._open_connection_with_opts")
    def test_create_session_falls_back_when_set_auth_raises(
        self, mock_open_conn, mock_pass, mock_file, mock_path, mock_json
    ):
        """A failure attaching the saved token (e.g. TSC dropped the private
        _set_auth) must fall back to a fresh sign-in, not abort the command."""
        _set_mocks_for_json_file_exists(mock_path, mock_json)
        _set_mocks_for_json_file_saved_username(mock_json, "cookieee", "monster")
        self._saved_session_ids()

        broken_server = mock.MagicMock(name="broken_tsc_server")
        broken_server._set_auth.side_effect = AttributeError("_set_auth")
        fresh_server = mock.MagicMock(name="fresh_tsc_server")
        _set_mock_signin_validation_succeeds(fresh_server, "monster")
        mock_open_conn.side_effect = [broken_server, fresh_server]
        mock_pass.return_value = "prompted_password"

        test_args = Namespace(**vars(args_to_mock))
        auth = Session().create_session(test_args, None)

        fresh_server.auth.sign_in.assert_called_once()
        assert auth is fresh_server

    @mock.patch("tabcmd.commands.auth.session.Session._open_connection_with_opts")
    def test_create_session_does_not_reuse_token_for_different_site(
        self, mock_open_conn, mock_pass, mock_file, mock_path, mock_json
    ):
        """--site naming a different site than the saved one must not reattach
        the saved token, or the command would run against the old site."""
        _set_mocks_for_json_file_exists(mock_path, mock_json)
        _set_mocks_for_json_file_saved_username(mock_json, "cookieee", "monster")
        self._saved_session_ids()

        fresh_server = mock.MagicMock(name="fresh_tsc_server")
        _set_mock_signin_validation_succeeds(fresh_server, "monster")
        mock_open_conn.return_value = fresh_server
        mock_pass.return_value = "prompted_password"

        test_args = Namespace(**vars(args_to_mock))
        test_args.site_name = "othersite"
        auth = Session().create_session(test_args, None)

        fresh_server._set_auth.assert_not_called()
        fresh_server.auth.sign_in.assert_called_once()
        assert auth is fresh_server

    @mock.patch("tabcmd.commands.auth.session.Session._open_connection_with_opts")
    def test_create_session_does_not_reuse_token_for_different_server(
        self, mock_open_conn, mock_pass, mock_file, mock_path, mock_json
    ):
        """--server naming a different server than the saved one must not reattach the saved token."""
        _set_mocks_for_json_file_exists(mock_path, mock_json)
        _set_mocks_for_json_file_saved_username(mock_json, "cookieee", "monster")
        self._saved_session_ids()

        fresh_server = mock.MagicMock(name="fresh_tsc_server")
        _set_mock_signin_validation_succeeds(fresh_server, "monster")
        mock_open_conn.return_value = fresh_server
        mock_pass.return_value = "prompted_password"

        test_args = Namespace(**vars(args_to_mock))
        test_args.server = "http://other-server"
        auth = Session().create_session(test_args, None)

        fresh_server._set_auth.assert_not_called()
        fresh_server.auth.sign_in.assert_called_once()
        assert auth is fresh_server


@mock.patch("tabcmd.commands.auth.session.json")
@mock.patch("tabcmd.commands.auth.session.os.path")
@mock.patch("builtins.open")
class MissingCredentialFileTests(unittest.TestCase):
    """Tests that missing --password-file / --token-file paths exit with an actionable error."""

    def _assert_missing_file_error(self, mock_exit, expected_key_fragment, expected_path):
        """Assert exit_with_error was called with a message referencing the missing file."""
        call_kwargs = mock_exit.call_args
        message = call_kwargs[1].get("message", "") or str(call_kwargs)
        # Depending on whether locale .mo files are loaded, _() returns either the
        # translated string (containing the path) or the raw i18n key.
        self.assertTrue(
            expected_path in message or expected_key_fragment in message,
            "Expected path '{}' or key '{}' in error message, got: {}".format(
                expected_path, expected_key_fragment, message
            ),
        )

    def test_password_file_not_found_exits_with_actionable_error(self, mock_file, mock_path, mock_json):
        mock_path.isfile.return_value = False
        mock_path.exists.return_value = False
        new_session = Session()
        new_session.username = "uuuu"
        new_session.password_file = "/nonexistent/cred.txt"
        with mock.patch("tabcmd.commands.auth.session.Errors.exit_with_error", side_effect=SystemExit) as mock_exit:
            with self.assertRaises(SystemExit):
                new_session._create_new_credential(None, Session.PASSWORD_CRED_TYPE)
        self._assert_missing_file_error(mock_exit, "password_file_not_found", "/nonexistent/cred.txt")

    def test_token_file_not_found_exits_with_actionable_error(self, mock_file, mock_path, mock_json):
        mock_path.isfile.return_value = False
        mock_path.exists.return_value = False
        new_session = Session()
        new_session.token_name = "mytoken"
        new_session.token_file = "/nonexistent/token.txt"
        with mock.patch("tabcmd.commands.auth.session.Errors.exit_with_error", side_effect=SystemExit) as mock_exit:
            with self.assertRaises(SystemExit):
                new_session._create_new_token_credential()
        self._assert_missing_file_error(mock_exit, "token_file_not_found", "/nonexistent/token.txt")

    @mock.patch("tableauserverclient.Server")
    def test_create_session_with_missing_password_file_exits(self, mock_tsc, mock_file, mock_path, mock_json):
        mock_path.isfile.return_value = False
        mock_path.exists.return_value = False
        new_session = Session()
        new_session.tableau_server = mock_tsc()
        test_args = Namespace(**vars(args_to_mock))
        test_args.username = "uuuu"
        test_args.server = "https://fake.server.com"
        test_args.password_file = "/nonexistent/cred.txt"
        with mock.patch("tabcmd.commands.auth.session.Errors.exit_with_error", side_effect=SystemExit) as mock_exit:
            with self.assertRaises(SystemExit):
                new_session.create_session(test_args, None)
        self._assert_missing_file_error(mock_exit, "password_file_not_found", "/nonexistent/cred.txt")

    @mock.patch("tableauserverclient.Server")
    def test_create_session_with_missing_token_file_exits(self, mock_tsc, mock_file, mock_path, mock_json):
        mock_path.isfile.return_value = False
        mock_path.exists.return_value = False
        new_session = Session()
        new_session.tableau_server = mock_tsc()
        test_args = Namespace(**vars(args_to_mock))
        test_args.token_name = "mytoken"
        test_args.server = "https://fake.server.com"
        test_args.token_file = "/nonexistent/token.txt"
        with mock.patch("tabcmd.commands.auth.session.Errors.exit_with_error", side_effect=SystemExit) as mock_exit:
            with self.assertRaises(SystemExit):
                new_session.create_session(test_args, None)
        self._assert_missing_file_error(mock_exit, "token_file_not_found", "/nonexistent/token.txt")


class RestoreSavedSessionTests(unittest.TestCase):
    """Direct unit tests for Session._restore_saved_session (issue #463).

    These exist as a hard regression guard: they fail if the method is deleted
    or if TSC removes the private _set_auth API tabcmd depends on to reattach
    a saved token."""

    def test_method_exists_on_session(self):
        # Guards the fix against accidental removal. If someone deletes the
        # method during a refactor, the create_session flow falls back to
        # getpass and hangs silently in non-TTY contexts (#463).
        assert callable(getattr(Session, "_restore_saved_session", None)), (
            "Session._restore_saved_session was removed; login-then-publish "
            "will silently hang on getpass again. See #463."
        )

    def test_tsc_server_still_exposes_set_auth(self):
        # Guards the fix against a TSC upstream rename/removal of the private
        # _set_auth attachment API. If TSC drops it, _restore_saved_session's
        # broad `except Exception` would swallow the AttributeError at DEBUG
        # level and reintroduce the silent-hang behavior.
        import tableauserverclient as TSC

        assert callable(getattr(TSC.Server, "_set_auth", None)), (
            "tableauserverclient.Server._set_auth is gone; tabcmd's saved-"
            "session reuse will silently fall back to a getpass prompt. See "
            "the note in Session._restore_saved_session."
        )

    def test_returns_none_when_no_saved_token(self):
        session = Session()
        session.auth_token = None
        session.site_id = "s"
        session.user_id = "u"
        session.server_url = "https://x"
        assert session._restore_saved_session() is None

    def test_returns_none_when_no_site_id(self):
        session = Session()
        session.auth_token = "t"
        session.site_id = None
        session.user_id = "u"
        session.server_url = "https://x"
        assert session._restore_saved_session() is None

    def test_returns_none_when_no_user_id(self):
        session = Session()
        session.auth_token = "t"
        session.site_id = "s"
        session.user_id = None
        session.server_url = "https://x"
        assert session._restore_saved_session() is None

    def test_returns_none_when_no_server_url(self):
        session = Session()
        session.auth_token = "t"
        session.site_id = "s"
        session.user_id = "u"
        session.server_url = None
        assert session._restore_saved_session() is None


class SessionFileSecurityTests(unittest.TestCase):
    """The session file holds the auth token and PAT secret; the proxy URL may hold a password."""

    def _session_with_file(self, directory):
        session = Session()
        path = os.path.join(directory, "tableau_auth.json")
        patcher = mock.patch.object(Session, "_get_file_path", return_value=path)
        patcher.start()
        self.addCleanup(patcher.stop)
        return session, path

    @unittest.skipIf(os.name == "nt", "POSIX file modes")
    def test_new_session_file_is_owner_only(self):
        with tempfile.TemporaryDirectory() as directory:
            session, path = self._session_with_file(directory)
            session.token_value = "pat-secret"
            session._save_file(session._serialize_for_save())
            assert stat.S_IMODE(os.stat(path).st_mode) == 0o600

    @unittest.skipIf(os.name == "nt", "POSIX file modes")
    def test_existing_loose_session_file_is_tightened(self):
        with tempfile.TemporaryDirectory() as directory:
            session, path = self._session_with_file(directory)
            with open(path, "w") as f:
                f.write("{}")
            os.chmod(path, 0o644)
            session._save_file(session._serialize_for_save())
            assert stat.S_IMODE(os.stat(path).st_mode) == 0o600

    def test_saved_file_round_trips(self):
        with tempfile.TemporaryDirectory() as directory:
            session, path = self._session_with_file(directory)
            session.token_value = "pat-secret"
            session.auth_token = "tok"
            session._save_file(session._serialize_for_save())
            with open(path) as f:
                saved = json.load(f)["tableau_auth"][0]
            assert saved["personal_access_token"] == "pat-secret"
            assert saved["auth_token"] == "tok"

    def test_redact_proxy_hides_credentials(self):
        assert Session._redact_proxy("http://user:pw@proxy:8080") == "http://***@proxy:8080"
        assert Session._redact_proxy("user:pw@proxy:8080") == "***@proxy:8080"

    def test_redact_proxy_leaves_plain_proxy_alone(self):
        assert Session._redact_proxy("http://proxy:8080") == "http://proxy:8080"
        assert Session._redact_proxy(None) is None

    def test_redact_http_options_does_not_modify_original(self):
        options = {"proxies": {"http": "http://u:p@proxy"}, "timeout": 5}
        redacted = Session._redact_http_options(options)
        assert redacted["proxies"] == {"http": "http://***@proxy"}
        assert redacted["timeout"] == 5
        assert options["proxies"] == {"http": "http://u:p@proxy"}

    def test_proxy_credentials_not_logged_when_connecting(self):
        session = Session()
        session.server_url = "fakehost"
        session.proxy = "http://user:secretpw@proxy:8080"
        with self.assertLogs(session.logger, level="DEBUG") as logs:
            session._open_connection_with_opts()
        assert "secretpw" not in " ".join(logs.output)


class SessionLogicFixTests(unittest.TestCase):
    def test_base_url_keeps_port_without_scheme(self):
        assert Session()._get_server_base_url("my-server:8080") == "https://my-server:8080"
        assert Session()._get_server_base_url("localhost:8080/some/path") == "https://localhost:8080"

    def test_base_url_keeps_port_with_scheme(self):
        assert Session()._get_server_base_url("http://my-server:8080/x") == "http://my-server:8080"

    def test_password_file_trailing_newline_is_stripped(self):
        for content in ("secret\n", "secret\r\n", "secret"):
            with tempfile.TemporaryDirectory() as directory:
                path = os.path.join(directory, "pw.txt")
                with open(path, "w", newline="") as f:
                    f.write(content)
                assert Session._read_password_from_file(path) == "secret", repr(content)

    def test_timeout_zero_and_negative_become_zero(self):
        assert Session.timeout_as_integer(logger, -5, None) == 0
        assert Session.timeout_as_integer(logger, 0, None) == 0

    def test_timeout_invalid_new_value_falls_back_to_stored(self):
        assert Session.timeout_as_integer(logger, -5, 7) == 7

    def test_proxy_applies_to_http_and_https(self):
        session = Session()
        session.server_url = "https://fakehost"
        session.proxy = "proxy:8080"
        session.no_proxy = False
        connection = session._open_connection_with_opts()
        assert connection._http_options["proxies"] == {"http": "proxy:8080", "https": "proxy:8080"}

    def test_no_proxy_overrides_proxy(self):
        session = Session()
        session.server_url = "https://fakehost"
        session.proxy = "proxy:8080"
        session.no_proxy = True
        connection = session._open_connection_with_opts()
        assert connection._http_options["proxies"] is None

    def test_print_server_info_shows_token_name_only_when_set(self):
        session = Session()
        session.server_url = "http://srvr"
        session.username = "me"
        with self.assertLogs(session.logger, level="INFO") as logs:
            session._print_server_info()
        assert "Token Name" not in " ".join(logs.output)
        session.token_name = "mytoken"
        session.certificate = "cert.pem"
        with self.assertLogs(session.logger, level="INFO") as logs:
            session._print_server_info()
        output = " ".join(logs.output)
        assert "Token Name: mytoken" in output
        assert "Certificate: cert.pem" in output

    def test_clear_data_forgets_server_and_saved_target(self):
        session = Session()
        session.server_url = "http://srvr"
        session._saved_server_url = "http://srvr"
        session._saved_site_name = "site"
        with mock.patch.object(Session, "_remove_json"):
            session._clear_data()
        assert session.server_url is None
        assert session._saved_server_url is None
        assert session._saved_site_name is None

    def test_empty_session_file_is_wiped_once(self):
        session = Session()
        with mock.patch.object(Session, "_wipe_bad_json") as mock_wipe:
            session._save_data_from_json([None])
        mock_wipe.assert_called_once()


class LoadSessionFileTests(unittest.TestCase):
    def test_file_missing_newer_keys_still_loads(self):
        session = Session()
        with mock.patch.object(Session, "_wipe_bad_json") as mock_wipe:
            session._save_data_from_json([{"auth_token": "tok", "server": "http://srvr", "site_name": "s"}])
        mock_wipe.assert_not_called()
        assert session.auth_token == "tok"
        assert session.server_url == "http://srvr"
        assert session.token_file is None
        assert session.no_prompt is False
        assert session._saved_server_url == "http://srvr"
        assert session._saved_site_name == "s"


class UpdateSessionDataTests(unittest.TestCase):
    def _args(self, **overrides):
        args = Namespace(**vars(args_to_mock))
        for key, value in overrides.items():
            setattr(args, key, value)
        return args

    def test_site_default_becomes_empty(self):
        session = Session()
        session._update_session_data(self._args(site_name="Default"))
        assert session.site_name == ""

    def test_site_name_keeps_its_case(self):
        session = Session()
        session._update_session_data(self._args(site_name="MySite"))
        assert session.site_name == "MySite"

    def test_username_is_lowercased(self):
        session = Session()
        session._update_session_data(self._args(username="Me"))
        assert session.username == "me"

    def test_new_server_resets_saved_site(self):
        session = Session()
        session.site_name = "oldsite"
        session._update_session_data(self._args(server="other-server.com"))
        assert session.server_url == "https://other-server.com"
        assert session.site_name == ""

    def test_new_server_keeps_explicitly_given_site(self):
        session = Session()
        session.site_name = "oldsite"
        session._update_session_data(self._args(server="other-server.com", site_name="newsite"))
        assert session.site_name == "newsite"

    def test_no_args_keeps_saved_values(self):
        session = Session()
        session.server_url = "https://saved.com"
        session.site_name = "saved"
        session.username = "someone"
        session._update_session_data(self._args())
        assert (session.server_url, session.site_name, session.username) == ("https://saved.com", "saved", "someone")


class SignInTests(unittest.TestCase):
    def _session(self, server):
        session = Session()
        session.tableau_server = server
        session.server_url = "http://srvr"
        return session

    def test_sign_in_exits_when_server_rejects_credentials(self):
        server = mock.MagicMock()
        server.auth.sign_in.side_effect = Exception("401001")
        with mock.patch("tabcmd.commands.auth.session.Errors.exit_with_error", side_effect=SystemExit) as mock_exit:
            with self.assertRaises(SystemExit):
                self._session(server)._sign_in(mock.MagicMock())
        assert mock_exit.call_args[1]["exception"] is not None

    def test_sign_in_exits_when_validation_fails(self):
        server = mock.MagicMock()
        server.is_signed_in.return_value = False
        with mock.patch("tabcmd.commands.auth.session.Errors.exit_with_error", side_effect=SystemExit) as mock_exit:
            with self.assertRaises(SystemExit):
                self._session(server)._sign_in(mock.MagicMock())
        assert mock_exit.call_args[1]["message"] == "Sign in failed"

    def test_sign_in_saves_ids_and_token(self):
        server = mock.MagicMock()
        server.site_id, server.user_id, server.auth_token = "s", "u", "t"
        _set_mock_signin_validation_succeeds(server, "me")
        session = self._session(server)
        assert session._sign_in(mock.MagicMock()) is server
        assert (session.site_id, session.user_id, session.auth_token) == ("s", "u", "t")


class ValidateExistingSigninTests(unittest.TestCase):
    def _session(self, server):
        session = Session()
        session.tableau_server = server
        session.user_id = "u"
        return session

    def test_returns_none_when_not_signed_in(self):
        server = mock.MagicMock()
        server.is_signed_in.return_value = False
        assert self._session(server)._validate_existing_signin() is None

    def test_returns_none_on_server_error(self):
        server = mock.MagicMock()
        server.is_signed_in.return_value = True
        server.users.get_by_id.side_effect = TSC.ServerResponseError("401002", "Unauthorized", "")
        assert self._session(server)._validate_existing_signin() is None

    def test_returns_none_on_unexpected_error(self):
        server = mock.MagicMock()
        server.is_signed_in.return_value = True
        server.users.get_by_id.side_effect = RuntimeError("boom")
        assert self._session(server)._validate_existing_signin() is None

    def test_fills_in_username_from_server(self):
        server = mock.MagicMock()
        _set_mock_signin_validation_succeeds(server, "fromserver")
        session = self._session(server)
        session.username = None
        assert session._validate_existing_signin() is server
        assert session.username == "fromserver"


class SavedCredentialsTests(unittest.TestCase):
    def test_no_previous_login_gives_no_credentials(self):
        session = Session()
        session.last_login_using = None
        assert session._get_saved_credentials() is None

    def test_saved_token_login_uses_saved_pat(self):
        session = Session()
        session.last_login_using = "token"
        session.token_name = "tn"
        session.token_value = "secret"
        session.site_name = "site"
        auth = session._get_saved_credentials()
        assert isinstance(auth, TSC.PersonalAccessTokenAuth)
        assert (auth.token_name, auth.personal_access_token) == ("tn", "secret")

    @mock.patch("getpass.getpass", return_value="typed")
    def test_saved_username_login_prompts_for_password(self, mock_pass):
        session = Session()
        session.last_login_using = "username"
        session.username = "me"
        auth = session._get_saved_credentials()
        mock_pass.assert_called_once()
        assert isinstance(auth, TSC.TableauAuth)
        assert auth.password == "typed"


class NoCookieTests(unittest.TestCase):
    def _run(self, no_cookie):
        server = mock.MagicMock()
        server.site_id, server.user_id, server.auth_token = "s", "u", "t"
        _set_mock_signin_validation_succeeds(server, "me")
        args = Namespace(**vars(args_to_mock))
        args.username, args.password, args.server, args.no_cookie = "me", "pw", "http://srvr", no_cookie
        with (
            mock.patch.object(Session, "_open_connection_with_opts", return_value=server),
            mock.patch.object(Session, "_save_session_to_json") as mock_save,
            mock.patch.object(Session, "_remove_json") as mock_remove,
        ):
            Session().create_session(args, None)
        return mock_save, mock_remove

    def test_no_cookie_removes_session_file_and_does_not_save(self):
        mock_save, mock_remove = self._run(no_cookie=True)
        mock_remove.assert_called()
        mock_save.assert_not_called()

    def test_default_saves_session_file(self):
        mock_save, _ = self._run(no_cookie=False)
        mock_save.assert_called_once()


class RemoveAndWipeSessionFileTests(unittest.TestCase):
    def test_remove_json_deletes_existing_file(self):
        session = Session()
        with (
            mock.patch.object(Session, "_json_exists", return_value=True),
            mock.patch.object(Session, "_get_file_path", return_value="/tmp/tableau_auth.json"),
            mock.patch.object(Session, "_save_file") as mock_save,
            mock.patch("tabcmd.commands.auth.session.os.path.exists", return_value=True),
            mock.patch("tabcmd.commands.auth.session.os.remove") as mock_remove,
        ):
            session._remove_json()
        mock_save.assert_called_once_with({})
        mock_remove.assert_called_once_with("/tmp/tableau_auth.json")

    def test_remove_json_does_nothing_when_no_file(self):
        session = Session()
        with (
            mock.patch.object(Session, "_json_exists", return_value=False),
            mock.patch.object(Session, "_save_file") as mock_save,
        ):
            session._remove_json()
        mock_save.assert_not_called()

    def test_remove_json_logs_error_and_continues_when_it_fails(self):
        session = Session()
        with (
            mock.patch.object(Session, "_json_exists", return_value=True),
            mock.patch.object(Session, "_get_file_path", return_value="/tmp/tableau_auth.json"),
            mock.patch.object(Session, "_save_file", side_effect=OSError("locked")),
            mock.patch.object(session, "logger") as mock_logger,
        ):
            session._remove_json()
        assert "check and remove manually" in mock_logger.error.call_args_list[0][0][0]

    def test_wipe_bad_json_removes_file(self):
        session = Session()
        with mock.patch.object(Session, "_remove_json") as mock_remove:
            session._wipe_bad_json(ValueError("bad"), "Error reading session file")
        mock_remove.assert_called_once()

    def test_unreadable_json_file_is_wiped(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "tableau_auth.json")
            with open(path, "w") as f:
                f.write("{not json")
            session = Session()
            with (
                mock.patch.object(Session, "_get_file_path", return_value=path),
                mock.patch.object(Session, "_json_exists", return_value=True),
                mock.patch.object(Session, "_remove_json") as mock_remove,
            ):
                session._read_from_json()
        mock_remove.assert_called_once()


class OpenConnectionFailureTests(unittest.TestCase):
    """_open_connection_with_opts exits the process on failure; callers that fall back must survive that."""

    def _session_with_bad_url(self):
        session = Session()
        session.auth_token = "t"
        session.site_id = "s"
        session.user_id = "u"
        session.server_url = "http://[bad"
        session._saved_server_url = "http://[bad"
        session._saved_site_name = session.site_name
        return session

    def test_restore_falls_back_when_connection_cannot_be_opened(self):
        assert self._session_with_bad_url()._restore_saved_session() is None

    def test_logout_clears_local_data_when_connection_cannot_be_opened(self):
        session = self._session_with_bad_url()
        with mock.patch.object(Session, "_remove_json") as mock_remove:
            session.end_session_and_clear_data()
        mock_remove.assert_called_once()
        assert session.auth_token is None


class SaveFilePermissionTests(unittest.TestCase):
    def test_file_is_still_written_when_chmod_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "tableau_auth.json")
            session = Session()
            with (
                mock.patch.object(Session, "_get_file_path", return_value=path),
                mock.patch("tabcmd.commands.auth.session.os.chmod", side_effect=OSError("not permitted")),
            ):
                session.token_value = "pat-secret"
                session._save_file(session._serialize_for_save())
            with open(path) as f:
                assert json.load(f)["tableau_auth"][0]["personal_access_token"] == "pat-secret"


class LogoutTests(unittest.TestCase):
    def _saved_session(self):
        session = Session()
        session.auth_token = "tok"
        session.site_id = "site-1"
        session.user_id = "user-1"
        session.server_url = "http://srvr"
        return session

    def test_logout_signs_out_saved_token_on_server(self):
        session = self._saved_session()
        server = mock.MagicMock(name="saved_session_server")
        with (
            mock.patch.object(Session, "_open_connection_with_opts", return_value=server),
            mock.patch.object(Session, "_remove_json"),
        ):
            session.end_session_and_clear_data()
        server._set_auth.assert_called_once_with("site-1", "user-1", "tok")
        server.auth.sign_out.assert_called_once()
        assert session.auth_token is None

    def test_logout_of_live_session_signs_out_once(self):
        session = self._saved_session()
        live_server = mock.MagicMock(name="live_server")
        session.tableau_server = live_server
        with (
            mock.patch.object(Session, "_open_connection_with_opts") as mock_open_conn,
            mock.patch.object(Session, "_remove_json"),
        ):
            session.end_session_and_clear_data()
        live_server.auth.sign_out.assert_called_once()
        mock_open_conn.assert_not_called()

    def test_logout_still_clears_local_data_when_server_sign_out_fails(self):
        session = self._saved_session()
        server = mock.MagicMock(name="saved_session_server")
        server.auth.sign_out.side_effect = Exception("401 Unauthorized")
        with (
            mock.patch.object(Session, "_open_connection_with_opts", return_value=server),
            mock.patch.object(Session, "_remove_json") as mock_remove,
        ):
            session.end_session_and_clear_data()
        mock_remove.assert_called_once()
        assert session.auth_token is None

    def test_logout_with_no_saved_session_makes_no_connection(self):
        session = Session()
        session.auth_token = None
        with (
            mock.patch.object(Session, "_open_connection_with_opts") as mock_open_conn,
            mock.patch.object(Session, "_remove_json"),
        ):
            session.end_session_and_clear_data()
        mock_open_conn.assert_not_called()


def _set_mock_tsc_not_signed_in(mock_tsc):
    tsc_in_test = mock.MagicMock(name="manually mocking tsc")
    tsc_in_test.is_signed_in.return_value = False  # CreateSessionTests.return_False
    tsc_in_test.server_info.get.return_value = Exception
    return tsc_in_test


def _set_mock_tsc_sign_in_succeeds(mock_tsc):
    tscauth_mock = mock.MagicMock(name="tsc.auth")
    mock_tsc.auth = tscauth_mock
    mock_tsc.auth_token = "cookiieeeee"
    mock_tsc.site_id = "1"
    mock_tsc.user_id = "0"


def _set_mock_signin_validation_succeeds(mock_tsc, username):
    mock_u_factory = MagicMock("user")
    mock_u = mock_u_factory()
    mock_tsc.users.get_by_id.return_value = mock_u
    mock_u.name = username
    mock_tsc.is_signed_in.return_value = True


class TimeoutArgTests(unittest.TestCase):
    def test_timeout_as_integer_stored_int(self):
        result = Session.timeout_as_integer(logger, 1, None)
        assert result == 1

    def test_timeout_as_integer_new_int(self):
        result = Session.timeout_as_integer(logger, None, 3)
        assert result == 3

    def test_timeout_as_integer_no_value(self):
        result = Session.timeout_as_integer(logger, None, None)
        assert result == 0

    def test_timeout_as_integer_stored_char(self):
        result = Session.timeout_as_integer(logger, "ab", None)
        assert result == 0


class ConnectionOptionsTest(unittest.TestCase):
    def test_user_agent(self):
        mock_session = Session()
        mock_session.server_url = "fakehost"
        connection = mock_session._open_connection_with_opts()
        assert connection._http_options["headers"]["User-Agent"].startswith("Tabcmd/")

    def test_no_certcheck(self):
        mock_session = Session()
        mock_session.server_url = "fakehost"
        mock_session.no_certcheck = True
        mock_session.site_id = "s"
        mock_session.user_id = "u"
        connection = mock_session._open_connection_with_opts()
        assert connection._http_options["verify"] == False

    def test_cert(self):
        mock_session = Session()
        mock_session.server_url = "fakehost"
        mock_session.site_id = "s"
        mock_session.user_id = "u"
        mock_session.certificate = "my-cert-info"
        connection = mock_session._open_connection_with_opts()
        assert connection._http_options["cert"] == mock_session.certificate

    def test_proxy_stuff(self):
        mock_session = Session()
        mock_session.server_url = "fakehost"
        mock_session.site_id = "s"
        mock_session.user_id = "u"
        mock_session.proxy = "proxy:port"
        connection = mock_session._open_connection_with_opts()
        assert connection._http_options["proxies"] == {"http": mock_session.proxy, "https": mock_session.proxy}

    def test_timeout(self):
        mock_session = Session()
        mock_session.server_url = "fakehost"
        mock_session.site_id = "s"
        mock_session.user_id = "u"
        mock_session.timeout = 10
        connection = mock_session._open_connection_with_opts()
        assert connection._http_options["timeout"] == 10


class GetServerBaseUrlTests(unittest.TestCase):
    """Unit tests for Session._get_server_base_url."""

    def setUp(self):
        self.session = Session()

    def test_no_scheme_defaults_to_https(self):
        result = self.session._get_server_base_url("my-tableau-server.com")
        assert result == "https://my-tableau-server.com", result

    def test_explicit_http_stays_http(self):
        result = self.session._get_server_base_url("http://my-tableau-server.com")
        assert result == "http://my-tableau-server.com", result

    def test_explicit_https_stays_https(self):
        result = self.session._get_server_base_url("https://my-tableau-server.com")
        assert result == "https://my-tableau-server.com", result

    def test_no_scheme_with_path_component(self):
        result = self.session._get_server_base_url("my-tableau-server.com/some/path")
        assert result == "https://my-tableau-server.com", result

    def test_no_scheme_with_trailing_slash(self):
        result = self.session._get_server_base_url("my-tableau-server.com/")
        assert result == "https://my-tableau-server.com", result

    def test_https_with_path_strips_path(self):
        result = self.session._get_server_base_url("https://my-tableau-server.com/some/path")
        assert result == "https://my-tableau-server.com", result


"""

This is too slow for unit tests.
class TimeoutIntegrationTest(unittest.TestCase):
    def test_connection_times_out(self):
        test_args = Namespace(**vars(args_to_mock))
        new_session = Session()
        test_args.timeout = 2
        test_args.username = "u"
        test_args.password = "p"

        test_args.server = "https://nothere.com"
        with self.assertRaises(SystemExit):
            new_session.create_session(test_args, None)



class CookieTests(unittest.TestCase):

    def test_no_file_if_no_cookie(self):
        assert False, 'feature not implemented'


class LastLoggedInTests(unittest.TestCase):

    def test_last_logged_in_username(self):
        assert False, 'test not implemented'

    def test_last_logged_in_token(self):
        assert False, 'test not implemented'

    def test_no_previous_login(self):
        assert False, 'test not implemented'
"""
