from ..commands import Commands
from .group_command import GroupCommand
from .. import DeleteGroupParser
import tableauserverclient as TSC
from .. import get_logger


class DeleteGroupCommand(GroupCommand):
    def __init__(self, args):
        super().__init__(args)

    @classmethod
    def parse(cls):
        args = DeleteGroupParser.delete_group_parser()
        return cls(args)

    def log(self):
        logger = get_logger('pythontabcmd2.create_project_command',
                            self.logging_level)
        return logger

    def run_command(self):
        server_object = Commands.deserialize()
        self.delete_group(server_object)

    def delete_group(self, server):
        """Method to delete group using Tableauserverclient methods"""
        logger = self.log()
        try:
            group_id = GroupCommand.find_group_id(server, self.name)
            server.groups.delete(group_id)
            logger.info("Successfully deleted group")
        except TSC.ServerResponseError as e:
            logger.error("Server error occurred", e)

