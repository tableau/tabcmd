from tabcmd.commands.server import Server
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log
from .session import Session


class LoginCommand(Server):
    """
    Logs in a Tableau Server user.
    """

    name: str = "login"
    description: str = _("login.short_description")

    @staticmethod
    def define_args(parser):
        # just uses global options
        pass

    @classmethod
    def run_command(cls, args):
        logger = log(cls.__name__, args.logging_level)
        logger.debug(_("tabcmd.launching"))
        session = Session()
        session.create_session(args, logger)
