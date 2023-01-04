import getpass
import json
import os

import requests
import tableauserverclient as TSC
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from tabcmd.version import version
from tabcmd.commands.constants import Errors
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


class Session:
    """
    Session class handles all authentication related work
    """

    TOKEN_CRED_TYPE = "token"
    PASSWORD_CRED_TYPE = "password"

    TOKEN_CRED_TYPE = "token"
    PASSWORD_CRED_TYPE = "password"

    def __init__(self):
        self.username = None
        # we don't store the password
        self.user_id = None
        self.auth_token = None
        self.token_name = None
        self.token_value = None
        self.password_file = None
        self.site_name = None  # The site name, e.g 'alpodev'
        self.site_id = None  # The site id, e.g 'abcd-1234-1234-1244-1234'
        self.server_url = None
        self.last_command = None  # for when we have to renew the session then re-try
        self.last_login_using = None

        self.no_prompt = False
        self.certificate = None
        self.no_certcheck = False
        self.no_proxy = True
        self.proxy = None
        self.timeout = None

        self.logging_level = "info"
        self._read_from_json()
        self.logger = log(__name__, self.logging_level)  # instantiate here mostly for tests
        self.tableau_server = None  # this one is an object that doesn't get persisted in the file

    # called before we connect to the server
    # generally, we don't want to overwrite stored data with nulls
    def _update_session_data(self, args):
        # user id and site id are never passed in as args
        # last_login_using and tableau_server are internal data
        # self.command = args.???
        self.username = args.username or self.username or ""
        self.username = self.username.lower()
        self.server_url = args.server or self.server_url or "http://localhost"
        self.server_url = self.server_url.lower()
        if args.server is not None:
            self.site_name = None
        self.site_name = args.site_name or self.site_name or ""
        self.site_name = self.site_name.lower()
        if self.site_name == "default":
            self.site_name = ""
        self.logging_level = args.logging_level or self.logging_level
        self.password_file = args.password_file
        self.token_name = args.token_name or self.token_name
        self.token_value = args.token_value or self.token_value

        self.no_prompt = args.no_prompt or self.no_prompt
        self.certificate = args.certificate or self.certificate
        self.no_certcheck = args.no_certcheck or self.no_certcheck
        self.no_proxy = args.no_proxy or self.no_proxy
        self.proxy = args.proxy or self.proxy
        self.timeout = self.timeout_as_integer(self.logger, args.timeout, self.timeout)

    @staticmethod
    def timeout_as_integer(logger, option_1, option_2):
        result = None
        if option_1:
            try:
                result = int(option_1)
            except Exception as anyE:
                result = 0
        if option_2 and (not result or result <= 0):
            try:
                result = int(option_2)
            except Exception as anyE:
                result = 0
        if not option_1 and not option_2:
            logger.debug(_("setsetting.status").format("timeout", "None"))
        elif not result or result <= 0:
            logger.warning(_("sessionoptions.errors.bad_timeout").format("--timeout", result))
        return result or 0

    @staticmethod
    def _read_password_from_file(filename):
        credential = None
        with open(str(filename), "r") as file_contents:
            reader = file_contents.readlines()
            for row in reader:
                credential = row
            return credential

    def _allow_prompt(self):
        try:
            return not self.no_prompt
        except Exception:
            return True

    def _create_new_credential(self, password, credential_type):
        if password is None:
            if self.password_file:
                password = Session._read_password_from_file(self.password_file)
            elif self._allow_prompt():
                password = getpass.getpass(_("session.password"))
            else:
                Errors.exit_with_error(self.logger, _("session.errors.script_no_password"))

        if credential_type == Session.PASSWORD_CRED_TYPE and self.username and password:
            credentials = TSC.TableauAuth(self.username, password, site_id=self.site_name)
            self.last_login_using = "username"
            return credentials
        elif credential_type == Session.TOKEN_CRED_TYPE and self.token_name:
            credentials = self._create_new_token_credential()
            return credentials
        else:
            Errors.exit_with_error(self.logger, _("session.errors.missing_arguments").format(""))

    def _create_new_token_credential(self):
        if self.token_value:
            token = self.token_value
        elif self.password_file:
            token = Session._read_password_from_file(self.password_file)
        elif self._allow_prompt():
            token = getpass.getpass("Token:")
        else:
            Errors.exit_with_error(self.logger, _("session.errors.missing_arguments").format("token"))

        if self.token_name and token:
            credentials = TSC.PersonalAccessTokenAuth(self.token_name, token, site_id=self.site_name)
            self.last_login_using = "token"
            return credentials
        else:
            Errors.exit_with_error(self.logger, _("session.errors.missing_arguments").format("token name"))

    def _set_connection_options(self) -> TSC.Server:
        self.logger.debug("Setting up request options")
        # args still to be handled here:
        # proxy, --no-proxy,
        # cert
        http_options = {"headers": {"User-Agent": "Tabcmd" + version}}
        if self.no_certcheck:
            http_options["verify"] = False
            urllib3.disable_warnings(category=InsecureRequestWarning)
        if self.proxy:
            # do we catch this error? "sessionoptions.errors.bad_proxy_format"
            self.logger.debug("Setting proxy: ", self.proxy)
        if self.timeout:
            http_options["timeout"] = self.timeout
        try:
            self.logger.debug(http_options)
            tableau_server = TSC.Server(self.server_url, http_options=http_options)

        except Exception as e:
            self.logger.debug(
                "Connection args: server {}, site {}, proxy {}, cert {}".format(
                    self.server_url, self.site_name, self.proxy, self.certificate
                )
            )
            Errors.exit_with_error(self.logger, "Failed to connect to server", e)

        self.logger.debug("Finished setting up connection")
        return tableau_server

    def _verify_server_connection_unauthed(self):
        try:
            self.tableau_server.use_server_version()
        except requests.exceptions.ReadTimeout as timeout_error:
            Errors.exit_with_error(
                self.logger,
                message="Timed out after {} seconds attempting to connect to server".format(self.timeout),
                exception=timeout_error,
            )
        except requests.exceptions.RequestException as requests_error:
            Errors.exit_with_error(
                self.logger, message="Error attempting to connect to the server", exception=requests_error
            )
        except Exception as e:
            Errors.exit_with_error(self.logger, exception=e)

    def _create_new_connection(self) -> TSC.Server:
        self.logger.info(_("session.new_session"))
        self._print_server_info()
        self.logger.info(_("session.connecting"))
        try:
            self.tableau_server = self._set_connection_options()
        except Exception as e:
            Errors.exit_with_error(self.logger, "Failed to connect to server", e)
        return self.tableau_server

    def _read_existing_state(self):
        if self._check_json():
            self._read_from_json()

    def _print_server_info(self):
        self.logger.info("=====   Server: {}".format(self.server_url))
        if self.username:
            self.logger.info("=====   Username: {}".format(self.username))
        else:
            self.logger.info("=====   Token Name: {}".format(self.token_name))
        site_display_name = self.site_name or "Default Site"
        self.logger.info(_("dataconnections.classes.tableau_server_site") + ": {}".format(site_display_name))

    def _validate_existing_signin(self):
        self.logger.info(_("session.continuing_session"))
        # when do these two messages show up? self.logger.info(_("session.auto_site_login"))
        try:
            if self.tableau_server and self.tableau_server.is_signed_in():
                response = self.tableau_server.users.get_by_id(self.user_id)
                self.logger.debug(response)
                if response.status_code.startswith("200"):
                    return self.tableau_server
        except TSC.ServerResponseError as e:
            self.logger.info(_("publish.errors.unexpected_server_response"), e)
        except Exception as e:
            self.logger.info(_("errors.internal_error.request.message"), e)
        return None

    # server connection created, not yet logged in
    def _sign_in(self, tableau_auth) -> TSC.Server:
        self.logger.debug(_("session.login") + self.server_url)
        self.logger.debug(_("listsites.output").format("", self.username or self.token_name, self.site_name))
        try:
            self.tableau_server.auth.sign_in(tableau_auth)  # it's the same call for token or user-pass
        except Exception as e:
            Errors.exit_with_error(self.logger, exception=e)
        try:
            self.site_id = self.tableau_server.site_id
            self.user_id = self.tableau_server.user_id
            self.auth_token = self.tableau_server._auth_token
            if not self.username:
                self.username = self.tableau_server.users.get_by_id(self.user_id).name
            self.logger.info(_("common.output.succeeded"))
        except Exception as e:
            Errors.exit_with_error(self.logger, e)
        self.logger.debug("Signed into {0}{1} as {2}".format(self.server_url, self.site_name, self.username))
        return self.tableau_server

    def _get_saved_credentials(self):
        if self.last_login_using == "username":
            credentials = self._create_new_credential(None, Session.PASSWORD_CRED_TYPE)
        elif self.last_login_using == "token":
            credentials = self._create_new_token_credential()
        else:
            return None
        if credentials:
            self.logger.info(_("session.options.password-file"))
        return credentials

    # external entry point:
    def create_session(self, args):
        signed_in_object = None
        # pull out cached info from json, then overwrite with new args if available
        self._read_existing_state()
        self._update_session_data(args)
        self.logging_level = args.logging_level or self.logging_level
        self.logger = self.logger or log(__class__.__name__, self.logging_level)

        credentials = None
        if args.password:
            self._end_session()
            # we don't save the password anywhere, so we pass it along directly
            credentials = self._create_new_credential(args.password, Session.PASSWORD_CRED_TYPE)
        elif args.password_file:
            self._end_session()
            if args.username:
                credentials = self._create_new_credential(args.password, Session.PASSWORD_CRED_TYPE)
            else:
                credentials = self._create_new_credential(args.password, Session.TOKEN_CRED_TYPE)
        elif args.token_value:
            self._end_session()
            credentials = self._create_new_token_credential()
        else:  # no login arguments given - look for saved info
            # maybe we're already signed in!
            if self.tableau_server:
                signed_in_object = self._validate_existing_signin()
            self.logger.debug(signed_in_object)
            # or maybe we at least have the credentials saved
            if not signed_in_object:
                credentials = self._get_saved_credentials()

        if credentials and not signed_in_object:
            # logging in, not using an existing session
            self.tableau_server = self._create_new_connection()
            self._verify_server_connection_unauthed()
            signed_in_object = self._sign_in(credentials)

        if not signed_in_object:
            message = "Run 'tabcmd login -h' for details on required arguments"
            Errors.exit_with_error(self.logger, _("session.errors.missing_arguments").format(message))
        if args.no_cookie:
            self._remove_json()
        else:
            self._save_session_to_json()
        return signed_in_object

    def end_session_and_clear_data(self):
        self._end_session()
        self.logger.info(_("session.logout"))
        self._clear_data()

    def _end_session(self):
        if self.tableau_server:
            self.tableau_server.auth.sign_out()
            self.tableau_server = None

    def _clear_data(self):
        self._remove_json()
        self.username = None
        self.user_id = None
        self.auth_token = None
        self.token_name = None
        self.token_value = None
        self.site_name = None
        self.site_id = None
        self.server = None
        self.last_login_using = None
        self.password_file = None

        self.last_command = None
        self.tableau_server = None

        self.certificate = None
        self.no_certcheck = None
        self.no_proxy = None
        self.proxy = None
        self.timeout = None

    # json file functions ----------------------------------------------------
    def _get_file_path(self):
        home_path = os.path.expanduser("~")
        file_path = os.path.join(home_path, "tableau_auth.json")
        return file_path

    def _read_from_json(self):
        if not self._check_json():
            return
        file_path = self._get_file_path()
        data = {}
        with open(str(file_path), "r") as file_contents:
            data = json.load(file_contents)
        try:
            for auth in data["tableau_auth"]:
                self.auth_token = auth["auth_token"]
                self.server_url = auth["server"]
                self.site_name = auth["site_name"]
                self.site_id = auth["site_id"]
                self.username = auth["username"]
                self.user_id = auth["user_id"]
                self.token_name = auth["personal_access_token_name"]
                self.token_value = auth["personal_access_token"]
                self.last_login_using = auth["last_login_using"]
                self.password_file = auth["password_file"]
                self.no_prompt = auth["no_prompt"]
                self.no_certcheck = auth["no_certcheck"]
                self.certificate = auth["certificate"]
                self.no_proxy = auth["no_proxy"]
                self.proxy = auth["proxy"]
                self.timeout = auth["timeout"]
        except KeyError as e:
            self.logger.debug(_("sessionoptions.errors.bad_password_file"), e)
            self._remove_json()
        except Exception as any_error:
            self.logger.info(_("session.new_session"))
            self._remove_json()

    def _check_json(self):
        home_path = os.path.expanduser("~")
        file_path = os.path.join(home_path, "tableau_auth.json")
        return os.path.exists(file_path)

    def _save_session_to_json(self):
        data = self._serialize_for_save()
        self._save_file(data)

    def _save_file(self, data):
        file_path = self._get_file_path()
        with open(str(file_path), "w") as f:
            json.dump(data, f)

    def _serialize_for_save(self):
        data = {"tableau_auth": []}
        data["tableau_auth"].append(
            {
                "auth_token": self.auth_token,
                "server": self.server_url,
                "username": self.username,
                "user_id": self.user_id,
                "site_name": self.site_name,
                "site_id": self.site_id,
                "personal_access_token_name": self.token_name,
                "personal_access_token": self.token_value,
                "last_login_using": self.last_login_using,
                "password_file": self.password_file,
                "no_prompt": self.no_prompt,
                "no_certcheck": self.no_certcheck,
                "certificate": self.certificate,
                "no_proxy": self.no_proxy,
                "proxy": self.proxy,
                "timeout": self.timeout,
            }
        )
        return data

    def _remove_json(self):
        file_path = self._get_file_path()
        self._save_file({})
        if os.path.exists(file_path):
            os.remove(file_path)
