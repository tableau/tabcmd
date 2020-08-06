from ..commands import Commands
from .. import LoginParser
from .. import Constants
import tableauserverclient as TSC
from .. import get_logger
import json

import os


class Session(Commands):
    def username_password_authentication_with_token_save(self):
        logger = self.log()
        if self.username:
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