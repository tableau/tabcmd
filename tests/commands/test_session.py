import logging
from argparse import Namespace
import unittest
from unittest import mock
from unittest.mock import MagicMock

from tabcmd.commands.auth.session import Session

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
        test_session._save_session_to_json()
        assert mock_json.dump.was_called()

    def clear_session(self, mock_open, mock_path, mock_json):
        _set_mocks_for_json_file_exists(mock_path, mock_json)
        test_session = Session()
        test_session.username = "USN"
        test_session.server = "SRVR"
        test_session._clear_data()
        assert test_session.username is None
        assert test_session.server is None

    def test_json_not_present(self, mock_open, mock_path, mock_json):
        _set_mocks_for_json_file_exists(mock_path, mock_json, does_it_exist=False)
        assert mock_open.was_not_called()

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
        active_session = Session()
        active_session.username = "user"
        active_session.site_name = ""
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
        active_session.site_name = ""
        auth = active_session._create_new_credential(None, Session.PASSWORD_CRED_TYPE)
        assert mock_pass.has_been_called()
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
        session: Session = Session()
        test_args = Namespace(**vars(args_to_mock))
        session._update_session_data(test_args)
        assert session._allow_prompt() is True, test_args

    def test_show_prompt_if_user_said_yes(self):
        session: Session = Session()
        test_args = Namespace(**vars(args_to_mock))
        test_args.prompt = True
        session._update_session_data(test_args)
        assert session._allow_prompt() is True, test_args

    def test_dont_show_prompt_if_user_said_no(self):
        session: Session = Session()
        test_args = Namespace(**vars(args_to_mock))
        test_args.no_prompt = True
        session._update_session_data(test_args)
        assert session._allow_prompt() is False, test_args


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
        assert mock_tsc.has_been_called()

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
        assert mock_tsc.has_been_called()

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
        assert mock_tsc.has_been_called()

    @mock.patch("tableauserverclient.Server")
    def test_load_saved_session_data(self, mock_tsc, mock_pass, mock_file, mock_path, mock_json):
        _set_mocks_for_json_file_exists(mock_path, mock_json)
        _set_mocks_for_json_file_saved_username(mock_json, "auth_token", "username")
        test_args = Namespace(**vars(args_to_mock))
        new_session = Session()
        new_session._read_existing_state()
        new_session._update_session_data(test_args)
        assert new_session, new_session
        assert new_session.username == "username", new_session.username
        assert new_session.server_url == fakeserver, new_session.server_url
        assert mock_tsc.has_been_called()

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
        assert mock_tsc.has_been_called()

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
        assert mock_pass.has_been_called()
        assert auth is not None, auth
        assert auth.auth_token is not None, auth.auth_token
        assert auth.auth_token == "cookiieeeee"
        assert new_session.username == test_username, new_session
        assert mock_tsc.use_server_version.has_been_called()


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

    # should test connection doesn't time out?


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
        assert connection._http_options["proxies"] == {"http": mock_session.proxy}

    def test_timeout(self):
        mock_session = Session()
        mock_session.server_url = "fakehost"
        mock_session.site_id = "s"
        mock_session.user_id = "u"
        mock_session.timeout = 10
        connection = mock_session._open_connection_with_opts()
        assert connection._http_options["timeout"] == 10


"""
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
