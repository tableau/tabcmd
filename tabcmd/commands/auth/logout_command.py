from tabcmd.commands.auth.session import Session
from tabcmd.commands.server import Server
from tabcmd.execution.logger_config import log


class LogoutCommand(Server):
    """
    Command to Log user out of the server
    """

    name: str = "logout"
    description: str = "Sign out from the server"

    @staticmethod
    def define_args(parser):
        # has no options
        pass

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.debug("======================= Launching command =======================")
        session = Session()
        session.end_session_and_clear_data()
