import unittest

import argparse
from tabcmd.parsers.edit_site_parser import EditSiteParser
from .common_setup import *

commandname = "editsites"


class EditSiteParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(commandname)
        EditSiteParser.edit_site_parser(manager, mock_command)

    def test_edit_site_parser_optional_args_present(self):
        mock_args = [
            commandname,
            "site-to-edit",
            "--site-name",
            "new-site-name",
            "--user-quota",
            "12",
        ]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.site_name == "site-to-edit", args
        assert args.new_site_name == "new-site-name", args
        assert args.user_quota == 12, args

    def test_edit_site_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    """
    bug: this should probably exit unhappy?
    def test_edit_site_parser_missing_all_args(self):
        mock_args = [commandname, 'site-to-edit']
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
    """

    def test_edit_site_parser_storage_quota_integer(self):
        mock_args = [commandname, "site-to-edit", "--storage-quota", "12"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.site_name == "site-to-edit", args
        assert args.storage_quota == 12, args

    def test_edit_site_parser_optional_arguments_archive(self):
        mock_args = [
            commandname,
            "site-to-edit",
            "--status",
            "ACTIVE",
            "--site-id",
            "1234",
            "--run-now-enabled",
            "true",
        ]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.site_id == "1234", args
        assert args.status == "ACTIVE", args
        assert args.run_now_enabled == "true", args
