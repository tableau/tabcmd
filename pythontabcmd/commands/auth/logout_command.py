
from .. import Constants
import tableauserverclient as TSC
from .. import log
import os
from .. import LogoutParser
from ... import Session


class LogoutCommand:
    """
    Command to Log user out of the server
    """
    def __init__(self, args):
        self.args = args
        self.logging_level = args.logging_level
        self.logger = log('pythontabcmd.logout_command', self.logging_level)

    @classmethod
    def parse(cls):
        args = LogoutParser.logout_parser()
        return cls(args)

    def run_command(self):
        self.logout()

    def logout(self):
        """ Method to log out from the current session """
        home_path = os.path.expanduser("~")
        file_path = os.path.join(home_path, 'tableau_auth.json')
        session = Session()
        server_object = session.create_session(self.args)
        server_object.auth.sign_out()
        if os.path.exists(file_path):
            os.remove(file_path)
            self.logger.info("Logged out successfully")
        else:
            self.logger.info("Not logged in")
