import sys
import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.create_users_parser import CreateUserParser


class CreateUserParserTest(unittest.TestCase):
    csv = ("testname", "testpassword", "test", "test", "test", "test")

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=(argparse.Namespace(
                                                 username="test",
                                                 password="testpass",
                                                 server="http://test",
                                                 site="helloworld")))
    def test_create_user_parser_role(self, mock_args):
        with mock.patch('builtins.open', mock.mock_open(read_data='test')):
            sys.argv = ["test_csv.csv", "test", "test1", "test2"]
            csv_lines, args = CreateUserParser.create_user_parser()
            args_from_command = vars(args)
            args_from_mock = vars(mock_args.return_value)
            self.assertEqual(args_from_command, args_from_mock)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=(argparse.Namespace()))
    def test_create_user_parser_missing_arguments(self, mock_args):
        with mock.patch('builtins.open', mock.mock_open(read_data='test')):
            with self.assertRaises(AttributeError):
                sys.argv = ["test_csv.csv", "test", "test1", "test2"]
                csv_lines, args = CreateUserParser.create_user_parser()
                args_from_command = vars(args)
                args_from_mock = vars(mock_args.return_value)
                self.assertEqual(args_from_command, args_from_mock)
