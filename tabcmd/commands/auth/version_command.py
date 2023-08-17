from tabcmd.commands.server import Server
from tabcmd.execution.localize import _
from tabcmd.execution.logger_config import log
from tabcmd.version import version


class VersionCommand(Server):

    """
    Command to Log user out of the server
    """

    strings = [
        "Tableau Server Command Line Utility",  # 6 in parent_parser
        "Show version information and exit.",  # 7 in parent_parser
    ]
    name: str = "version"
    description: str = _(strings[1])

    @staticmethod
    def define_args(parser):
        # has no options
        pass

    @staticmethod
    def run_command(args):
        logger = log(__class__.__name__, args.logging_level)
        logger.info(VersionCommand.strings[0] + " v" + version + "\n")
