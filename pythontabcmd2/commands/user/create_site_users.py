from ..commands import Commands
from .. import Constants
from .user_command import UserCommand
from .. import CreateSiteUsersParser
import tableauserverclient as TSC
from .. import get_logger
#logger = get_logger('pythontabcmd2.create_site_users_command')


class CreateSiteUsersCommand(UserCommand):
    def __init__(self, csv_lines, args):
        super().__init__(csv_lines)
        self.role = args.role

    def log(self):
        logger = get_logger('pythontabcmd2.create_site_users_command',
                            self.logging_level)
        return logger

    @classmethod
    def parse(cls):
        csv_lines, role = CreateSiteUsersParser.create_site_user_parser()
        return cls(csv_lines, role)

    def run_command(self):
        server_object = Commands.deserialize()
        self.create_user(server_object, self.csv_lines, self.role)

    def create_user(self, server_object, csv_lines, role):
        self.create_user_command(csv_lines, server_object, role)

    def create_user_command(self, csv_lines, server_object, role):
        logger = self.log()
        command = Commands()
        user_obj_list = command.get_user(csv_lines)
        for user_obj in user_obj_list:
            username = user_obj.username
            site_role = role
            password = user_obj.password
            try:
                new_user = TSC.UserItem(username, role)
                new_user_added = server_object.users.add(new_user)
                logger.info("Successfully created user")
            except TSC.ServerResponseError as e:
                if e.code == Constants.forbidden:
                    logger.error("User is not local, and the user's "
                                "credentials are not maintained on "
                                "Tableau Server.")
                if e.code == Constants.invalid_credentials:
                    logger.error("Unauthorized access, Please login")
                if e.code == Constants.user_already_member_of_site:
                    logger.error("User already member of site")
