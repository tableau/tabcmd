import tableauserverclient as TSC

from tabcmd.commands.auth.session import Session
from tabcmd.commands.commands import Commands
from tabcmd.execution.logger_config import log
from .group_command import GroupCommand


class DeleteGroupCommand(GroupCommand):
    """
    This command deletes the specified group from the server
    """

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        server = session.create_session(args)
        try:
            group_id = GroupCommand.find_group_id(server, args.name)
            server.groups.delete(group_id)
            logger.info("Successfully deleted group")
        except TSC.ServerResponseError as e:
            Commands.exit_with_error(logger, "Server Error:", e)
