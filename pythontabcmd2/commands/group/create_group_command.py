from ..commands import Commands
from .group_command import GroupCommand
from .. import CreateGroupParser
import tableauserverclient as TSC
from .. import get_logger


class CreateGroupCommand(GroupCommand):
    def __init__(self, args):
        super().__init__(args)
        self.logging_level = args.logging_level

    def log(self):
        logger = get_logger('pythontabcmd2.create_group_command',
                            self.logging_level)
        return logger

    @classmethod
    def parse(cls):
        args = CreateGroupParser.create_group_parser()
        return cls(args)

    def run_command(self):
        signed_in_object, server_object = Commands.deserialize()
        self.create_group(server_object)

    def create_group(self, server):
        """Method to create group using Tableauserverclient methods"""
        logger = self.log()
        try:
            new_group = TSC.GroupItem(self.name)
            server.groups.create(new_group)
            logger.info("Successfully created group")
        except TSC.ServerResponseError as e:      # TODO MAP ERROR
            logger.error("Error: Server error occurred: Group already exists")
