from ..commands import Commands
from .. import Constants
from .user_command import UserCommand
from .. import CreateUserParser
import tableauserverclient as TSC
from .. import log
from ... import Session


class CreateUserCommand(UserCommand):
    def __init__(self, csv_lines, args):
        super().__init__(csv_lines, args)
        self.args = args
        self.logger = log('pythontabcmd2.create_users_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        csv_lines, args = CreateUserParser.create_user_parser()
        return cls(csv_lines, args)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.create_user(server_object, self.csv_lines)

    def create_user(self, server_object, csv_lines):
        self.create_user_command(csv_lines, server_object)

    def create_user_command(self, csv_lines, server_object):
        number_of_users_added = 0
        command = Commands(self.args)
        user_obj_list = command.get_user(csv_lines)
        self.logger.info("======== 0% complete ========")
        for user_obj in user_obj_list:
            username = user_obj.username
            site_role = user_obj.site_role
            password = user_obj.password
            try:
                new_user = TSC.UserItem(username, site_role)
                new_user_added = server_object.users.add(new_user)
                server_object.users.update(new_user_added, password)
                number_of_users_added += 1
            except TSC.ServerResponseError as e:
                if e.code == Constants.forbidden:
                    self.logger.error("User is not local, and the user's "
                                      "credentials are not maintained on"
                                      " Tableau Server.")
                if e.code == Constants.invalid_credentials:
                    self.logger.error("Unauthorized access, Please login")
                if e.code == Constants.user_already_member_of_site:
                    self.logger.error("User: {} already member of "
                                      "site".format(username))
        self.logger.info("======== 100% complete ========")
        self.logger.info("======== Number of users added: {} =========".
                         format(number_of_users_added))
