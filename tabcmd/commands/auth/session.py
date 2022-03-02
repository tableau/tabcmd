import getpass
from tabcmd.commands.constants import Constants
import tableauserverclient as TSC
from tabcmd.execution.logger_config import log
import json
import os
from ..commands import Commands
from urllib3.exceptions import InsecureRequestWarning
import requests


class Session:
    """
    Session class handles all authentication related work
    """

    def __init__(self):
        self.username = None
        self._password = None  # underscore naming is a reminder that we don't save this
        self.user_id = None
        self.auth_token = None
        self.token_name = None
        self.token = None
        self.site = None  # The site name, or 'alpodev'
        self.site_id = None  # The site id, or 'abcd-1234-1234-1244-1234'
        self.server = None
        self.last_login_using = None
        self.logging_level = "info"
        self.logger = log(__name__, self.logging_level)
        self._read_from_json()

    # called before we connect to the server
    # generally, we don't want to overwrite stored data with nulls
    # exception: if a username/token name was given, clear the associated password or token
    def _update_session_data(self, args):
        self.username = args.username or self.username
        if args.username:
            self._password = None
        self.site = args.site or self.site or ""
        self.server = args.server or self.server or "http://localhost"
        self.logging_level = args.logging_level or self.logging_level
        self.token_name = args.token_name or self.token_name
        if args.token_name:
            self.token = None
        self.token = args.token or self.token

    @staticmethod
    def _allow_prompt(args):
        try:
            return not args.no_prompt
        except Exception:
            return True

    def _create_new_username_credential(self, args):
        self._update_session_data(args)
        if args.password is None:
            # TODO: implement passwordfile here
            if self._allow_prompt(args):
                args.password = getpass.getpass("Password:")
            else:
                self.logger.debug("No password entered")
                raise SystemExit("No password entered")

        if self.username and args.password:
            credentials = TSC.TableauAuth(self.username, args.password, site_id=self.site)
            self.last_login_using = "username"
            return credentials
        else:
            self.logger.debug("Couldn't find username")
            raise SystemExit("Couldn't find username")

    def _create_new_token_credential(self, args):
        self._update_session_data(args)
        if self.token is None:
            if self._allow_prompt(args):
                self.token = getpass.getpass("Token:")
            else:
                raise SystemExit("No token value entered")
        if self.token_name and self.token:
            credentials = TSC.PersonalAccessTokenAuth(self.token_name, self.token, site_id=self.site)
            self.last_login_using = "token"
            return credentials
        else:
            self.logger.debug("Couldn't find token name")
            raise SystemExit("Couldn't find token name")

    @staticmethod
    def _set_connection_options(server, args):
        # args to handle here: proxy, --no-proxy, cert, --no-certcheck, timeout
        tableau_server = TSC.Server(server)
        if args.no_certcheck:
            tableau_server.add_http_options({"verify": False})
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        tableau_server.use_server_version()  # this will attempt to contact the server
        return tableau_server

    def _print_server_info(self):
        self.logger.info("=====   Server: {}".format(self.server))
        if self.username:
            self.logger.info("=====   Username: {}".format(self.username))
        else:
            self.logger.info("=====   Token Name: {}".format(self.token_name))
        self.logger.info("=====   Site: {}".format(self.site))

    def _validate_existing_signin(self, args):
        self.logger.info("===== Continuing previous session")
        tableau_server = Session._set_connection_options(self.server, args)
        self._print_server_info()
        try:
            tableau_server._set_auth(self.site_id, self.user_id, self.auth_token)
            if tableau_server.is_signed_in():
                return tableau_server
        except TSC.ServerResponseError as e:
            self.logger.info("===== Abandoning invalid session")
            self.logger.debug("Invalid session token: ", e)
            Commands.exit_with_error(self.logger, e)
        except Exception as e:
            self.logger.info("===== Abandoning invalid server connection:")
            self.logger.debug("Error contacting the server: {}".format(e))
            Commands.exit_with_error(self.logger, e)
        self.auth_token = None
        return None

    def _sign_in(self, tableau_auth, args):
        self.logger.info("===== Creating new session")
        tableau_server = Session._set_connection_options(self.server, args)
        self._print_server_info()  # do we even have all of this? well, we must
        tableau_server.use_server_version()
        self.logger.info("===== Connecting to the server...")
        try:
            tableau_server.auth.sign_in(tableau_auth)  # it's the same call for token or user-pass
            self.auth_token = tableau_server.auth_token
            self.site_id = tableau_server.site_id
            self.user_id = tableau_server.user_id
            # TODO: get username and save to self.username, if we used token credentials?
            self.logger.debug("Signed into {0}{1} as {2}".format(self.server, self.site, self.user_id))
            self.logger.info("=========Succeeded========")
        except TSC.ServerResponseError as e:
            self.logger.debug("Server error occurred", e)
            Commands.exit_with_error(self.logger, e)
        return tableau_server

    # external entry point:
    def create_session(self, args):
        signed_in_object = None
        self.logging_level = args.logging_level or self.logging_level
        if self._check_json():
            self._read_from_json()

        # if the user passed in new username/token-name, we use those and scrap anything saved
        credentials = None
        if args.username:
            self.auth_token = None
            self._password = None
            credentials = self._create_new_username_credential(args)
        elif args.token_name:
            self.auth_token = None
            self.token = None
            credentials = self._create_new_token_credential(args)
        else:  # no login arguments given - look for saved info
            # maybe we're already signed in!
            if self.auth_token:
                signed_in_object = self._validate_existing_signin(args)
            if not signed_in_object:
                # nope: get saved credentials if available, we will try to start a new session with them
                if self._last_logged_in_by_username():
                    credentials = self._create_new_username_credential(args)
                elif self._last_logged_in_by_token():
                    credentials = self._create_new_token_credential(args)

                if credentials:
                    self.logger.info("=====Using saved credentials")

        if credentials and not signed_in_object:  # logging in, not using an existing session
            signed_in_object = self._sign_in(credentials, args)
        if not signed_in_object:
            Commands.exit_with_error(
                self.logger,
                "Unable to find or create a session. Please check credentials and login again.",
            )

        if args.no_cookie:
            self._remove_json()
        else:
            self._save_token_to_json_file()
        return signed_in_object

    # delete all saved info
    def end_session_and_clear_data(self):
        self._remove_json()
        self.username = None
        self.user_id = None
        self.auth_token = None
        self.token_name = None
        self.token = None
        self.site = None
        self.site_id = None
        self.server = None
        self.last_login_using = None

    def _last_logged_in_by_username(self):
        return self.last_login_using == "username"

    def _last_logged_in_by_token(self):
        return self.last_login_using == "token"

    # json file functions ----------------------------------------------------
    def _get_file_path(self):
        home_path = os.path.expanduser("~")
        file_path = os.path.join(home_path, "tableau_auth.json")
        return file_path

    def _read_from_json(self):
        if not self._check_json():
            return
        file_path = self._get_file_path()
        with open(str(file_path), "r") as file_contents:
            data = json.load(file_contents)
            for auth in data["tableau_auth"]:
                self.auth_token = auth["token"]
                self.server = auth["server"]
                self.site = auth["site_name"]
                self.site_id = auth["site_id"]
                self.username = auth["username"]
                self.user_id = auth["user_id"]
                self.token_name = auth["personal_access_token_name"]
                self.token = auth["personal_access_token"]
                self.last_login_using = auth["last_login_using"]

    def _check_json(self):
        home_path = os.path.expanduser("~")
        file_path = os.path.join(home_path, "tableau_auth.json")
        return os.path.exists(file_path)

    def _save_token_to_json_file(self):
        data = {}
        data["tableau_auth"] = []
        data["tableau_auth"].append(
            {
                "token": self.auth_token,
                "server": self.server,
                "username": self.username,
                "user_id": self.user_id,
                "site_name": self.site,
                "site_id": self.site_id,
                "personal_access_token_name": self.token_name,
                "personal_access_token": self.token,
                "last_login_using": self.last_login_using,
            }
        )
        file_path = self._get_file_path()
        with open(str(file_path), "w") as f:
            json.dump(data, f)

    def _remove_json(self):
        file_path = self._get_file_path()
        if os.path.exists(file_path):
            os.remove(file_path)
