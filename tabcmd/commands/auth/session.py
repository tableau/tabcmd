import getpass
import sys
from ... import Constants
import tableauserverclient as TSC
from .. import log
import json
import os


class Session:
    """
    Session class handles all authentication related work
    """

    def __init__(self):
        self.username = None
        self.password = None
        self.auth_token = None
        self.token_name = None
        self.token = None
        self.site = None
        self.site_id = None
        self.server = None
        self.last_login_using = None
        self.logging_level = "info"
        self.logger = log('tabcmd.session', self.logging_level)
        self._read_from_json()

    # called before we connect to the server
    def _update_session_data(self, args):
        if args.username:
            self.username = args.username
        if args.site is None:
            args.site = ''
        self.site = args.site
        if args.password:
            self.password = args.password
        if args.server is None:
            args.server = 'http://localhost'
        self.server = args.server
        if args.logging_level:
            self.logging_level = args.logging_level
        if args.token_name:
            self.token_name = args.token_name
        if args.token:
            self.token = args.token

    def _create_new_username_credential(self, args):
        if self.password is None and args.prompt is True:
            self.password = getpass.getpass("Password:")
        tableau_auth = TSC.TableauAuth(self.username, self.password, self.site)
        self.last_login_using = "username"
        return tableau_auth

    def _create_new_token_credential(self, args):
        if self.token is None and args.prompt is True:
            self.token = getpass.getpass("Token:")
        tableau_auth = TSC.PersonalAccessTokenAuth(self.token_name, self.token, self.site)
        self.last_login_using = "token"
        return tableau_auth

    def _begin_session_or_fail(self, args, tableau_auth):
        try:
            tableau_server = self._create_server_connection(args)
            tableau_server.auth.sign_in(tableau_auth)  # it's actually the same call for token or user-pass
            self.auth_token = tableau_server.auth_token
            self.site_id = tableau_server.site_id
            self.logger.info("=========Succeeded========")
        except TSC.ServerResponseError as e:
            if e.code == Constants.login_error:
<<<<<<< HEAD
                self.logger.error("Please check "
                                  "credentials and login again")
                sys.exit()

    def reuse_session(self):
        try:
            tableau_server = TSC.Server(self.server,
                                        use_server_version=True)
            tableau_server._auth_token = self.auth_token
            tableau_server._site_id = self.site_id
            return tableau_server
        except TSC.ServerResponseError as e:
            if e.code == Constants.login_error:
                self.logger.error("Cannot create a session, Please try "
                                  "again with updated credentials")
                sys.exit()
=======
                self.logger.error("Please check login credentials and try again.", e)
                sys.exit(1)
        return tableau_server

    def _create_server_connection(self, args):
        self._print_server_info()
        # args to handle here: proxy, --no-proxy, cert, --no-certcheck, timeout
        tableau_server = TSC.Server(self.server)
        if args.no_certcheck:
            tableau_server.add_http_options({'verify': False})
        tableau_server.use_server_version()  # this will attempt to contact the server
        return tableau_server
>>>>>>> development

    def _print_server_info(self):

        self.logger.info("===== Creating new session")
        self.logger.info("===== Server: {}".format(self.server))
        if self.username:
            self.logger.info("===== Username: {}".format(self.username))
        else:
            self.logger.info("===== Token Name: {}".format(self.token_name))
        self.logger.info("===== Site: {}".format(self.site))
        self.logger.info("===== Connecting to the server...")

    def _reuse_session(self, args):
        try:
<<<<<<< HEAD
            if self.token is None:
                self.token = getpass.getpass("Token:")
            self.check_for_missing_arguments()
            tableau_auth = \
                TSC.PersonalAccessTokenAuth(self.token_name,
                                            self.token, self.site)
            tableau_server = \
                TSC.Server(self.server, use_server_version=True)
            signed_in_object = \
                tableau_server.auth.sign_in_with_personal_access_token(
                    tableau_auth)
            self.auth_token = tableau_server.auth_token
            self.site_id = tableau_server.site_id
            self.last_login_using = "token"
            self.logger.info("=========Succeeded========")
            return tableau_server
        except TSC.ServerResponseError as e:
            if e.code == Constants.login_error:
                self.logger.error("Please check login "
                                  "credentials")
                sys.exit()

    def create_session(self, args):
        try:
            signed_in_object = None
            if args.username or args.password:
                signed_in_object = self.create_new_session_using_username(args)
            elif args.token or args.token_name:
                signed_in_object = self.create_new_session_using_token(args)
            elif args.site or args.server:
                last_login_username_present, last_login_token_name_present, \
                    username, token_name = \
                    self.check_last_login_username_token_name()
                if last_login_username_present:
                    signed_in_object = \
                        self.create_new_session_using_username(args)
                elif last_login_token_name_present:
                    signed_in_object = \
                        self.create_new_session_using_token(args)
            else:
                self.logger.info("==========Continuing previous "
                                 "session========")
                signed_in_object = self.reuse_session()
            if args.no_cookie:
                self.remove_json()
            else:
                self.save_token_to_json_file()
            return signed_in_object
        except (Exception,):
            self.logger.error("Cannot create a session, Please try "
                              "again with updated credentials")
            sys.exit()
