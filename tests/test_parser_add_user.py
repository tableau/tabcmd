import unittest
from unittest import mock
from tabcmd.parsers.add_users_parser import AddUserParser
from .common_setup import *

commandname = 'addusers'


class AddUsersParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(commandname)
        AddUserParser.add_user_parser(manager, mock_command)

    def test_add_users_parser_role(self):
        cmd_line_input = [commandname, 'group-name', '--users', 'users.csv']
        with mock.patch('builtins.open', mock.mock_open(read_data='users.csv')) as file:
            args_from_command = vars(self.parser_under_test.parse_args(cmd_line_input))
            print(args_from_command)
            assert args_from_command['users'] is not None
            assert args_from_command['func'] is not None  # has id'd a subcommand
            assert args_from_command['groupname'] == 'group-name'
            assert args_from_command['require_all_valid'] is True

    def test_add_users_parser_users_file(self):
        with mock.patch('builtins.open', mock.mock_open(read_data='test')) as open_file:
            mock_args = [commandname, 'group-name', '--users', "users.csv"]
            args = self.parser_under_test.parse_args(mock_args)
            self.assertEqual(args.groupname, 'group-name')
            open_file.assert_called_with('users.csv', 'r', -1, 'UTF-8', None)

    @mock.patch('builtins.open')
    def test_add_user_parser_missing_group_name(self, filereader):
        cmd_line_input = [commandname, '--users', 'test_csv.csv']
        with self.assertRaises(SystemExit):
            self.parser_under_test.parse_args(cmd_line_input)

    def test_add_user_parser_missing_users(self):
        cmd_line_input = [commandname, 'group-name']
        with self.assertRaises(SystemExit):
            self.parser_under_test.parse_args(cmd_line_input)

    @mock.patch('builtins.open')
    def test_add_user_parser_complete(self, filereader):
        cmd_line_input = [commandname, 'group-name', '--users', 'users.csv', '--complete']
        with mock.patch('builtins.open', mock.mock_open(read_data='users.csv')) as file:
            args_from_command = vars(self.parser_under_test.parse_args(cmd_line_input))
            assert args_from_command['require_all_valid'] is True, args_from_command

    @mock.patch('builtins.open')
    def test_add_user_parser_extra_args_present(self, filereader):
        cmd_line_input = [commandname, 'group-name', '--users', 'users.csv', 'what']
        with self.assertRaises(SystemExit):
            self.parser_under_test.parse_args(cmd_line_input)
