from commands.user.user_command import UserCommand

try:
    from tabcmd2.pythontabcmd2 import tableauserverclient as TSC
    from logger_config import get_logger

except:
    import tableauserverclient as TSC
    from logger_config import get_logger
    from constants import *

logger = get_logger('pythontabcmd2.create_user_command')


class CreateUserCommand(UserCommand):

    def create_user(self, server_object, csv_lines):
        self.create_user_command(csv_lines, server_object)



    def create_user_command(self, csv_lines, server_object):
        for line in csv_lines:
            split_line = line.split(',')

            username = split_line[0].lower()  # TODO: BREAK THIS FUNCTION INTO TWO
            password = split_line[1].lower()
            full_name = split_line[2].lower()
            license_level = split_line[3].lower()
            admin_level = split_line[4].lower()
            publisher = split_line[5].lower()
            email = split_line[6].lower()
            site_role = self.evaluate_license_level_admin_level(license_level, admin_level, publisher)

            try:
                new_user = TSC.UserItem(username, site_role)
                new_user_added = server_object.users.add(new_user)
                server_object.users.update(new_user_added, password)
            except TSC.ServerResponseError as e:
                if e.code == Constants.forbidden:
                    logger.info("User is not local, and the user's credentials are not maintained on Tableau Server.")
                if e.code == Constants.invalid_credentials:
                    logger.info("Unauthorized access, Please login")
                if e.code == Constants.user_already_member_of_site:
                    logger.info("User already member of site")

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
