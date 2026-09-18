import argparse
import unittest
from unittest.mock import *
from tabcmd.commands.user.user_data import UserCommand, Userdata
from tabcmd.execution.logger_config import log

from typing import List, Optional
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
        "u",
        "p",
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
        for line in UserDataTest.role_inputs:
            actual = UserCommand.evaluate_site_role(line[0], line[1], line[2])
            assert actual == line[3], line + [actual]

    def test_get_user_detail_empty_line(self):
        test_line = ""
        test_user = UserCommand._parse_line(test_line)
        assert test_user is None

    def test_get_user_detail_standard(self):
        test_line = "username, pword, fname, license, admin, pub, email"
        test_user: Optional[TSC.UserItem] = UserCommand._parse_line(test_line)
        assert test_user is not None
        assert test_user.name == "username", test_user.name
        assert test_user.fullname == "fname", test_user.fullname
        assert test_user.site_role == "Unlicensed", test_user.site_role
        assert test_user.email == "email", test_user.email

    def test_get_user_details_only_username(self):
        test_line = "username"
        test_user: Optional[TSC.UserItem] = UserCommand._parse_line(test_line)
        assert test_user is not None

    def test_populate_user_details_only_some(self):
        values = ["username", "", "", "creator", "admin"]
        data = Userdata()
        data.populate(values)

    def test_populate_user_details_all(self):
        values = UserDataTest.valid_import_content[0]
        data = Userdata()
        data.populate([values])

    def test_validate_user_detail_standard(self):
        test_line = "username, pword, fname, creator, site, 1, email"
        UserCommand._validate_user_or_throw(test_line, UserDataTest.logger)

    # for file handling
    def _mock_file_content(self, content: List[str]) -> io.TextIOWrapper:
        # the empty string represents EOF
        # the tests run through the file twice, first to validate then to fetch
        mock = MagicMock(io.TextIOWrapper)
        content.append("")  # EOF
        mock.readline.side_effect = content
        mock.name = "file-mock"
        return mock

    def test_get_users_from_file_missing_elements(self):
        bad_content = [
            "username, pword, , yes, email",
            "username",
            "username, pword",
            "username, pword, , , yes, email",
        ]
        test_data = self._mock_file_content(bad_content)
        UserCommand.get_users_from_file(test_data)

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

    def test_validate_mixed_case_license(self):
        # Regression: _validate_item was case-sensitive; tabcmd issue #351
        UserCommand._validate_user_or_throw("username, pword, fname, Viewer, None, no, email", UserDataTest.logger)
        UserCommand._validate_user_or_throw("username, pword, fname, Creator, Site, yes, email", UserDataTest.logger)
        UserCommand._validate_user_or_throw("username, pword, fname, EXPLORER, NONE, YES, email", UserDataTest.logger)

    def test_parse_line_preserves_role(self):
        # Regression: CreateUsersCommand replaced user_obj with bare TSC.UserItem(name), discarding role/auth
        user = UserCommand._parse_line("username, pword, fname, creator, none, yes, email")
        assert user is not None
        assert user.site_role == "Creator", f"Expected Creator, got {user.site_role}"


class ApplyCliOverridesTest(unittest.TestCase):
    """
    Covers UserCommand.apply_cli_overrides, which both createsiteusers and
    createUsers invoke before calling server.users.add.
    """

    def _mk_args(self, role=None, auth_type=None, idp_configuration_id=None):
        return argparse.Namespace(role=role, auth_type=auth_type, idp_configuration_id=idp_configuration_id)

    def test_idp_flag_applied_when_present(self):
        user = TSC.UserItem("alice", "Viewer")
        UserCommand.apply_cli_overrides(user, self._mk_args(idp_configuration_id="idp-uuid-1"))
        assert user.idp_configuration_id == "idp-uuid-1"
        assert user.auth_setting is None

    def test_idp_flag_overrides_auth_type_flag(self):
        # Argparse's mutually_exclusive_group prevents both flags from being passed
        # via the CLI in practice, but the runtime clear is still the last-line-of-defense
        # so the wire request never has both attributes.
        user = TSC.UserItem("alice", "Viewer")
        UserCommand.apply_cli_overrides(user, self._mk_args(auth_type="SAML", idp_configuration_id="idp-uuid-2"))
        assert user.idp_configuration_id == "idp-uuid-2"
        assert user.auth_setting is None

    def test_idp_flag_clears_existing_auth_setting(self):
        # A user_obj may already have an auth_setting picked up from the CSV row's
        # 8th column before apply_cli_overrides runs. If the operator passes
        # --idp-configuration-id, that IDP wins and the pre-existing auth is cleared.
        user = TSC.UserItem("alice", "Viewer")
        user.auth_setting = "OpenID"  # e.g. set from CSV col 8
        UserCommand.apply_cli_overrides(user, self._mk_args(idp_configuration_id="idp-uuid-3"))
        assert user.idp_configuration_id == "idp-uuid-3"
        assert user.auth_setting is None

    def test_auth_type_still_works_when_no_idp(self):
        user = TSC.UserItem("alice", "Viewer")
        UserCommand.apply_cli_overrides(user, self._mk_args(auth_type="SAML"))
        assert user.auth_setting == "SAML"
        assert user.idp_configuration_id is None

    def test_neither_flag_leaves_user_unchanged(self):
        # Backward-compat: users invoking without either flag see no change.
        user = TSC.UserItem("alice", "Viewer")
        user.auth_setting = "OpenID"
        UserCommand.apply_cli_overrides(user, self._mk_args())
        assert user.auth_setting == "OpenID"
        assert user.idp_configuration_id is None

    def test_role_flag_applied(self):
        user = TSC.UserItem("alice", "Viewer")
        UserCommand.apply_cli_overrides(user, self._mk_args(role="Creator"))
        assert user.site_role == "Creator"
