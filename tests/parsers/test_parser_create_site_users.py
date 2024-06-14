import unittest
from unittest import mock

from tabcmd.commands.user.create_site_users import CreateSiteUsersCommand
from .common_setup import *

commandname = "createsiteusers"


class CreateSiteUsersParserTest(ParserTestCase):
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
