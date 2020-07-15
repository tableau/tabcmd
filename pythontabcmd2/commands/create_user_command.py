try:
    from .. import tableauserverclient as TSC
    from .. logger_config import get_logger
except:
    import tableauserverclient as TSC
    from logger_config import get_logger


class CreateUserCommand:

    def create_user(self, server_object, csv_lines):
        self.evaluate_csv_lines_call_create_user_command(csv_lines, server_object)

    def evaluate_csv_lines_call_create_user_command(self, csv_lines, server_object):
        for line in csv_lines:
            username = line[0].lower()                      #TODO: BREAK THIS FUNCTION INTO TWO
            password = line[1].lower()
            full_name = line[2].lower()
            license_level = line[3].lower()
            admin_level = line[4].lower()
            publisher = line[5].lower()
            email = line[6].lower()
            site_role = self.evaluate_license_level_admin_level(license_level, admin_level, publisher)
            try:
                new_user = TSC.UserItem(username, site_role)
                server_object.users.update(new_user, password)
            except TSC.ServerResponseError as e:
                print("error create user command")

    def evaluate_license_level_admin_level(self, license_level, admin_level, publisher):
        site_role = None
        if license_level == ('creator' or 'explorer' or 'viewer' or 'unlicensed' or '') and (admin_level == 'system') and publisher == 'yes':
            site_role = 'SiteAdministrator'
        if license_level == 'creator' and (admin_level == 'site') and publisher == 'yes':
            site_role = 'SiteAdministratorCreator'
        if license_level == 'explorer' and (admin_level == 'site') and publisher == 'yes':
            site_role = 'SiteAdministratorExplorer'
        if license_level == 'creator' and (admin_level is None or '') and publisher == 'yes':    #TODO: CHECK CASE IS NONE
            site_role = 'Creator'
        if license_level == 'explorer' and (admin_level is None or '') and publisher == 'yes':
            site_role = 'ExplorerCanPublish'
        if license_level == 'explorer' and (admin_level is None or '') and publisher == 'yes':
            site_role = 'Explorer'
        if license_level == 'viewer' and (admin_level is None or '') and publisher == 'no':
            site_role = 'Viewer'
        if license_level == 'unlicensed' and (admin_level is None or '') and publisher == 'no':
            site_role = 'Unlicensed'
        return site_role




