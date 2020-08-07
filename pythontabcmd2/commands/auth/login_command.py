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
        session = Session()
        if self.args.username or self.args.site or self.args.password or \
                self.args.server:
            session.update_session(self.args)
            session.check_for_missing_arguments()
            signed_in_object \
                = session.no_cookie_save_session_creation_with_username()
        # print("this is from seesion", session.__dict__)
        else:
            signed_in_object = session.reuse_session()
        if self.args.no_cookie:
            home_path = os.path.expanduser("~")
            file_path = os.path.join(home_path, 'tableau_auth.json')
            if os.path.exists(file_path):
                os.remove(file_path)
        else:
            session.save_token_to_json_file()
        return signed_in_object
