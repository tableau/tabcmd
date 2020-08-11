import getpass
import sys
from ..commands import Commands
from .. import LoginParser
from .. import Constants
import tableauserverclient as TSC
from .. import get_logger,log
import json
import os


class Session:
    def __init__(self):
        self.username = None
        self.password = None
        self.auth_token = None
        self.token_name = None
        self.token = None
        self.site = None
        self.site_id = None
        self.server = None
        self.logging_level = "info"
        self.logger = log('pythontabcmd2.session', self.logging_level)
        self.read_from_json()

    def get_file_path(self):
        home_path = os.path.expanduser("~")
        file_path = os.path.join(home_path, 'tableau_auth.json')
        return file_path

    def read_json(self):
        file_path = self.get_file_path()
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

    def read_from_json(self):
        if self.check_json():
            self.read_json()

    def check_json(self):
        home_path = os.path.expanduser("~")
        file_path = os.path.join(home_path, 'tableau_auth.json')
        return os.path.exists(file_path)

    def update_session(self, args):
        if args.username:
            self.username = args.username
        if args.site is not None:
            self.site = args.site
        if args.password:
            self.password = args.password
        if args.server:
            self.server = args.server
        if args.logging_level:
            self.logging_level = args.logging_level
        if args.token_name:
            self.token_name = args.token_name
        if args.token:
            self.token = args.token

    def check_for_missing_arguments(self):
        if self.username and self.password is None:
            self.password = getpass.getpass("Password:")
        if self.password and self.username is None:
            print("Please pass username")
            sys.exit()
        if self.token and self.token_name is None:
            print("Please pass Personal Access Token Name")
            sys.exit()
        if self.token_name and self.token is None:
            self.token = getpass.getpass("Token:")
        if self.server is None:
            print("Please pass server")
            sys.exit()
        if self.site is None:
            print("please pass site")
            sys.exit()

    def save_token_to_json_file(self):
        data = {}
        data['tableau_auth'] = []
        data['tableau_auth'].append({
            'token': self.auth_token,
            'server': self.server,
            'username': self.username,
            'site_name': self.site,
            'site_id': self.site_id,
            'personal_access_token_name': self.token_name,
            'personal_access_token': self.token
        })
        file_path = self.get_file_path()
        with open(str(file_path), 'w') as f:
            json.dump(data, f)


    def no_cookie_save_session_creation_with_username(self):
        try:
            tableau_auth = TSC.TableauAuth(self.username,
                                           self.password, self.site)
            tableau_server = TSC.Server(self.server,
                                        use_server_version=True)
            signed_in_object = tableau_server.auth.sign_in(tableau_auth)
            self.auth_token = tableau_server.auth_token
            self.site_id = tableau_server.site_id
            return tableau_server
        except TSC.ServerResponseError as e:
            if e.code == Constants.login_error:
                self.logger.error(" this is from here Login Error, Please "
                                  "Login again", e)
                sys.exit()

    def reuse_session(self):
        tableau_server = TSC.Server(self.server,
                                    use_server_version=True)
        tableau_server._auth_token = self.auth_token
        tableau_server._site_id = self.site_id
        return tableau_server

    def no_cookie_save_session_creation_with_token(self):
        try:
            tableau_auth = \
                TSC.PersonalAccessTokenAuth(self.token_name,
                                            self.token, self.site)
            tableau_server = \
                TSC.Server(self.server, use_server_version=True)
            signed_in_object = \
                tableau_server.auth.sign_in_with_personal_access_token(
                    tableau_auth)
            return tableau_server
        except TSC.ServerResponseError as e:
            if e.code == Constants.login_error:
                self.logger.error("Login Error, Please Login again")

    def create_session(self, args):
        signed_in_object = None
        if args.username or args.password:
            signed_in_object = self.create_new_session_using_username(args)
        elif args.token or args.token_name:
            signed_in_object = self.create_new_session_using_token(args)
        elif args.site or args.server:
            if self.check_json_for_username():
                signed_in_object = self.create_new_session_using_username(args)
            elif self.check_json_for_token_name():
                signed_in_object = self.create_new_session_using_token(args)
            else:
                print("Please pass complete credentials")
        else:
            signed_in_object = self.reuse_session()
            print("re-using session")
        if args.no_cookie:
            file_path = self.get_file_path()
            if os.path.exists(file_path):
                os.remove(file_path)
        else:
            self.save_token_to_json_file()
        return signed_in_object

    def check_json_for_username(self):
        file_path = self.get_file_path()
        with open(str(file_path), 'r') as input:
            data = json.load(input)
            for auth in data['tableau_auth']:
                if auth['username'] is not None:
                    return True
            return False

    def check_json_for_token_name(self):
        file_path = self.get_file_path()
        with open(str(file_path), 'r') as input:
            data = json.load(input)
            for auth in data['tableau_auth']:
                if auth['personal_access_token_name'] is not None:
                    return True
            return False

    def create_new_session_using_username(self, args):
        self.update_session(args)
        self.check_for_missing_arguments()
        signed_in_object \
            = self.no_cookie_save_session_creation_with_username()
        return signed_in_object

    def create_new_session_using_token(self, args):
        self.update_session(args)
        self.check_for_missing_arguments()
        signed_in_object \
            = self.no_cookie_save_session_creation_with_token()
        return signed_in_object
