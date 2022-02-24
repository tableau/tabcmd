from ..commands import Commands
from .group_command import GroupCommand
from tabcmd.parsers.create_group_parser import CreateGroupParser
import tableauserverclient as TSC
from tabcmd.execution.logger_config import log
from ..auth.session import Session


class CreateGroupCommand(GroupCommand):
    """
    This command is used to create a group
    """

    @classmethod
    def parse(cls):
        args = CreateGroupParser.create_group_parser()
        return args

    @staticmethod
    def run_command(args):
        logger = log(__name__, args.logging_level)
        logger.debug("Launching command")
        session = Session()
        server = session.create_session(args)
        """Method to create group using Tableauserverclient methods"""
        try:
            logger.info("Creating group '{}' on the server...".format(args.name))
            new_group = TSC.GroupItem(args.name)
            server.groups.create(new_group)
            logger.info("Succeeded")
        except TSC.ServerResponseError as e:
            logger.debug(e)
            Commands.exit_with_error(logger, "Error while communicating with the server")
