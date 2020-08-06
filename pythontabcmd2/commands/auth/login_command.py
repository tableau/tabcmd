from .. import LoginParser
from .. import Constants
import tableauserverclient as TSC
from .. import get_logger
import json
import os
from ..commands import Commands
from .session import Session


class LoginCommand(Commands):
    def __init__(self, args):
        super().__init__(args)
        self.args = args

    def log(self):
        logger = get_logger('pythontabcmd2.session', self.logging_level)
        return logger

    @classmethod
    def parse(cls):
        args = LoginParser.login_parser()
        return cls(args)

    def run_command(self):
        self.create_session()

    def create_session(self):
        """ Method to authenticate user and establish connection """
        logger = self.log()
        session = Session(self.args)
        if self.args.cookie:
            if self.args.token_name and self.args.token:
                session.personal_access_token_authentication_with_token_save()
            elif self.args.username and self.args.password:
                session.username_password_authentication_with_token_save()
            elif self.args.site:
                pass
            # update json and create session with saving token
            elif self.args.server:
                pass
            # update json and create session with saving token
        elif self.args.no_cookie:
            if self.args.token_name:
                session.no_cookie_save_session_creation_with_token()
                logger.info("========Established Connection========")
            elif self.args.username:
                session.no_cookie_save_session_creation_with_username()
                logger.info("========Established Connection========")
        else:
            if self.args.token_name:
                session.personal_access_token_authentication_with_token_save()
            elif self.args.username:
                session.username_password_authentication_with_token_save()




    def update_json_file(self):
        pass
