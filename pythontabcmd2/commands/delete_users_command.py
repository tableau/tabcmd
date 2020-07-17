try:
    from .. import tableauserverclient as TSC
    from .. logger_config import get_logger
except:
    import tableauserverclient as TSC
    from logger_config import get_logger
logger = get_logger('pythontabcmd2.delete_user_command')


class DeleteUserCommand:
    def delete_users(self, server_object, csv_lines):
        self.evaluate_csv_lines_call_delete_user_command(server_object, csv_lines)

    def evaluate_csv_lines_call_delete_user_command(self, server, csv_lines):
        """Method to delete users using Tableauserverclient methods"""
        for line in csv_lines:  # TODO: BREAK THIS FUNCTION INTO TWO
            split_line = line.split(',')
            username = split_line[0].lower()
            user_id = self.find_user_id(server, username)
            try:
                server.users.remove(user_id)
                logger.info("Successfully removed")
            except TSC.ServerResponseError as e:
                logger.info("Error: Server error occurred", e)  # TODO Map Error code
            except ValueError:
                logger.info("Error user for ", username, "not found")

    def find_user_id(self, server, username):  # TODO: Move to separate class
        """ Method to find the group id given group name"""

        all_users, pagination_item = server.users.get()
        all_user_names_ids = [(user.name, user._id) for user in all_users]
        user_id = None
        for user in all_user_names_ids:
            if user[0] == username:
                user_id = user[1]
                break

        return user_id
