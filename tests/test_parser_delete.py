import sys
import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.delete_parser import DeleteParser


class DeleteGroupParserTestT(unittest.TestCase):

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=(argparse.Namespace(
                    username="test",
                    password="testpass",
                    server="http://test",
                    site="helloworld")))
    def test_delete_parser_login(self, mock_args):
        args = DeleteParser.delete_parser()
        args_from_command = vars(args)
        args_from_mock = vars(mock_args.return_value)
        self.assertEqual(args_from_command, args_from_mock)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=(argparse.Namespace(datasource="hellotest",

                                                 site="helloworld")))
    def test_delete_parser(self, mock_args):
        args = DeleteParser.delete_parser()
        args_from_command = vars(args)
        args_from_mock = vars(mock_args.return_value)
        self.assertEqual(args_from_command, args_from_mock)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=(argparse.Namespace(datasource="hellotest",
                                                 workbook=None,
                                                 site="helloworld")))
    def test_delete_parser_datasource_and_workbook_present(self, mock_args):
        args = DeleteParser.delete_parser()
        args_from_command = vars(args)
        args_from_mock = vars(mock_args.return_value)
        self.assertEqual(args_from_command, args_from_mock)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=(argparse.Namespace()))
    def test_delete_parser_missing_args(self, mock_args):
        with self.assertRaises(AttributeError):
            args = DeleteParser.delete_parser()
            args_from_command = vars(args)
            args_from_mock = vars(mock_args.return_value)
            self.assertEqual(args_from_command, args_from_mock)
