import unittest
from unittest import mock

from tabcmd.commands.user.create_users_command import CreateUsersCommand
from .common_setup import *

commandname = "createusers"


class CreateUsersTest(ParserTest):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, CreateUsersCommand)

    def test_create_users_parser_users_file(self):
        with mock.patch("builtins.open", mock.mock_open(read_data="test")) as open_file:
            mock_args = [commandname, "users.csv"]
            args = self.parser_under_test.parse_args(mock_args)
            open_file.assert_called_with("users.csv", "r", -1, encoding, None)

    def test_create_user_parser_missing_arguments(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_create_user_parser_role(self):
        with mock.patch("builtins.open", mock.mock_open(read_data="test")):
            mock_args = [commandname, "users.csv", "-r", "SiteAdministrator"]
            args = self.parser_under_test.parse_args(mock_args)
            assert args.role.lower() == "SiteAdministrator".lower(), args

    def test_create_user_parser_idp_configuration_id(self):
        with mock.patch("builtins.open", mock.mock_open(read_data="test")):
            mock_args = [commandname, "users.csv", "--idp-configuration-id", "abc-123-idp"]
            args = self.parser_under_test.parse_args(mock_args)
            assert args.idp_configuration_id == "abc-123-idp", args
            assert args.auth_type is None, args

    def test_create_user_parser_auth_and_idp_mutually_exclusive(self):
        # argparse should reject requests that pass both flags at once.
        with mock.patch("builtins.open", mock.mock_open(read_data="test")):
            mock_args = [
                commandname,
                "users.csv",
                "--auth-type",
                "SAML",
                "--idp-configuration-id",
                "abc-123-idp",
            ]
            with self.assertRaises(SystemExit):
                self.parser_under_test.parse_args(mock_args)
