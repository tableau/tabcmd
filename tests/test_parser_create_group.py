import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.create_group_parser import CreateGroupParser


class CreateGroupParserTest(unittest.TestCase):
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name="test",
                                                site="helloworld"))
    def test_create_group_parser_required_name(self, mock_args):

        args = CreateGroupParser.create_group_parser()
        assert getattr(args, "name") == getattr(mock_args.return_value, "name")

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace())
    def test_create_group_parser_missing_required_name(self, mock_args):
        with self.assertRaises(AttributeError):
            args = CreateGroupParser.create_group_parser()
            args_from_command = vars(args)
            args_from_mock = vars(mock_args.return_value)
            assert args_from_command == args_from_mock

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name="test",
                                                username="testname",
                                                site="helloworld"))
    def test_create_group_parser_username(self, mock_args):
        args = CreateGroupParser.create_group_parser()
        args_from_command = vars(args)
        args_from_mock = vars(mock_args.return_value)
        assert args_from_command == args_from_mock

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name="test",
                                                password="testpass",
                                                site="helloworld"
                                                ))
    def test_create_group_parser_password(self, mock_args):
        args = CreateGroupParser.create_group_parser()
        args_from_command = vars(args)
        args_from_mock = vars(mock_args.return_value)
        assert args_from_command == args_from_mock
