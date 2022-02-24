import unittest


from tabcmd.commands.user.user_command import UserCommand


class UserDataTest(unittest.TestCase):
    def test_get_users_from_file(self):
        test_content = [
            "username, pword, fname, license, admin, pub, email",
            "username, pword, fname, license, admin, pub, email",
        ]
        assert UserCommand.get_users_from_file(test_content) is not None

    def test_get_users_from_file_missing_elements(self):
        bad_content = [
            ["username, pword, , yes, email"],
            ["username"],
            ["username, pword"],
            ["username, pword, , , yes, email"],
        ]
        for input in bad_content:
            with self.assertRaises(AttributeError):
                UserCommand.get_users_from_file(input)

    def test_get_user_detail_empty_line(self):
        test_line = ""
        test_user = UserCommand.get_user_details(test_line)
        assert test_user is None

    def test_get_user_detail_standard(self):
        test_line = "username, pword, fname, license, admin, pub, email"
        test_user = UserCommand.get_user_details(test_line)
        assert test_user.username == "username", test_user.username
        assert test_user.password == "pword", test_user.password
        assert test_user.full_name == "fname", test_user.full_name
        assert test_user.license_level == "license", test_user.license_level
        assert test_user.admin_level == "admin", test_user.admin_level
        assert test_user.publisher == "pub", test_user.publisher
        assert test_user.email == "email", test_user.email
        # assert test_user.site_role == 'Unlicensed', test_user.site_role

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
