try:
    from .. import tableauserverclient as TSC
    from .. logger_config import get_logger
except:
    import tableauserverclient as TSC
    from logger_config import get_logger
logger = get_logger('pythontabcmd2.remove_user_command')


class RemoveUserCommand:
    def remove_users(self, server_object, csv_lines, group_name):
        self.evaluate_csv_lines_call_remove_user_command(server_object, csv_lines, group_name)

    def evaluate_csv_lines_call_remove_user_command(self, server, csv_lines, group_name):
        """Method to remove users using Tableauserverclient methods"""
        for line in csv_lines:
            split_line = line.split(',')
            username = split_line[0].lower()
            user_id = self.find_user_id(server, username)
            group = self.find_group(server, group_name)
            try:
                server.groups.remove_user(group, user_id)
                logger.info("Successfully removed")
            except TSC.ServerResponseError as e:
                logger.info("Error: Server error occurred", e)    #TODO Map Error code

    def find_user_id(self, server, user_name):             # TODO: Move to separate class
        """ Method to find the group id given group name"""
        all_users, pagination_item = server.users.get()
        all_user_names_ids = [(user.name, user._id) for user in all_users]
        user_id = None
        for user in all_user_names_ids:
            if user[0] == user_name:
                user_id = user[1]
                break
        return user_id

    def find_group(self, newserver, group_name):  # TODO: Move to separate class
        """ Method to find the group id given group name"""
        all_groups, pagination_item = newserver.groups.get()
        all_group_names = [(group.name, group) for group in all_groups]
        group_item = None
        for group in all_group_names:
            if group[0] == group_name:
                group_item = group[1]
                break
        return group_item

