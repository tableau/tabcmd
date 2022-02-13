import sys
import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.delete_site_users_parser import DeleteSiteUsersParser


class DeleteSiteUsersParserTest(unittest.TestCase):
    csv = ("testname", "testpassword", "test", "test", "test", "test")

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=(argparse.Namespace(
                    username="test",
                    password="testpass",
                    server="http://test",
                    site="helloworld")))
    def test_delete_site_user_parser(self, mock_args):
        with mock.patch('builtins.open', mock.mock_open(read_data='test')):
            sys.argv = ["test_csv.csv", "test", "test1", "test2"]
            args = DeleteSiteUsersParser.delete_site_users_parser()
            args_from_command = vars(args)
            args_from_mock = vars(mock_args.return_value)
            self.assertEqual(args_from_command, args_from_mock)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=(argparse.Namespace(
                    username="test",
                    password="testpass",
                    server="http://test",
                    site="helloworld")))
    def test_delete_site_user_parser_all_args(self, mock_args):
        with mock.patch('builtins.open', mock.mock_open(read_data='test')):
            sys.argv = ["test_csv.csv", "test", "test1", "test2"]
            args = DeleteSiteUsersParser.delete_site_users_parser()
            assert args == argparse.Namespace(username="test",
                                              password="testpass",
                                              server="http://test",
                                              site="helloworld",
                                              csv_lines=['test']), args

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=(argparse.Namespace()))
    def test_delete_site_user_parser_missing_arguments(self, mock_args):
        with mock.patch('builtins.open', mock.mock_open(read_data='test')):
            with self.assertRaises(AttributeError):
                sys.argv = ["test_csv.csv", "test", "test1", "test2"]
                args = DeleteSiteUsersParser.delete_site_users_parser()
                args_from_command = vars(args)
                args_from_mock = vars(mock_args.return_value)
                self.assertEqual(args_from_command, args_from_mock)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=(argparse.Namespace(
                    password="testpass",
                    server="http://test",
                    site="helloworld")))
    def test_delete_site_user_parser_missing_username(self, mock_args):
        with mock.patch('builtins.open', mock.mock_open(read_data='test')):
            sys.argv = ["test_csv.csv", "test", "test1", "test2"]
            args = DeleteSiteUsersParser.delete_site_users_parser()
            args_from_command = vars(args)
            args_from_mock = vars(mock_args.return_value)
            self.assertEqual(args_from_command, args_from_mock)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=(argparse.Namespace(
                    password="testpass",
                    server="http://test")))
    def test_delete_site_user_parser_missing_site(self, mock_args):
        with self.assertRaises(AttributeError):
            with mock.patch('builtins.open', mock.mock_open(read_data='test')):
                sys.argv = ["test_csv.csv", "test", "test1", "test2"]
                args = DeleteSiteUsersParser.delete_site_users_parser()
                args_from_command = vars(args)
                args_from_mock = vars(mock_args.return_value)
                self.assertEqual(args_from_command, args_from_mock)
