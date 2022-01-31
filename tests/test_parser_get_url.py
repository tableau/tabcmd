import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from pythontabcmd.parsers.get_url_parser import GetUrlParser


class GetUrlParserTest(unittest.TestCase):
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(filename="helloworld"))
    def test_get_url_parser_file(self, mock_args):
        with self.assertRaises(AttributeError):
            args, url = GetUrlParser.get_url_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace())
    def test_get_url_parser_missing_all_args(self, mock_args):
        with self.assertRaises(AttributeError):
            args, url = GetUrlParser.get_url_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(site="default",
                                                filename="helloworld",
                                                ))
    def test_get_url_parser_optional_args(self, mock_args):
        args, url = GetUrlParser.get_url_parser()
        args_from_command = vars(args)
        args_from_mock = vars(mock_args.return_value)
        assert args_from_command == args_from_mock
