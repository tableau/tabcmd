from ..commands import Commands
from .group_command import GroupCommand
from tabcmd.parsers.delete_group_parser import DeleteGroupParser
import tableauserverclient as TSC
from tabcmd.execution.logger_config import log
from ..auth.session import Session


class DeleteGroupCommand(GroupCommand):
    """
    This command deletes the specified group from the server
    """

    @classmethod
    def parse(cls):
        args = DeleteGroupParser.delete_group_parser()
        return args

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        server = session.create_session(args)
        try:
            logger.info("Finding group {} on server...".format(args.name))
            group_id = GroupCommand.find_group_id(server, args.name)
            logger.info("Deleting group {} on server...".format(group_id))
            server.groups.delete(group_id)
            logger.info("===== Succeeded")
        except TSC.ServerResponseError as e:
            Commands.exit_with_error(logger, e)
