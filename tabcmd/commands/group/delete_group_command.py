from ..commands import Commands
from .group_command import GroupCommand
from .. import DeleteGroupParser
import tableauserverclient as TSC
from .. import log
from ... import Session


class DeleteGroupCommand(GroupCommand):
    """
    This command deletes the specified group from the server
    """
    @classmethod
    def parse(cls):
        args = DeleteGroupParser.delete_group_parser()
        return cls(args)

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        server = session.create_session(args)
        try:
            group_id = GroupCommand.find_group_id(server, args.group_name)
            server.groups.delete(group_id)
            logger.info("Successfully deleted group")
        except TSC.ServerResponseError as e:
            Commands.exit_with_error(logger, "Server Error:", e)
