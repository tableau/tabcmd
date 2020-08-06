from ..commands import Commands
from .. import LoginParser
from .. import Constants
import tableauserverclient as TSC
from .. import get_logger
import json
import os


class Session(Commands):
    def __init__(self, args):
        super().__init__(args)
        self.args = args

    def username_password_authentication_with_token_save(self):
        logger = self.log()
        try:
            tableau_auth = TSC.TableauAuth(self.username,
                                           self.password, self.site)
            tableau_server = TSC.Server(self.server,
                                        use_server_version=True)
            signed_in_object = tableau_server.auth.sign_in(tableau_auth)
            self.save_token_to_json_file(tableau_server.auth_token,
                                         self.server,
                                         tableau_server.site_id)
            logger.info("======Successfully established connection======")

        except TSC.ServerResponseError as e:
            if e.code == Constants.login_error:
                logger.error("Login Error, Please Login again")

    def personal_access_token_authentication_with_token_save(self):
        logger = self.log()

        try:
            tableau_auth = \
                TSC.PersonalAccessTokenAuth(self.token_name,
                                            self.personal_token, self.site)
            tableau_server = \
                TSC.Server(self.server, use_server_version=True)
            signed_in_object = \
                tableau_server.auth.sign_in_with_personal_access_token(
                    tableau_auth)
            self.save_token_to_json_file(tableau_server.auth_token,
                                         self.server,
                                         tableau_server.site_id)
            logger.info("======Successfully established connection======")

        except TSC.ServerResponseError as e:
            if e.code == Constants.login_error:
                logger.error("Login Error, Please Login again")

    def save_token_to_json_file(self, token, server, site_id):
        data = {}
        data['tableau_auth'] = []
        data['tableau_auth'].append({
            'token': token,
            'server': server,
            'site': site_id,
        })
        home_path = os.path.expanduser("~")
        file_path = os.path.join(home_path, 'tableau_auth.json')
        with open(str(file_path), 'w') as f:
            json.dump(data, f)

    def log(self):
        logger = get_logger('pythontabcmd2.create_project_command',
                            self.logging_level)
        return logger

    def no_cookie_save_session_creation_with_username(self):
        logger = self.log()
        try:
            tableau_auth = TSC.TableauAuth(self.username,
                                           self.password, self.site)
            tableau_server = TSC.Server(self.server,
                                        use_server_version=True)
            signed_in_object = tableau_server.auth.sign_in(tableau_auth)
            return tableau_server.auth_token, tableau_server.site_id
        except TSC.ServerResponseError as e:
            if e.code == Constants.login_error:
                logger.error("Login Error, Please Login again")

    def no_cookie_save_session_creation_with_token(self):
        logger = self.log()
        try:
            tableau_auth = \
                TSC.PersonalAccessTokenAuth(self.token_name,
                                            self.personal_token, self.site)
            tableau_server = \
                TSC.Server(self.server, use_server_version=True)
            signed_in_object = \
                tableau_server.auth.sign_in_with_personal_access_token(
                    tableau_auth)
            return tableau_server.auth_token, tableau_server.site_id
        except TSC.ServerResponseError as e:
            if e.code == Constants.login_error:
                logger.error("Login Error, Please Login again")

    def no_cookie_server_object_creation(self, token, site_id):
        tableau_server = TSC.Server(self.server, use_server_version=True)
        tableau_server._auth_token = token
        tableau_server._site_id = site_id
        return tableau_server
