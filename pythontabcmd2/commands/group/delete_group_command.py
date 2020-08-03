from ..commands import Commands
from .group_command import GroupCommand
from .. import DeleteGroupParser
import tableauserverclient as TSC
from .. import get_logger
#logger = get_logger('pythontabcmd2.delete_group_command')


class DeleteGroupCommand(GroupCommand):
    def __init__(self, args):
        super().__init__(args)
        self.logging_level = args.logging_level

    @classmethod
    def parse(cls):
        args = DeleteGroupParser.delete_group_parser()
        return cls(args)

    def log(self):
        logger = get_logger('pythontabcmd2.create_project_command',
                            self.logging_level)
        return logger

    def run_command(self):
        signed_in_object, server_object = Commands.deserialize()
        self.delete_group(server_object)

    def delete_group(self, server):
        """Method to delete group using Tableauserverclient methods"""
        logger = self.log()
        try:
            group_id = GroupCommand.find_group_id(server, self.name)
            server.groups.delete(group_id)
            logger.info("Successfully deleted group")
        except TSC.ServerResponseError as e:
            logger.error("Error: Server error occurred", e)

