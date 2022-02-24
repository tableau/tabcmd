from ..commands import Commands
import tableauserverclient as TSC
from .user_data import Userdata


class UserCommand(Commands):
    """
    This class acts as a base class for user related group of commands
    """

    @staticmethod
    def find_user_id(server, username):
        """Method to find the user id given username"""
        all_users = list(TSC.Pager(server.users))
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
        if line is None:
            return
        line = line.strip().lower()
        if line is False or line == "\n" or line == "":
            return None

        split_line = list(map(str.strip, line.split(",")))
        if len(split_line) != 7:
            raise AttributeError("CSV file must contain exactly 7 columns, even if some are always empty")
        user_data = Userdata()
        if split_line[0] is None or split_line[0] == "":
            raise AttributeError("Username must be specified in csv file")
        user_data.username = split_line[0]
        if split_line[1] is None or split_line[1] == "":
            raise AttributeError("Passwords must be specified in csv file")
        user_data.password = split_line[1]
        user_data.full_name = split_line[2]
        user_data.license_level = split_line[3]
        user_data.admin_level = split_line[4]
        user_data.publisher = split_line[5]
        user_data.email = split_line[6]
        user_data.site_role = UserCommand.evaluate_license_level_admin_level(
            user_data.license_level, user_data.admin_level, user_data.publisher
        )
        return user_data

    @staticmethod
    def evaluate_license_level_admin_level(license_level, admin_level, publisher):
        # ignore case everywhere
        license_level = license_level.lower()
        admin_level = admin_level.lower()
        publisher = publisher.lower()
        site_role = None
        # don't need to check publisher for system/site admin
        if admin_level == "system":
            site_role = "SiteAdministrator"
        elif admin_level == "site":
            if license_level == "creator":
                site_role = "SiteAdministratorCreator"
            elif license_level == "explorer":
                site_role = "SiteAdministratorExplorer"
            else:
                site_role = "SiteAdministratorExplorer"
        else:  # if it wasn't 'system' or 'site' then we can treat it as 'none'
            if publisher == "yes":
                if license_level == "creator":
                    site_role = "Creator"
                elif license_level == "explorer":
                    site_role = "ExplorerCanPublish"
                else:
                    site_role = "Unlicensed"  # is this the expected outcome?
            else:  # publisher == 'no':
                if license_level == "explorer" or license_level == "creator":
                    site_role = "Explorer"
                elif license_level == "viewer":
                    site_role = "Viewer"
                else:  # if license_level == 'unlicensed'
                    site_role = "Unlicensed"
        if site_role is None:
            site_role = "Unlicensed"
        return site_role

    @staticmethod
    def find_group(server, group_name):
        """Method to find the group id given group name"""
        all_groups, pagination_item = server.groups.get()
        all_group_names = [(group.name, group) for group in all_groups]
        group_item = None
        for group in all_group_names:
            if group[0] == group_name:
                group_item = group[1]
                break
        return group_item
