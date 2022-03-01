from tabcmd.commands.commands import Commands
from tabcmd.execution.logger_config import log
from .session import Session


class LoginCommand(Commands):
    """
    Logs in a Tableau Server user.
    """

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        session.create_session(args)
