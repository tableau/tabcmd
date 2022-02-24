import os
from tabcmd.parsers.logout_parser import LogoutParser
from tabcmd.execution.logger_config import log
from ..auth.session import Session


class LogoutCommand:
    """
    Command to Log user out of the server
    """

    @classmethod
    def parse(cls):
        args = LogoutParser.logout_parser()
        return args

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        session.end_session_and_clear_data()
        logger.info("===== Signed out")
