from ..commands import Commands
from .. import Constants
from .user_command import UserCommand
from .. import RemoveUserParser
import tableauserverclient as TSC
from .. import log
from ... import Session


class RemoveUserCommand(UserCommand):
    """
     Command to remove users from the specified group
    """
    def __init__(self, args, csv_lines, group_name):
        super().__init__(args, csv_lines)
        self.args = args
        self.group = group_name
        self.logger = log('tabcmd.remove_users_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        csv_lines, args, group_name = RemoveUserParser.remove_user_parser()
        return cls(args, csv_lines, group_name)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.remove_users(server_object, self.csv_lines, self.group)

    def remove_users(self, server_object, csv_lines, group_name):
        self.remove_user_command(server_object, csv_lines, group_name)

    def remove_user_command(self, server, csv_lines, group_name):
        """Method to remove users using Tableauserverclient methods"""
        command = Commands(self.args)
        user_obj_list = command.get_user(csv_lines)
        for user_obj in user_obj_list:
            username = user_obj.username
            user_id = UserCommand.find_user_id(server, username)
            group = UserCommand.find_group(server, group_name)
            try:
                server.groups.remove_user(group, user_id)
                self.logger.info("Successfully removed")
            except TSC.ServerResponseError as e:
                self.logger.error("Error: Server error occurred", e)
                # TODO Map Error code

