from ..commands import Commands
from .group_command import GroupCommand
from .. import DeleteGroupParser
import tableauserverclient as TSC
from .. import get_logger
logger = get_logger('pythontabcmd2.delete_group_command')


class DeleteGroupCommand(GroupCommand):
    def __init__(self, args):
        super().__init__(args)

    @classmethod
    def parse(cls):
        args = DeleteGroupParser.delete_group_parser()
        return cls(args)

    def run_command(self):
        signed_in_object, server_object = Commands.deserialize()
        self.delete_group(server_object)

    def delete_group(self, server):
        """Method to delete group using Tableauserverclient methods"""
        try:
            group_id = GroupCommand.find_group_id(server, self.name)
            server.groups.delete(group_id)
            logger.info("Successfully deleted group") 
        except TSC.ServerResponseError as e:
            logger.info("Error: Server error occurred", e)    #TODO Map Error code
# code        except Un:
#             logger.info("Error: Group not found, Please check Group name", e)

