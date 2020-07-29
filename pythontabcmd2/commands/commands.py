from .command_strategy_interface import CommandStrategyInterface
import os
import sys
import dill as pickle
from . import get_logger
from .user.user_data import Userdata
logger = get_logger('pythontabcmd2.commands')


class Commands(CommandStrategyInterface):
    @staticmethod
    def deserialize():
        """" Method to convert the pickle file back to an object """
        try:
            home_path = os.path.expanduser("~")
            file_path = os.path.join(home_path, 'tabcmd.pkl')
            with open(str(file_path), 'rb') as input:
                signed_in_object = pickle.load(input)
                server_object = pickle.load(input)
                return signed_in_object, server_object
        except IOError:
            logger.info("****** Please login first ******")
            sys.exit()

    def get_user(self, csv_file):
        user_list = []
        for line in csv_file:
            users_data = self.get_users(line)
            user_list.append(users_data)
        return user_list

    def get_users(self, line):
        split_line = line.split(',')
        user_data = Userdata()
        user_data.username = split_line[0].lower()
        user_data.password = split_line[1].lower()
        user_data.full_name = split_line[2].lower()
        user_data.license_level = split_line[3].lower()
        user_data.admin_level = split_line[4].lower()
        user_data.publisher = split_line[5].lower()
        user_data.email = split_line[6].lower()
        user_data.site_role = self.evaluate_license_level_admin_level(user_data.license_level,
                                                                      user_data.admin_level,
                                                                      user_data.publisher)
        return user_data

    def evaluate_license_level_admin_level(self, license_level, admin_level, publisher):
        site_role = None
        if license_level == ('creator' or 'explorer' or 'viewer' or 'unlicensed' or '') and (
                admin_level == 'system') and publisher == 'yes':
            site_role = 'SiteAdministrator'
        if license_level == 'creator' and (admin_level == 'site') and publisher == 'yes':
            site_role = 'SiteAdministratorCreator'
        if license_level == 'explorer' and (admin_level == 'site') and publisher == 'yes':
            site_role = 'SiteAdministratorExplorer'
        if license_level == 'creator' and (admin_level == "none") and publisher == 'yes':  # TODO: CHECK CASE IS NONE
            site_role = 'Creator'
        if license_level == 'explorer' and (admin_level == "none") and publisher == 'yes':
            site_role = 'ExplorerCanPublish'
        if license_level == 'explorer' and (admin_level == "none") and publisher == 'yes':
            site_role = 'Explorer'
        if license_level == 'viewer' and (admin_level == "none") and publisher == 'no':
            site_role = 'Viewer'
        if license_level == 'unlicensed' and (admin_level == "none") and publisher == 'no':
            site_role = 'Unlicensed'
        return site_role