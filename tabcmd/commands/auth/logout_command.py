from tabcmd.commands.auth.session import Session
from tabcmd.commands.server import Server
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log


class LogoutCommand(Server):
    """
    Command to Log user out of the server
    """

    name: str = "logout"
    description: str = _("logout.short_description")

    @staticmethod
    def define_args(parser):
        # has no options
        pass

    @classmethod
    def run_command(cls, args):
        logger = log(cls.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        session.end_session_and_clear_data()
