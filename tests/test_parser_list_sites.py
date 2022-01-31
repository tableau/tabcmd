import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from pythontabcmd.parsers.list_sites_parser import ListSitesParser


class ListSitesParserTest(unittest.TestCase):

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace())
    def test_list_site_parser_user_quota_integer_missing(self, mock_args):
        with self.assertRaises(AttributeError):
            args = ListSitesParser.list_site_parser()
            args_from_command = vars(args)
            args_from_mock = vars(mock_args.return_value)
            assert args_from_command == args_from_mock

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(username="hello",
                                                password="hellotest",
                                                site="helloworld"))
    def test_list_site_parser_user_quota_integer(self, mock_args):
        args = ListSitesParser.list_site_parser()
        args_from_command = vars(args)
        args_from_mock = vars(mock_args.return_value)
        assert args_from_command == args_from_mock
