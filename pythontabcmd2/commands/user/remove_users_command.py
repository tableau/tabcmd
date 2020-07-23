from commands.commands import Commands
from commands.user.user_command import UserCommand
from parsers.remove_users_parser import RemoveUserParser

try:
    from tabcmd2.pythontabcmd2 import tableauserverclient as TSC
    from logger_config import get_logger
except:
    import tableauserverclient as TSC
    from logger_config import get_logger
logger = get_logger('pythontabcmd2.remove_user_command')


class RemoveUserCommand(UserCommand):
    def __init__(self, args, csv_lines):
        super().__init__(csv_lines)
        self.group = args.group

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
                logger.info("Error: Server error occurred", e)    #TODO Map Error code

