from ..commands import Commands
import tableauserverclient as TSC


class UserCommand(Commands):
    """
    This class acts as a base class for user related group of commands
    """
    def __init__(self, args, csv_lines):
        super().__init__(args)
        self.csv_lines = csv_lines
        self.args = args

    @staticmethod
    def find_user_id(server, username):
        """ Method to find the user id given username"""
        all_users = list(TSC.Pager(server.users))
        all_user_names_ids = [(user.name, user._id) for user in all_users]
        user_id = None
        for user in all_user_names_ids:
            if user[0] == username:
                user_id = user[1]
                break
        return user_id

    @staticmethod
    def find_group(server, group_name):
        """ Method to find the group id given group name"""
        all_groups, pagination_item = server.groups.get()
        all_group_names = [(group.name, group) for group in all_groups]
        group_item = None
        for group in all_group_names:
            if group[0] == group_name:
                group_item = group[1]
                break
        return group_item
