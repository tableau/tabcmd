import unittest
from unittest import mock

from tabcmd.commands.user.create_site_users import CreateSiteUsersCommand
from .common_setup import *

commandname = "createsiteusers"


class CreateSiteUsersParserTest(ParserTest):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, CreateSiteUsersCommand)

    def test_create_site_users_parser_users_file(self):
        with mock.patch("builtins.open", mock.mock_open(read_data="test")) as open_file:
            mock_args = [commandname, "users.csv"]
            args = self.parser_under_test.parse_args(mock_args)
            open_file.assert_called_with("users.csv", "r", -1, encoding, None)

    def test_create_site_user_parser_missing_arguments(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_create_site_user_parser_role(self):
        with mock.patch("builtins.open", mock.mock_open(read_data="test")):
            mock_args = [commandname, "users.csv", "--site", "site-name"]
            args = self.parser_under_test.parse_args(mock_args)
            assert args.site_name == "site-name", args

    def test_create_site_user_parser_auth_Default(self):
        with mock.patch("builtins.open", mock.mock_open(read_data="test")):
            mock_args = [commandname, "users.csv", "--site", "site-name", "--auth-type", "ServerDefault"]
            args = self.parser_under_test.parse_args(mock_args)
            assert args.site_name == "site-name", args
            assert args.auth_type == "ServerDefault", args

    def test_create_site_user_parser_auth_MFA(self):
        with mock.patch("builtins.open", mock.mock_open(read_data="test")):
            mock_args = [commandname, "users.csv", "--site", "site-name", "--auth-type", "TableauIDWithMFA"]
            args = self.parser_under_test.parse_args(mock_args)
            assert args.site_name == "site-name", args
            assert args.auth_type == "TableauIDWithMFA", args

    def test_create_site_user_parser_auth_TabId_NotAvailable(self):
        with mock.patch("builtins.open", mock.mock_open(read_data="test")):
            mock_args = [commandname, "users.csv", "--site", "site-name", "--auth-type", "TableauId"]
            with self.assertRaises(SystemExit):
                args = self.parser_under_test.parse_args(mock_args)

    def test_create_site_user_parser_idp_configuration_id(self):
        with mock.patch("builtins.open", mock.mock_open(read_data="test")):
            mock_args = [commandname, "users.csv", "--idp-configuration-id", "12345678-1234-5678-1234-567812345678"]
            args = self.parser_under_test.parse_args(mock_args)
            assert args.idp_configuration_id == "12345678-1234-5678-1234-567812345678", args
            assert args.auth_type is None, args

    def test_create_site_user_parser_auth_and_idp_mutually_exclusive(self):
        # argparse should reject requests that pass both flags at once.
        with mock.patch("builtins.open", mock.mock_open(read_data="test")):
            mock_args = [
                commandname,
                "users.csv",
                "--auth-type",
                "SAML",
                "--idp-configuration-id",
                "12345678-1234-5678-1234-567812345678",
            ]
            with self.assertRaises(SystemExit):
                self.parser_under_test.parse_args(mock_args)

    def test_create_site_user_parser_idp_configuration_id_rejects_non_uuid(self):
        # argparse should reject non-UUID values (typos, free text) at parse time
        # rather than sending them to the REST API and failing with a server-side
        # validation error.
        with mock.patch("builtins.open", mock.mock_open(read_data="test")):
            for bad_value in ("not-a-uuid", "abc-123-idp", ""):
                with self.assertRaises(SystemExit):
                    self.parser_under_test.parse_args([commandname, "users.csv", "--idp-configuration-id", bad_value])
