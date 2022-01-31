import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.create_site_parser import CreateSiteParser


class CreateSiteParserTest(unittest.TestCase):
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(site_name="testsite",
                                                no_site_mode=None))
    def test_create_site_parser_missing_site_mode(self, mock_args):
        with self.assertRaises(AttributeError):
            args, mode = CreateSiteParser.create_site_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(site_name="testsite",
                                                site_mode=None))
    def test_create_site_parser_missing_no_site_mode(self, mock_args):
        with self.assertRaises(AttributeError):
            args, mode = CreateSiteParser.create_site_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(site_name="testsite"))
    def test_create_site_parser_missing_both_site_modes(self, mock_args):
        with self.assertRaises(AttributeError):
            args, mode = CreateSiteParser.create_site_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace())
    def test_create_site_parser_missing_all_args(self, mock_args):
        with self.assertRaises(AttributeError):
            args, mode = CreateSiteParser.create_site_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(site_name="testsite",
                                                user_quota=12,
                                                site_mode=None,
                                                no_site_mode=None,
                                                site="helloworld"))
    def test_create_site_parser_user_quota_integer(self, mock_args):
        args, mode = CreateSiteParser.create_site_parser()
        args_from_command = vars(args)
        args_from_mock = vars(mock_args.return_value)
        assert args_from_command == args_from_mock
