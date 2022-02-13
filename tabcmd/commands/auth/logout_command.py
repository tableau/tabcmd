from .. import LogoutParser
from .. import log
import os
from ... import Session


class LogoutCommand:
    """
    Command to Log user out of the server
    """
    @classmethod
    def parse(cls):
        args = LogoutParser.logout_parser()
        return cls(args)


    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        # TODO move this logic into Session class
        home_path = os.path.expanduser("~")
        file_path = os.path.join(home_path, 'tableau_auth.json')
        session = Session()
        server_object = session.create_session(args)
        server_object.auth.sign_out()
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info("Logged out successfully")
        else:
            logger.info("Not logged in")