=======
            tableau_server = self._create_server_connection(self, args)
        except Exception as e:
            self.logger.debug("Saved session token was invalid or something went wrong connecting to the server:")
            self.logger.debug(e)
            self.auth_token = None
            return None
        tableau_server._auth_token = self.auth_token
        tableau_server._site_id = self.site_id
        # todo check current behavior: show this before or after successful login?
        self.logger.info("===== Continuing previous session")
        return tableau_server

    def create_session(self, args):
        signed_in_object = None
        self._update_session_data(args)
        if args.username:
            credentials = self._create_new_username_credential(args)
        elif args.token_name:
            credentials = self._create_new_token_credential(args)
        elif self._check_json():
            self._read_from_json()
            if self.auth_token:
                signed_in_object = self._reuse_session(args)

            if not signed_in_object:  # reused session may have expired
                last_login_username_present, last_login_token_name_present = self._check_last_login_method()
                if last_login_username_present:
                    credentials = self._create_new_username_credential(args)
                elif last_login_token_name_present:
                    credentials = self._create_new_token_credential(args)
        else:
            self.logger.error("Unable to find or create a session. Please check credentials and login again.")
            sys.exit()

        if credentials and not signed_in_object:
            signed_in_object = self._begin_session_or_fail(args, credentials)
        if args.no_cookie:
            self._remove_json()
        else:
            self._save_token_to_json_file()
        return signed_in_object
>>>>>>> development

    def _check_last_login_username_token_name(self):
        last_login_username_present = False
        last_login_token_name_present = False
        if not self._check_json():
            return
        # TODO can this call read_from_json instead of opening the file itself?
        file_path = self._get_file_path()
        with open(str(file_path), 'r') as input:
            data = json.load(input)
            for auth in data['tableau_auth']:
                if auth['last_login_using'] == "username":
                    last_login_username_present = True
                if auth['last_login_using'] == "token":
                    last_login_token_name_present = True
<<<<<<< HEAD
            return last_login_username_present, \
                last_login_token_name_present, username, token_name

    def create_new_session_using_username(self, args):
        try:
            self.update_session(args)
            signed_in_object \
                = self.no_cookie_save_session_creation_with_username()
            return signed_in_object
        except TSC.ServerResponseError as e:
            self.logger.error("Please check login credentials")
            sys.exit()
=======
            return last_login_username_present, last_login_token_name_present
>>>>>>> development

    # json file functions

    def _get_file_path(self):
        home_path = os.path.expanduser("~")
        file_path = os.path.join(home_path, 'tableau_auth.json')
        return file_path

    def _read_from_json(self):
        if not self._check_json():
            return
        file_path = self._get_file_path()
        with open(str(file_path), 'r') as input:
            data = json.load(input)
            for auth in data['tableau_auth']:
                self.auth_token = auth['token']
                self.server = auth['server']
                self.site = auth['site_name']
                self.site_id = auth['site_id']
                self.username = auth['username']
                self.token_name = auth['personal_access_token_name']
                self.token = auth['personal_access_token']
                self.last_login_using = auth['last_login_using']

    def _check_json(self):
        home_path = os.path.expanduser("~")
        file_path = os.path.join(home_path, 'tableau_auth.json')
        return os.path.exists(file_path)

    def _save_token_to_json_file(self):
        data = {}
        data['tableau_auth'] = []
        data['tableau_auth'].append({
            'token': self.auth_token,
            'server': self.server,
            'username': self.username,
            'site_name': self.site,
            'site_id': self.site_id,
            'personal_access_token_name': self.token_name,
            'personal_access_token': self.token,
            'last_login_using': self.last_login_using
        })
        file_path = self._get_file_path()
        with open(str(file_path), 'w') as f:
            json.dump(data, f)

    def _remove_json(self):
        file_path = self._get_file_path()
        if os.path.exists(file_path):
            os.remove(file_path)
