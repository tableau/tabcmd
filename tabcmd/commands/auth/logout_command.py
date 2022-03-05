from tabcmd.commands.commands import Commands
from tabcmd.commands.auth.session import Session
from tabcmd.execution.logger_config import log


class LogoutCommand(Commands):
    """
    Command to Log user out of the server
    """

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        session.end_session_and_clear_data()
        logger.info("===== Signed out")
