from ..commands import Commands
from .. import Constants
from .user_command import UserCommand
from .. import CreateSiteUsersParser
import tableauserverclient as TSC
from .. import log
from ... import Session


class CreateSiteUsersCommand(UserCommand):
    def __init__(self, csv_lines, args):
        super().__init__(csv_lines, args)
        self.args = args
        self.role = args.role
        self.logger = log('pythontabcmd2.create_site_users_command',
                          self.logging_level)

    @classmethod
    def parse(cls):
        csv_lines, args = CreateSiteUsersParser.create_site_user_parser()
        return cls(csv_lines, args)

    def run_command(self):
        session = Session()
        server_object = session.create_session(self.args)
        self.create_user(server_object, self.csv_lines, self.role)

    def create_user(self, server_object, csv_lines, role):
        self.create_user_command(csv_lines, server_object, role)

    def create_user_command(self, csv_lines, server_object, role):
        number_of_users_added = 0
        command = Commands(self.args)
        user_obj_list = command.get_user(csv_lines)
        self.logger.info("======== 0% complete ========")
        for user_obj in user_obj_list:
            username = user_obj.username
            site_role = role
            password = user_obj.password
            try:
                new_user = TSC.UserItem(username, role)
                server_object.users.add(new_user)
                self.logger.info("Successfully created user: {}".format(
                    username))
                number_of_users_added += 1
            except TSC.ServerResponseError as e:
                if e.code == Constants.forbidden:
                    self.logger.error("User is not local, and the user's "
                                      "credentials are not maintained on "
                                      "Tableau Server.")
                if e.code == Constants.invalid_credentials:
                    self.logger.error("Unauthorized access, Please login")
                if e.code == Constants.user_already_member_of_site:
                    self.logger.error("User: {} already member of "
                                      "site".format(username))
        self.logger.info("======== 100% complete ========")
        self.logger.info("======== Number of users added: {} =========".
                         format(number_of_users_added))
