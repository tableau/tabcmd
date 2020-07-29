from ..commands import Commands
from .. import Constants
from .user_command import UserCommand
from .. import AddUserParser
import tableauserverclient as TSC
from .. import get_logger
logger = get_logger('pythontabcmd2.add_user_command')


class AddUserCommand(UserCommand):
    def __init__(self, args, csv_lines):
        super().__init__(csv_lines)
        self.group = args.group

    @classmethod
    def parse(cls):
        csv_lines, args = AddUserParser.add_user_parser()
        return cls(args, csv_lines)

    def run_command(self):
        signed_in_object, server_object = Commands.deserialize()
        self.add_users(server_object, self.csv_lines, self.group)

    def add_users(self, server_object, csv_lines, group_name):
        self.add_user_command(server_object, csv_lines, group_name)

    def add_user_command(self, server, csv_lines, group_name):
        """Method to add users to a group using Tableauserverclient methods"""
        command = Commands()
        user_obj_list = command.get_user(csv_lines)
        for user_obj in user_obj_list:
            username = user_obj.username
            user_id = UserCommand.find_user_id(server, username)
            group = UserCommand.find_group(server, group_name)
            try:
                server.groups.add_user(group, user_id)
                logger.info("Successfully added")
            except TSC.ServerResponseError as e:
                logger.info("Error: Server error occurred", e)  # TODO Map Error code

