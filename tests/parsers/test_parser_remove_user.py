import unittest
from unittest import mock

from tabcmd.commands.user.remove_users_command import RemoveUserCommand
from .common_setup import *

commandname = "removeusers"


class RemoveUsersParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, RemoveUserCommand)

    def test_remove_users_parser_required_name(self):
        with mock.patch("builtins.open", mock.mock_open(read_data="test")) as open_file:
            mock_args = [commandname, "group-name", "--users", "file"]
            args = self.parser_under_test.parse_args(mock_args)
            self.assertEqual(args.name, "group-name")

    def test_remove_users_parser_users_file(self):
        with mock.patch("builtins.open", mock.mock_open(read_data="test")) as open_file:
            mock_args = [commandname, "group-name", "--users", "users.csv"]
            args = self.parser_under_test.parse_args(mock_args)
            self.assertEqual(args.name, "group-name")
            open_file.assert_called_with("users.csv", "r", -1, encoding, None)

    def test_remove_users_parser_missing_group_name(self):
        with mock.patch("builtins.open", mock.mock_open(read_data="test")):
            mock_args = [commandname, "--users", "users.csv"]
            with self.assertRaises(SystemExit):
                self.parser_under_test.parse_args(mock_args)

    # --[no-]complete?
