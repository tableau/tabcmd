from ..commands import Commands
from .. import Constants
import tableauserverclient as TSC
from .. import get_logger
import os
import dill as pickle
logger = get_logger('pythontabcmd2.logout', 'info')


class LogoutCommand(Commands):
    def __init__(self):
        pass

    @classmethod
    def parse(cls):
        return cls()

    def run_command(self):
        self.logout()

    def logout(self):
        """ Method to log out from the current session """
        home_path = os.path.expanduser("~")
        file_path = os.path.join(home_path, 'tabcmd.pkl')
        signed_in_object, server_object = Commands.deserialize()
        server_object.auth.sign_out()
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info("Logged out successfully")
        else:
            logger.info("Not logged in")
