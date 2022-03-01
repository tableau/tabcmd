from tabcmd.parsers.login_parser import LoginParser
from tabcmd.execution.logger_config import log
from ..commands import Commands
from .session import Session


class LoginCommand(Commands):
    """
    Logs in a Tableau Server user.
    """

    @classmethod
    def parse(cls):
        args = LoginParser.login_parser()
        return args

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        session.create_session(args)
