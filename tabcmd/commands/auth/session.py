import getpass
import json
import os

import requests
import tableauserverclient as TSC
from urllib3.exceptions import InsecureRequestWarning

from tabcmd.commands.constants import Errors
from tabcmd.execution.logger_config import log


class Session:
    """
    Session class handles all authentication related work
    """

    def __init__(self):
        self.username = None
        # we don't store the password
        self.user_id = None
        self.auth_token = None
        self.token_name = None
        self.token = None
        self.password_file = None
        self.site_name = None  # The site name, or 'alpodev'
        self.site_id = None  # The site id, or 'abcd-1234-1234-1244-1234'
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
        self.logger = log(__name__, self.logging_level)
        self._read_from_json()
        self.tableau_server = None  # this one is an object that doesn't get persisted in the file

    # called before we connect to the server
    # generally, we don't want to overwrite stored data with nulls
    def _update_session_data(self, args):
        # user id and site id are never passed in as args
        # last_login_using and tableau_server are internal data
        # self.command = args.???
        self.username = args.username or self.username
        self.site_name = args.site_name or self.site_name or ""
        self.server_url = args.server or self.server_url or "http://localhost"
        self.logging_level = args.logging_level or self.logging_level
        self.password_file = args.password_file
        self.token_name = args.token_name or self.token_name
        self.token = args.token or self.token

        self.no_prompt = args.no_prompt or self.no_prompt
        self.certificate = args.certificate or self.certificate
        self.no_certcheck = args.no_certcheck or self.no_certcheck
        self.no_proxy = args.no_proxy or self.no_proxy
        self.proxy = args.proxy or self.proxy
        self.timeout = args.timeout or self.timeout

    @staticmethod
    def _read_password_from_file(filename):
        with open(str(filename), "r") as file_contents:
            return file_contents

    def _allow_prompt(self):
        try:
            return not self.no_prompt
        except Exception:
            return True

    def _create_new_username_credential(self, password):
        if password is None:
            if self.password_file:
                password = Session._read_password_from_file(self.password_file)
            elif self._allow_prompt():
                password = getpass.getpass("Password:")
            else:
                Errors.exit_with_error(self.logger, "No password entered")

        if self.username and password:
            credentials = TSC.TableauAuth(self.username, password, site_id=self.site_name)
            self.last_login_using = "username"
            return credentials
        else:
            Errors.exit_with_error(self.logger, "Couldn't find username")

    def _create_new_token_credential(self):
        if self.token:
            token = self.token
        elif self.password_file:
            token = Session._read_password_from_file(self.password_file)
        elif self._allow_prompt():
            token = getpass.getpass("Token:")
        else:
            Errors.exit_with_error(self.logger, "No token value entered")

        if self.token_name and token:
            credentials = TSC.PersonalAccessTokenAuth(self.token_name, token, site_id=self.site_name)
            self.last_login_using = "token"
            return credentials
        else:
            Errors.exit_with_error(self.logger, "Couldn't find token name")

    def _set_connection_options(self):
        # args to handle here: proxy, --no-proxy, cert, --no-certcheck, timeout
        tableau_server = TSC.Server(self.server_url, use_server_version=False)
        if self.no_certcheck:
            tableau_server.add_http_options({"verify": False})
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        tableau_server.use_server_version()  # this will attempt to contact the server
        return tableau_server

    def _create_new_connection(self):
        self.logger.info("===== Creating new session")
        self.tableau_server = self._set_connection_options()
        self._print_server_info()
        self.logger.info("===== Connecting to the server...")

    def _read_existing_state(self):
        if self._check_json():
            self._read_from_json()

    def _print_server_info(self):
        self.logger.info("=====   Server: {}".format(self.server_url))
        if self.username:
            self.logger.info("=====   Username: {}".format(self.username))
        else:
            self.logger.info("=====   Token Name: {}".format(self.token_name))
        self.logger.info("=====   Site: {}".format(self.site_name))

    def _validate_existing_signin(self):
        self.logger.info("===== Continuing previous session")
        self.tableau_server = self._set_connection_options()
        try:
            if self.tableau_server and self.tableau_server.is_signed_in():
                response = self.tableau_server.users.get_by_id(self.user_id)
                self.logger.debug(response)
                if response.status_code.startswith("200"):
                    return self.tableau_server
        except TSC.ServerResponseError as e:
            self.logger.info("Invalid session token", e)
        except Exception as e:
            self.logger.info("Error contacting the server", e)
        return None

    def _sign_in(self, tableau_auth):
        self.logger.debug("Signing in to {0}{1} as {2}".format(self.server_url, self.site_name, self.username))
        try:
            self.tableau_server.auth.sign_in(tableau_auth)  # it's the same call for token or user-pass
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(self.logger, "Error signing in", e)
        try:
            self.site_id = self.tableau_server.site_id
            self.user_id = self.tableau_server.user_id
            self.auth_token = self.tableau_server._auth_token
            if not self.username:
                self.username = self.tableau_server.users.get_by_id(self.user_id).name
            self.logger.debug("Signed into {0}{1} as {2}".format(self.server_url, self.site_name, self.username))
            self.logger.info("=========Succeeded========")
        except TSC.ServerResponseError as e:
            Errors.exit_with_error(self.logger, "Server response", e)

        return self.tableau_server

    def _get_saved_credentials(self):
        if self.last_login_using == "username":
            credentials = self._create_new_username_credential(None)
        elif self.last_login_using == "token":
            credentials = self._create_new_token_credential()
        else:
            return None
        if credentials:
            self.logger.info("===== Using saved credentials")
        return credentials

    # external entry point:
    def create_session(self, args):
        signed_in_object = None
        # pull out cached info from json, then overwrite with new args if available
        self._read_existing_state()
        self._update_session_data(args)
        self.logging_level = args.logging_level or self.logging_level

        credentials = None
        if args.password or args.password_file:
            self._end_session()
            # we don't save the password anywhere, so we pass it along directly
            credentials = self._create_new_username_credential(args.password)
        elif args.token:
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
            self._create_new_connection()
            signed_in_object = self._sign_in(credentials)

        if not signed_in_object:
            Errors.exit_with_error(
                self.logger, "Unable to find or create a session. Please check credentials and login again."
            )
        if args.no_cookie:
            self._remove_json()
        else:
            self._save_session_to_json()
        return signed_in_object

    def end_session_and_clear_data(self):
        self._end_session()
        self.logger.info("===== Signed out")
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
        self.token = None
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
                self.token = auth["personal_access_token"]
                self.last_login_using = auth["last_login_using"]
                self.password_file = auth["password_file"]
                self.no_prompt = auth["no_prompt"]
                self.no_certcheck = auth["no_certcheck"]
                self.certificate = auth["certificate"]
                self.no_proxy = auth["no_proxy"]
                self.proxy = auth["proxy"]
                self.timeout = auth["timeout"]
        except KeyError as e:
            self.logger.debug("Error reading values from stored json file: ", e)
            self._remove_json()
        except Exception as any_error:
            self.logger.info("Error loading session from file: clearing saved values")
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
                "personal_access_token": self.token,
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
