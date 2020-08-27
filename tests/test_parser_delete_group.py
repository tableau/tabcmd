import sys
import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from pythontabcmd2.parsers.delete_group_parser import DeleteGroupParser


class DeleteGroupParserTestT(unittest.TestCase):
    csv = ("testname", "testpassword", "test", "test", "test", "test")

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=(argparse.Namespace(name="hello",
                                                 username="test",
                                                 password="testpass",
                                                 server="http://test",
                                                 site="helloworld")))
    def test_delete_group(self, mock_args):
        args = DeleteGroupParser.delete_group_parser()
        args_from_command = vars(args)
        args_from_mock = vars(mock_args.return_value)
        self.assertEqual(args_from_command, args_from_mock)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=(argparse.Namespace(name=None,
                                                 site="helloworld")))
    def test_create_user_parser_required_name(self, mock_args):

        args = DeleteGroupParser.delete_group_parser()
        args_from_command = vars(args)
        args_from_mock = vars(mock_args.return_value)
        self.assertEqual(args_from_command, args_from_mock)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=(argparse.Namespace()))
    def test_create_user_parser_required_name_missing(self, mock_args):
        with self.assertRaises(AttributeError):
            args = DeleteGroupParser.delete_group_parser()
            args_from_command = vars(args)
            args_from_mock = vars(mock_args.return_value)
            self.assertEqual(args_from_command, args_from_mock)
