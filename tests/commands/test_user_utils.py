import unittest
from unittest.mock import *
from tabcmd.commands.user.user_data import UserCommand, Userdata
from tabcmd.execution.logger_config import log

from typing import List, NamedTuple, TextIO, Union
import io
import tableauserverclient as TSC


class UserDataTest(unittest.TestCase):
    logger = log("UserDataTest", "debug")

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

    valid_import_content = [
        "username, pword, fname, creator, site, yes, email",
        "username, pword, fname, explorer, none, no, email",
        "",
    ]

    valid_username_content = ["jfitzgerald@tableau.com"]

    usernames = [
        "valid",
        "valid@email.com",
        "domain/valid",
        "domain/valid@tmail.com",
        "va!@#$%^&*()lid",
        "in@v@lid",
        "in valid",
        "",
    ]

    def test_validate_usernames(self):
        UserCommand._validate_username_or_throw(UserDataTest.usernames[0])
        UserCommand._validate_username_or_throw(UserDataTest.usernames[1])
        UserCommand._validate_username_or_throw(UserDataTest.usernames[2])
        UserCommand._validate_username_or_throw(UserDataTest.usernames[3])
        UserCommand._validate_username_or_throw(UserDataTest.usernames[4])
        with self.assertRaises(AttributeError):
            UserCommand._validate_username_or_throw(UserDataTest.usernames[5])
        with self.assertRaises(AttributeError):
            UserCommand._validate_username_or_throw(UserDataTest.usernames[6])

    def test_evaluate_role(self):
        for input in UserDataTest.role_inputs:
            actual = UserCommand.evaluate_site_role(input[0], input[1], input[2])
            assert actual == input[3], input + [actual]

    def test_get_user_detail_empty_line(self):
        test_line = ""
        test_user = UserCommand._parse_line(test_line)
        assert test_user is None

    def test_get_user_detail_standard(self):
        test_line = "username, pword, fname, license, admin, pub, email"
        test_user: TSC.UserItem = UserCommand._parse_line(test_line)
        assert test_user.name == "username", test_user.name
        assert test_user.fullname == "fname", test_user.fullname
        assert test_user.site_role == "Unlicensed", test_user.site_role
        assert test_user.email == "email", test_user.email

    def test_get_user_details_only_username(self):
        test_line = "username"
        test_user: TSC.UserItem = UserCommand._parse_line(test_line)

    def test_populate_user_details_only_some(self):
        values = ["username", "", "", "creator", "admin"]
        data = Userdata()
        data.populate(values)

    def test_populate_user_details_all(self):
        values = UserDataTest.valid_import_content[0]
        data = Userdata()
        data.populate(values)

    def test_validate_user_detail_standard(self):
        test_line = "username, pword, fname, creator, site, 1, email"
        UserCommand._validate_user_or_throw(test_line, UserDataTest.logger)

    # TODO: get typings for argparse
    class NamedObject(NamedTuple):
        name: str

    ArgparseFile = Union[TextIO, NamedObject]
    # for file handling
    def _mock_file_content(self, content: List[str]) -> ArgparseFile:
        # the empty string represents EOF
        # the tests run through the file twice, first to validate then to fetch
        mock = MagicMock(io.TextIOWrapper)
        mock.readline.side_effect = content
        mock.name = "file-mock"
        return mock

    def test_get_users_from_file_missing_elements(self):
        bad_content = [
            ["username, pword, , yes, email"],
            ["username"],
            ["username, pword"],
            ["username, pword, , , yes, email"],
        ]
        with self.assertRaises(AttributeError):
            UserCommand.get_users_from_file(bad_content)

    def test_validate_import_file(self):
        test_data = self._mock_file_content(UserDataTest.valid_import_content)
        num_lines = UserCommand.validate_file_for_import(test_data, UserDataTest.logger, detailed=True)
        assert num_lines == 2, "Expected two lines to be parsed, got {}".format(num_lines)

    def test_validate_usernames_file(self):
        test_data = self._mock_file_content(UserDataTest.usernames)
        n = UserCommand.validate_file_for_import(test_data, UserDataTest.logger)
        assert n == 5, "Exactly 5 of the lines were valid, counted {}".format(n)

    def test_validate_usernames_file_strict(self):
        test_data = self._mock_file_content(UserDataTest.usernames)
        with self.assertRaises(SystemExit):
            UserCommand.validate_file_for_import(test_data, UserDataTest.logger, strict=True)

    def test_get_usernames_from_file(self):
        test_data = self._mock_file_content(UserDataTest.usernames)
        user_list = UserCommand.get_users_from_file(test_data)
        assert user_list[0].name == "valid", user_list
