from tabcmd.commands.server import Server
from tabcmd.execution.logger_config import log
from .session import Session


class LoginCommand(Server):
    """
    Logs in a Tableau Server user.
    """

    name: str = "login"
    description: str = "Log in to site"

    @staticmethod
    def define_args(parser):
        # just uses global options
        pass

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        session.create_session(args)
