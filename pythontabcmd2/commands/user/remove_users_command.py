from commands.user.user_command import UserCommand

try:
    from tabcmd2.pythontabcmd2 import tableauserverclient as TSC
    from logger_config import get_logger
except:
    import tableauserverclient as TSC
    from logger_config import get_logger
logger = get_logger('pythontabcmd2.remove_user_command')


class RemoveUserCommand(UserCommand):
    def remove_users(self, server_object, csv_lines, group_name):
        self.evaluate_csv_lines_call_remove_user_command(server_object, csv_lines, group_name)

    def evaluate_csv_lines_call_remove_user_command(self, server, csv_lines, group_name):
        """Method to remove users using Tableauserverclient methods"""
        for line in csv_lines:
            split_line = line.split(',')
            username = split_line[0].lower()
            user_id = UserCommand.find_user_id(server, username)
            group = UserCommand.find_group(server, group_name)
            try:
                server.groups.remove_user(group, user_id)
                logger.info("Successfully removed")
            except TSC.ServerResponseError as e:
                logger.info("Error: Server error occurred", e)    #TODO Map Error code



    def evaluate_csv_lines(self):
        pass