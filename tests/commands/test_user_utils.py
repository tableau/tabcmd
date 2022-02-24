import unittest
from tabcmd.commands.user.user_command import UserCommand
from tabcmd.execution.logger_config import log


class UserDataTest(unittest.TestCase):
    logger = log("UserDataTest", "debug")
    # [license_level, admin_level, publisher] ---> expected_role
    # [(explorer/creator/viewer/unlicensed), (system/site/none), (yes/no) --->
    #       (SiteAdministrator/SiteAdministratorCreator/SiteAdministratorExplorer/ExplorerCanPublish/
    #       Creator/Viewer/Unlicensed)
    role_inputs = [
        ["creator", "system", "yes", "SiteAdministrator"],
        ["None", "system", "no", "SiteAdministrator"],
        ["explorer", "SysTEm", "no", "SiteAdministrator"],
        ["creator", "site", "yes", "SiteAdministratorCreator"],
        ["explorer", "site", "yes", "SiteAdministratorExplorer"],
        ["creator", "SITE", "no", "SiteAdministratorCreator"],
        ["creator", "none", "yes", "Creator"],
        ["explorer", "none", "yes", "ExplorerCanPublish"],
        ["viewer", "None", "no", "Viewer"],
        ["explorer", "no", "yes", "ExplorerCanPublish"],
        ["EXPLORER", "noNO", "yes", "ExplorerCanPublish"],
        ["explorer", "no", "no", "Explorer"],
        ["unlicensed", "none", "no", "Unlicensed"],
        ["Chef", "none", "yes", "Unlicensed"],
        ["yes", "yes", "yes", "Unlicensed"],
    ]

    def test_evaluate_role(self):
        for input in UserDataTest.role_inputs:
            actual = UserCommand.evaluate_license_level_admin_level(input[0], input[1], input[2])
            assert actual == input[3], input + [actual]

    def test_get_user_detail_empty_line(self):
        test_line = ""
        test_user = UserCommand.parse_line(test_line)
        assert test_user is None

    def test_validate_user_detail_standard(self):
        test_line = "username, pword, fname, creator, site, 1, email"
        UserCommand.validate_user_detail_line(test_line)

    def test_get_user_detail_standard(self):
        test_line = "username, pword, fname, license, admin, pub, email"
        test_user = UserCommand.parse_line(test_line)
        print(test_user.username, test_user.password, test_user.full_name)
        assert test_user.username == 'username', test_user.username
        assert test_user.password == 'pword', test_user.password
        assert test_user.full_name == 'fname', test_user.full_name
        assert test_user.license_level == 'license', test_user.license_level
        assert test_user.admin_level == 'admin', test_user.admin_level
        assert test_user.publisher == 'pub', test_user.publisher
        assert test_user.email == 'email', test_user.email
        # assert test_user.site_role == 'Unlicensed', test_user.site_role

        def test_get_users_from_file_missing_elements(self):
            bad_content = [
                ["username, pword, , yes, email"],
                ["username"],
                ["username, pword"],
                ["username, pword, , , yes, email"]]
            with self.assertRaises(AttributeError):
                UserCommand.get_users_from_file(bad_content)

    valid_import_content = [
        "username, pword, fname, license, admin, pub, email",
        "username, pword, fname, license, admin, pub, email"]

    def test_get_users_from_file(self):
        assert UserCommand.get_users_from_file(UserDataTest.valid_import_content) is not None

    def test_validate_import_file(self):
        UserCommand.validate_file_for_import(UserDataTest.valid_import_content, UserDataTest.logger, detailed=True)

    usernames = [
        "valid",
        "valid@email.com",
        "domain/valid",
        "domain/valid@tmail.com",
        "va!@#$%^&*()lid",
        "in@v@lid",
        "in valid"
    ]

    def test_validate_username(self):
        UserCommand.validate_username(UserDataTest.usernames[0])
        UserCommand.validate_username(UserDataTest.usernames[1])
        UserCommand.validate_username(UserDataTest.usernames[2])
        UserCommand.validate_username(UserDataTest.usernames[3])
        UserCommand.validate_username(UserDataTest.usernames[4])
        with self.assertRaises(AttributeError):
            UserCommand.validate_username(UserDataTest.usernames[5])
        with self.assertRaises(AttributeError):
            UserCommand.validate_username(UserDataTest.usernames[6])

    def test_validate_usernames_file(self):
        with self.assertRaises(AttributeError):
            UserCommand.validate_file_user_names(UserDataTest.usernames, UserDataTest.logger)

    def test_get_usernames_from_file(self):
        user_list = UserCommand.get_users_from_file(UserDataTest.usernames)
        assert user_list[0] == "valid", user_list
