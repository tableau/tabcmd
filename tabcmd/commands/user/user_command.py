from ..commands import Commands
from .user_data import Userdata

class UserCommand(Commands):
    """
    This class acts as a base class for user related group of commands
    """
    def __init__(self, csv_lines, args):
        super().__init__(args)
        self.csv_lines = csv_lines
        self.args = args

    @staticmethod
    def find_user_id(server, username):
        """ Method to find the user id given user name"""
        all_users, pagination_item = server.users.get()
        all_user_names_ids = [(user.name, user._id) for user in all_users]
        user_id = None
        for user in all_user_names_ids:
            if user[0] == username:
                user_id = user[1]
                break
        return user_id

    @staticmethod
    def get_users_from_file(csv_file):
        user_list = []
        for line in csv_file:
            users_data = UserCommand.get_user_details(line)
            user_list.append(users_data)
        return user_list

    @staticmethod
    def get_user_details(line):
        split_line = line.split(',')
        user_data = Userdata()
        user_data.username = split_line[0].lower()
        user_data.password = split_line[1].lower()
        user_data.full_name = split_line[2].lower()
        user_data.license_level = split_line[3].lower()
        user_data.admin_level = split_line[4].lower()
        user_data.publisher = split_line[5].lower()
        user_data.email = split_line[6].lower()
        user_data.site_role = \
            UserCommand.evaluate_license_level_admin_level(user_data.license_level,
                                                    user_data.admin_level,
                                                    user_data.publisher)
        return user_data

    @staticmethod
    def evaluate_license_level_admin_level(license_level,
                                           admin_level, publisher):
        site_role = None
        if license_level == ('creator' or 'explorer' or 'viewer' or
                             'unlicensed' or '') and (
                admin_level == 'system') and publisher == 'yes':
            site_role = 'SiteAdministrator'
        if license_level == 'creator' and (admin_level == 'site') and \
                publisher == 'yes':
            site_role = 'SiteAdministratorCreator'
        if license_level == 'explorer' and (admin_level == 'site') and \
                publisher == 'yes':
            site_role = 'SiteAdministratorExplorer'
        if license_level == 'creator' and (admin_level == "none") and \
                publisher == 'yes':  # TODO: CHECK CASE IS NONE
            site_role = 'Creator'
        if license_level == 'explorer' and (admin_level == "none") and \
                publisher == 'yes':
            site_role = 'ExplorerCanPublish'
        if license_level == 'explorer' and (admin_level == "none") and \
                publisher == 'yes':
            site_role = 'Explorer'
        if license_level == 'viewer' and (admin_level == "none") and \
                publisher == 'no':
            site_role = 'Viewer'
        if license_level == 'unlicensed' and (admin_level == "none") and \
                publisher == 'no':
            site_role = 'Unlicensed'
        return site_role


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
