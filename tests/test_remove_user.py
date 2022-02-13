import sys
import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.remove_users_parser import RemoveUserParser


class AddUsersParserTest(unittest.TestCase):
    csv = ("testname", "testpassword", "test", "test", "test", "test")

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=(argparse.Namespace(
                    username="test",
                    password="testpass",
                    server="http://test",
                    users="users.csv",
                    site="helloworld")))
    def test_remove_users_parser_role(self, mock_args):
        with mock.patch('builtins.open', mock.mock_open(read_data='test')):
            sys.argv = ["test_csv.csv", "test", "test1", "test2"]
            args = RemoveUserParser.remove_user_parser()
            print(args)
            args_from_command = vars(args)
            args_from_mock = vars(mock_args.return_value)
            self.assertEqual(args_from_command, args_from_mock)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=(argparse.Namespace(
                    username="test",
                    password="testpass",
                    server="http://test",
                    site="helloworld")))
    def test_remove_users_parser_missing_group_name(self, mock_args):
        with mock.patch('builtins.open', mock.mock_open(read_data='test')):
            with self.assertRaises(AttributeError):
                sys.argv = ["test_csv.csv", "test", "test1", "test2"]
                args = RemoveUserParser.remove_user_parser()
                args_from_command = vars(args)
                args_from_mock = vars(mock_args.return_value)
                self.assertEqual(args_from_command, args_from_mock)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=(argparse.Namespace(users="test.csv",
                                                 username="test",
                                                 password="testpass",
                                                 server="http://test",
                                                 site="helloworld")))
    def test_remove_users_parser_missing_group_name_present(self, mock_args):
        with mock.patch('builtins.open', mock.mock_open(read_data='test')):
            sys.argv = ["test_csv.csv", "test", "test1", "test2"]
            args = RemoveUserParser.remove_user_parser()
            args_from_command = vars(args)
            args_from_mock = vars(mock_args.return_value)
            self.assertEqual(args_from_command, args_from_mock)
