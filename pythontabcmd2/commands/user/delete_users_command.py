from ..commands import Commands
from .. import Constants
from .user_command import UserCommand
from .. import DeleteUserParser
import tableauserverclient as TSC
from .. import log


class DeleteUserCommand(UserCommand):
    def __init__(self, csv_lines, args):
        super().__init__(args, csv_lines)
        self.args = args
        self.logger = log('pythontabcmd2.delete_users_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        csv_lines, args = DeleteUserParser.delete_user_parser()
        return cls(csv_lines, args)

    def run_command(self):
        signed_in_object, server_object = Commands.deserialize()
        self.delete_users(server_object, self.csv_lines)

    def delete_users(self, server_object, csv_lines):
        self.delete_user_command(server_object, csv_lines)

    def delete_user_command(self, server, csv_lines):
        """Method to delete users using Tableauserverclient methods"""
        command = Commands(self.args)
        user_obj_list = command.get_user(csv_lines)
        for user_obj in user_obj_list:
            username = user_obj.username
            user_id = UserCommand.find_user_id(server, username)
            try:
                server.users.remove(user_id)
                self.logger.info("Successfully removed")
            except TSC.ServerResponseError as e:
                self.logger.error("Error: Server error occurred", e)
                # TODO Map Error code
            except ValueError:
                self.logger.error("Error user for ", username, "not found")
