from ..commands import Commands
from .. import Constants
from .user_command import UserCommand
from .. import RemoveUserParser
import tableauserverclient as TSC
from .. import get_logger

#logger = get_logger('pythontabcmd2.remove_user_command')


class RemoveUserCommand(UserCommand):
    def __init__(self, args, csv_lines):
        super().__init__(csv_lines)
        self.group = args.group
        self.logging_level = args.logging_level

    def log(self):
        logger = get_logger('pythontabcmd2.remove_user_command', self.logging_level)
        return logger

    @classmethod
    def parse(cls):
        csv_lines, args = RemoveUserParser.remove_user_parser()
        return cls(args, csv_lines)

    def run_command(self):
        signed_in_object, server_object = Commands.deserialize()
        self.remove_users(server_object, self.csv_lines, self.group)

    def remove_users(self, server_object, csv_lines, group_name):
        self.remove_user_command(server_object, csv_lines, group_name)

    def remove_user_command(self, server, csv_lines, group_name):
        """Method to remove users using Tableauserverclient methods"""
        logger = self.log()
        command = Commands()
        user_obj_list = command.get_user(csv_lines)
        for user_obj in user_obj_list:
            username = user_obj.username
            user_id = UserCommand.find_user_id(server, username)
            group = UserCommand.find_group(server, group_name)
            try:
                server.groups.remove_user(group, user_id)
                logger.info("Successfully removed")
            except TSC.ServerResponseError as e:
                logger.error("Error: Server error occurred", e)
                # TODO Map Error code
