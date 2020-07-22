from commands.user.user_command import UserCommand

try:
    from tabcmd2.pythontabcmd2 import tableauserverclient as TSC
    from logger_config import get_logger
except:
    import tableauserverclient as TSC
    from logger_config import get_logger
logger = get_logger('pythontabcmd2.delete_user_command')


class DeleteUserCommand(UserCommand):
    def delete_users(self, server_object, csv_lines):
        self.evaluate_csv_lines_call_delete_user_command(server_object, csv_lines)

    def evaluate_csv_lines_call_delete_user_command(self, server, csv_lines):
        """Method to delete users using Tableauserverclient methods"""
        for line in csv_lines:  # TODO: BREAK THIS FUNCTION INTO TWO
            split_line = line.split(',')
            username = split_line[0].lower()
            user_id = UserCommand.find_user_id(server, username)
            try:
                server.users.remove(user_id)
                logger.info("Successfully removed")
            except TSC.ServerResponseError as e:
                logger.info("Error: Server error occurred", e)  # TODO Map Error code
            except ValueError:
                logger.info("Error user for ", username, "not found")


