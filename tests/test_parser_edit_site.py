import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from pythontabcmd2.parsers.edit_site_parser import EditSiteParser


class EditSiteParserTest(unittest.TestCase):
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(site_name="testsite",
                                                no_site_mode=None,
                                                site="helloworld"))
    def test_edit_site_parser_missing_site_mode(self, mock_args):
        with self.assertRaises(AttributeError):
            args, mode, siteid = EditSiteParser.edit_site_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(site_name="testsite",
                                                site_mode=None,
                                                site="helloworld"))
    def test_edit_site_parser_missing_no_site_mode(self, mock_args):
        with self.assertRaises(AttributeError):
            args, mode, siteid = EditSiteParser.edit_site_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(site_name="testsite",
                                                site="helloworld"))
    def test_edit_site_parser_missing_both_site_modes(self, mock_args):
        with self.assertRaises(AttributeError):
            args, mode, siteid = EditSiteParser.edit_site_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace())
    def test_edit_site_parser_missing_all_args(self, mock_args):
        with self.assertRaises(AttributeError):
            args, mode, siteid = EditSiteParser.edit_site_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(site_name="testsite",
                                                user_quota=12,
                                                site_mode=None,
                                                no_site_mode=None,
                                                site="helloworld"))
    def test_edit_site_parser_user_quota_integer(self, mock_args):
        args, mode, siteid = EditSiteParser.edit_site_parser()
        args_from_command = vars(args)
        args_from_mock = vars(mock_args.return_value)
        assert args_from_command == args_from_mock

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(site_name="testsite",
                                                storage_quota=3222,
                                                user_quota=12,
                                                site_mode=None,
                                                no_site_mode=None,
                                                site="helloworld"))
    def test_edit_site_parser_storage_quota_integer(self, mock_args):
        args, mode, siteid = EditSiteParser.edit_site_parser()
        args_from_command = vars(args)
        args_from_mock = vars(mock_args.return_value)
        assert args_from_command == args_from_mock

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    username="helloworld",
                    site="helloworld1",
                    logging_level="info",
                    password="testing123",
                    no_prompt=True, token=None,
                    token_name=None,
                    no_site_mode=None,
                    site_mode=None,
                    cookie=True,
                    no_cookie=False,
                    prompt=False,
                    status=None,
                    site_id="1234",
                    run_now_enabled=None
                ))
    def test_runschedule_parser_optional_arguments(self, mock_args):
        args, mode, siteid = EditSiteParser.edit_site_parser()
        assert args == argparse.Namespace(username="helloworld",
                                          site="helloworld1",
                                          site_mode=None,
                                          no_site_mode=None,
                                          logging_level="info",
                                          password="testing123",
                                          no_prompt=True, token=None,
                                          token_name=None,
                                          cookie=True,
                                          no_cookie=False,
                                          prompt=False,
                                          status=None,
                                          site_id="1234",
                                          run_now_enabled=None)
