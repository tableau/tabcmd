from ..commands import Commands
from .. import Constants
from .user_command import UserCommand
from .. import DeleteUserParser
import tableauserverclient as TSC
from .. import log
from ... import Session


class DeleteUserCommand(UserCommand):
    def __init__(self, csv_lines, args):
        super().__init__(csv_lines, args)
        self.args = args
        self.logger = log('pythontabcmd2.delete_users_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        csv_lines, args = DeleteUserParser.delete_user_parser()
        return cls(csv_lines, args)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.delete_users(server_object, self.csv_lines)

    def delete_users(self, server_object, csv_lines):
        self.delete_user_command(server_object, csv_lines)

    def delete_user_command(self, server, csv_lines):
        """Method to delete users using Tableauserverclient methods"""
        number_of_users_deleted = 0
        command = Commands(self.args)
        user_obj_list = command.get_user(csv_lines)
        self.logger.info("======== 0% complete ========")
        for user_obj in user_obj_list:
            username = user_obj.username
            user_id = UserCommand.find_user_id(server, username)
            number_of_users_deleted += 1
            try:
                server.users.remove(user_id)
                self.logger.info("Successfully removed user: {}".
                                 format(username))
            except TSC.ServerResponseError as e:
                self.logger.error("Error: Server error occurred", e)
                # TODO Map Error code
            except ValueError:
                self.logger.error("Error user for ", username, "not found")
        self.logger.info("======== 100% complete ========")
        self.logger.info("======== Number of users deleted: {} =========".
                         format(number_of_users_deleted))
