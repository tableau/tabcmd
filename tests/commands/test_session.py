from argparse import Namespace
import unittest
from unittest import mock

from tabcmd.commands.auth.session import Session
import os

args_to_mock = Namespace(
    prompt=None,
    username=None,
    site=None,
    password=None,
    server=None,
    token_name=None,
    token=None,
    logging_level=None,
    no_certcheck=None,
    no_cookie=None,
    no_prompt=None,
)

mock_data_from_json = Namespace(
    token=None,  # this is the session token, not pat
    username=None,
    user_id=None,
    site_name=None,
    site_id=None,
    password=None,
    server=None,
    personal_access_token_name=None,
    personal_access_token=None,
    last_login_using=None
)


def _set_mocks_for_json_file_saved_username(mock_json_load, auth_token, username, password):
    mock_auth = vars(mock_data_from_json)
    mock_json_load.return_value = {'tableau_auth': [mock_auth]}
    mock_auth['token'] = auth_token
    mock_auth['password'] = password
    mock_auth['username'] = username
    mock_auth['last_login_using'] = 'username'
    print(mock_auth)


def _set_mocks_for_json_file_exists(mock_path, does_it_exist=True):
    os.path = mock_path
    mock_path.expanduser.return_value = ''
    mock_path.join.return_value = ''
    mock_path.exists.return_value = does_it_exist
    return mock_path


@mock.patch('json.dump')
@mock.patch('json.load')
@mock.patch('os.path')
@mock.patch('builtins.open')
class JsonTests(unittest.TestCase):

    def test_read_session_from_json(self, mock_open, mock_path, mock_load, mock_dump):
        _set_mocks_for_json_file_exists(mock_path)
        _set_mocks_for_json_file_saved_username(mock_load, 'AUTHTOKEN', 'USERNAME', 'PASSWORD')
        test_session = Session()
        test_session._read_from_json()
        assert test_session.auth_token == 'AUTHTOKEN'
        assert hasattr(test_session, 'password') is False, test_session
        assert test_session.username == 'USERNAME'

    def test_save_session_to_json(self, mock_open, mock_path, mock_load, mock_dump):
        _set_mocks_for_json_file_exists(mock_path)
        test_session = Session()
        test_session.username = 'USN'
        test_session.server = 'SRVR'
        test_session._save_token_to_json_file()
        assert mock_dump.was_called()


@mock.patch('getpass.getpass')
class BuildCredentialsTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # make sure any json data etc is cleared
        Session().end_session_and_clear_data()

    # Set: Create auth credentials
    # This first set of tests has no attributes set
    def test__create_new_token_credential_fails_no_args(self, mock_pass):
        test_args = Namespace(**vars(args_to_mock))
        active_session = Session()
        assert active_session._password is None, active_session._password
        with self.assertRaises(SystemExit):
            active_session._create_new_token_credential(test_args)

    def test__create_new_username_credential_fails_no_args(self, mock_pass):
        test_args = Namespace(**vars(args_to_mock))
        active_session = Session()
        assert active_session._password is None, active_session._password
        with self.assertRaises(SystemExit):
            active_session._create_new_username_credential(test_args)

    # These two already have a username saved and pass in a password as argument
    def test__create_new_token_credential_succeeds_new_token(self, mock_pass):
        test_args = Namespace(**vars(args_to_mock))
        test_args.token = 'gibberish'
        active_session = Session()
        assert active_session.token is None, active_session.token
        active_session.token_name = 'readable'
        auth = active_session._create_new_token_credential(test_args)
        assert auth is not None
        assert mock_pass.is_not_called()

    def test__create_new_username_credential_succeeds_new_password(self, mock_pass):
        test_args = Namespace(**vars(args_to_mock))
        test_args.password = 'pword1'
        active_session = Session()
        active_session.username = 'user'
        active_session.site = ''
        auth = active_session._create_new_username_credential(test_args)
        assert auth is not None

    # These two have a username and password saved
    def test__create_new_token_credential_succeeds_from_self(self, mock_pass):
        test_args = Namespace(**vars(args_to_mock))
        active_session = Session()
        active_session.token = 'gibberish2'
        active_session.token_name = 'readable2'
        auth = active_session._create_new_token_credential(test_args)
        assert auth is not None
        assert auth.token_name == 'readable2', auth
        assert auth.personal_access_token == 'gibberish2', auth

    # this one calls getpass because we don't store the password
    def test__create_new_username_credential_succeeds_from_self(self, mock_pass):
        test_args = Namespace(**vars(args_to_mock))
        active_session = Session()
        active_session.username = 'user3'
        active_session.site = ''
        auth = active_session._create_new_username_credential(test_args)
        assert auth is not None
        assert auth.username == 'user3', auth
        assert auth.password == mock_pass(), auth

    # These two have all info in args
    # It fails because the method expects username/tokenname to already be saved to self
    def test__create_new_token_credential_succeeds_from_args(self, mock_pass):
        test_args = Namespace(**vars(args_to_mock))
        test_args.token = 'gibberish'
        test_args.token_name = 'readable'
        active_session = Session()
        auth = active_session._create_new_token_credential(test_args)

    def test__create_new_username_credential_succeeds_from_args(self, mock_pass):
        test_args = Namespace(**vars(args_to_mock))
        test_args.username = 'user'
        test_args.password = 'pwordddddd'
        active_session = Session()
        active_session.site = ''
        auth = active_session._create_new_username_credential(test_args)


