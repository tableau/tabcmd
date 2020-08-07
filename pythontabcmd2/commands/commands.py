from .command_strategy_interface import CommandStrategyInterface
import os
import tableauserverclient as TSC
import sys
import json
from . import get_logger
from .user.user_data import Userdata
logger = get_logger('pythontabcmd2.commands', 'info')


class Commands(CommandStrategyInterface):

    def __init__(self, args):
        self.logging_level = args.logging_level
        self.username = args.username #TODO: CHNAGE HERE TO USER AFTER
        self.password = args.password
        self.server = args.server
        self.site = args.site
        self.token_name = args.token_name
        self.personal_token = args.token


    @staticmethod
    def deserialize():
        try:
            home_path = os.path.expanduser("~")
            file_path = os.path.join(home_path, 'tableau_auth.json')
            with open(str(file_path), 'r') as input:
                data = json.load(input)
                token_from_json = None
                server_from_json = None
                site_id_from_json = None
                for auth in data['tableau_auth']:
                    token_from_json = auth['token']
                    server_from_json = auth['server']
                    site_id_from_json = auth['site']
                server = Commands.create_new_server(token_from_json,
                                                    server_from_json,
                                                    site_id_from_json)
                return server

        except IOError:
            logger.info("****** Please login first ******")
            sys.exit()


    @staticmethod
    def create_new_server(token, server, site_id):
        tableau_server = TSC.Server(server, use_server_version=True)
        tableau_server._auth_token = token
        tableau_server._site_id = site_id
        return tableau_server

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
        user_data.site_role = \
            self.evaluate_license_level_admin_level(user_data.license_level,
                                                    user_data.admin_level,
                                                    user_data.publisher)
        return user_data

    def evaluate_license_level_admin_level(self, license_level,
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

    # def log(self):
    #     logger = get_logger('pythontabcmd2.create_project_command',
    #                         self.logging_level)
    #     return logger