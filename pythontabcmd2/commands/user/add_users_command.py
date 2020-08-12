from ..commands import Commands
from .. import Constants
from .user_command import UserCommand
from .. import AddUserParser
import tableauserverclient as TSC
from .. import log
from ... import Session

class AddUserCommand(UserCommand):
    def __init__(self, args, csv_lines):
        super().__init__(args, csv_lines)
        self.args = args
        self.group = args.group
        self.logger = log('pythontabcmd2.add_user_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        csv_lines, args = AddUserParser.add_user_parser()
        return cls(args, csv_lines)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.add_users(server_object, self.csv_lines, self.group)

    def add_users(self, server_object, csv_lines, group_name):
        self.add_user_command(server_object, csv_lines, group_name)

    def add_user_command(self, server, csv_lines, group_name):
        """Method to add users to a group using Tableauserverclient methods"""
        command = Commands(self.args)
        user_obj_list = command.get_user(csv_lines)
        for user_obj in user_obj_list:
            username = user_obj.username
            user_id = UserCommand.find_user_id(server, username)
            group = UserCommand.find_group(server, group_name)
            try:
                server.groups.add_user(group, user_id)
                self.logger.info("Successfully added")
            except TSC.ServerResponseError as e:
                self.logger.error("Error: Server error occurred", e)
                # TODO Map Error code