class PromptingTests(unittest.TestCase):

    def test_show_prompt_if_user_didnt_say(self):
        test_args = Namespace(**vars(args_to_mock))
        assert Session._allow_prompt(test_args) is True, test_args

    def test_show_prompt_if_user_said_yes(self):
        test_args = Namespace(**vars(args_to_mock))
        test_args.prompt = True
        assert Session._allow_prompt(test_args) is True, test_args

    def test_dont_show_prompt_if_user_said_no(self):
        test_args = Namespace(**vars(args_to_mock))
        test_args.no_prompt = True
        assert Session._allow_prompt(test_args) is False, test_args


"""
These tests all call the top-level method create_session, and mock out
the json file, and the TSC.Server calls
"""


@mock.patch('json.dump')
@mock.patch('json.load')
@mock.patch('os.path')
@mock.patch('builtins.open')
@mock.patch('getpass.getpass')
class CreateSessionTests(unittest.TestCase):

    @mock.patch('tableauserverclient.Server')
    def test_create_session_first_time_no_args(
            self, mock_tsc, mock_pass, mock_file, mock_path, mock_json_load, mock_json_dump):
        mock_path = _set_mocks_for_json_file_exists(mock_path, False)
        assert mock_path.exists('anything') is False
        test_args = Namespace(**vars(args_to_mock))
        new_session = Session()
        with self.assertRaises(SystemExit):
            auth = new_session.create_session(test_args)

    @mock.patch('tableauserverclient.Server')
    def test_create_session_first_time_with_token_arg(
            self, mock_tsc, mock_pass, mock_file, mock_path, mock_json_load, mock_json_dump):
        mock_path = _set_mocks_for_json_file_exists(mock_path, False)
        assert mock_path.exists('anything') is False
        test_args = Namespace(**vars(args_to_mock))
        test_args.token_name = 'tn'
        test_args.token = 'foo'
        new_session = Session()
        auth = new_session.create_session(test_args)
        assert auth is not None, auth
        assert auth.auth_token is not None, auth.auth_token
        assert auth.auth_token.name is not None, auth.auth_token
        assert new_session.token == 'foo', new_session
        assert new_session.token_name == 'tn', new_session

    @mock.patch('tableauserverclient.Server')
    def test_create_session_first_time_with_password_arg(
            self, mock_tsc, mock_pass, mock_file, mock_path, mock_json_load, mock_json_dump):
        mock_path = _set_mocks_for_json_file_exists(mock_path, False)
        test_args = Namespace(**vars(args_to_mock))
        test_args.username = 'uuuu'
        test_args.password = 'pppp'
        new_session = Session()

        auth = new_session.create_session(test_args)
        assert auth is not None, auth
        assert auth.auth_token is not None, auth.auth_token
        assert new_session._password is None, new_session
        assert new_session.username == 'uuuu', new_session
        assert mock_tsc.has_been_called()

    @mock.patch('tableauserverclient.Server')
    def test_create_session_with_active_session_saved(
            self, mock_tsc, mock_pass, mock_file, mock_path, mock_json_load, mock_json_dump):
        _set_mocks_for_json_file_exists(mock_path, True)
        _set_mocks_for_json_file_saved_username(mock_json_load, 'auth_token', None, 'pppppword')
        test_args = Namespace(**vars(args_to_mock))
        test_args.token = 'tn'
        test_args.token_name = 'tnnnn'
        new_session = Session()

        auth = new_session.create_session(test_args)
        assert auth is not None, auth
        assert auth.auth_token is not None, auth.auth_token
        assert mock_tsc.has_been_called()

    @mock.patch('tableauserverclient.Server')
    def test_create_session_with_saved_expired_username_session(
            self, mock_tsc, mock_pass, mock_file, mock_path, mock_json_load, mock_json_dump):
        _set_mocks_for_json_file_saved_username(mock_json_load, 'auth_token', 'username', 'pppppword')
        _set_mocks_for_json_file_exists(mock_path, True)
        tsc_under_test = CreateSessionTests._set_mock_tsc_not_signed_in(mock_tsc)
        CreateSessionTests._set_mock_tsc_sign_in_succeeds(tsc_under_test)
        args_to_mock.password = 'pppppword'
        test_args = Namespace(**vars(args_to_mock))
        new_session = Session()
        auth = new_session.create_session(test_args)
        assert auth is not None, auth
        assert auth.auth_token is not None, auth.auth_token
        assert auth.auth_token == 'cookiieeeee'
        assert new_session._password is None, new_session
        assert new_session.username == 'username', new_session
        assert mock_tsc.use_server_version.has_been_called()

    @staticmethod
    def _set_mock_tsc_not_signed_in(mock_tsc):
        tsc_in_test = mock.MagicMock(name='manually mocking tsc')
        mock_tsc.return_value = tsc_in_test
        tsc_in_test.is_signed_in.return_value = False  # CreateSessionTests.return_False
        tsc_in_test.server_info.get.return_value = Exception
        return tsc_in_test

    @staticmethod
    def _set_mock_tsc_sign_in_succeeds(mock_tsc):
        tscauth_mock = mock.MagicMock(name='tsc.auth')
        mock_tsc.auth = tscauth_mock
        mock_tsc.auth_token = 'cookiieeeee'
        mock_tsc.site_id = '1'
        mock_tsc.user_id = '0'


@mock.patch('tableauserverclient.Server')
class ConnectionOptionsTest(unittest.TestCase):

    def test_certcheck_on(self, mock_tsc):
        mock_tsc.add_http_options = mock.MagicMock()
        test_args = Namespace(**vars(args_to_mock))
        test_args.no_certcheck = True
        server_url = 'anything'
        Session._set_connection_options(server_url, test_args)
        assert mock_tsc.add_http_options.has_been_called()

    def test_certcheck_off(self, mock_tsc):
        test_args = Namespace(**vars(args_to_mock))
        server_url = 'anything'
        Session._set_connection_options(server_url, test_args)
        mock_tsc.add_http_options.assert_not_called()

    """
    def test_cert(self, mock_tsc):
        assert False, 'feature not implemented'

    def test_proxy_stuff(self, mock_tsc):
        assert False, 'feature not implemented'

    def test_timeout(self, mock_tsc):
        assert False, 'feature not implemented'

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
