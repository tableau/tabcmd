import unittest
from unittest import mock
from tabcmd.parsers.add_users_parser import AddUserParser
from .common_setup import *

commandname = 'addusers'


class AddUsersParserTest(unittest.TestCase):
    csv = ('testname', 'testpassword', 'test', 'test', 'test', 'test')
    defaults = {
        'use_certificate': None,
        'server': 'https://localhost/',
        'site': '',
        'logging_level': 'info',
        'no_prompt': False,
        'token': None,
        'token_name': None,
        'cookie': False,  # bug!
        'no_cookie': False,
        'prompt': True,
        'username': None
    }

    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(commandname)
        AddUserParser.add_user_parser(manager, mock_command)

    def test_add_users_parser_role(self):
        cmd_line_input = [commandname, 'group-name', '--users', 'users.csv']
        with mock.patch('builtins.open', mock.mock_open(read_data='users.csv')) as file:
            expected = {**{'groupname': 'group-name'}, **AddUsersParserTest.defaults}
            args_from_command = vars(self.parser_under_test.parse_args(cmd_line_input))
            print(args_from_command)
            assert args_from_command['users'] is not None
            assert args_from_command['func'] is not None  # has id'd a subcommand
            assert args_from_command['groupname'] == 'group-name'
            # direct comparison is hard b/c of weird mocked open file

    @mock.patch('builtins.open')
    def test_add_user_parser_missing_group_name(self, filereader):
        cmd_line_input = [commandname, '--users', 'test_csv.csv']
        with self.assertRaises(SystemExit):
            self.parser_under_test.parse_args(cmd_line_input)

    def test_add_user_parser_missing_users(self):
        expected = {**{'groupname': 'group-name'}, **AddUsersParserTest.defaults}
        cmd_line_input = [commandname, 'group-name']
        args_from_command = vars(self.parser_under_test.parse_args(cmd_line_input))
        assert args_from_command is not None
        assert args_from_command['users'] is None
        assert args_from_command['func'] is not None  # has id'd a subcommand
        assert args_from_command['groupname'] == 'group-name'

    @mock.patch('builtins.open')
    def test_add_user_parser_extra_args_present(self, filereader):
        expected = {**{'groupname': 'group-name', 'users': 'file_mock'}, **AddUsersParserTest.defaults}
        cmd_line_input = [commandname, 'group-name', '--users', 'users.csv']
        args_from_command = vars(self.parser_under_test.parse_args(cmd_line_input))
        print(args_from_command)
        assert args_from_command['func'] is not None  # has id'd a subcommand
        assert args_from_command['groupname'] == 'group-name', args_from_command['groupname']
