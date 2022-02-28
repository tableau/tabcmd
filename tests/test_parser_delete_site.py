import unittest
from tabcmd.parsers.delete_site_parser import DeleteSiteParser
from .common_setup import *

commandname = "deletesite"


class DeleteSiteParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(
            commandname
        )
        DeleteSiteParser.delete_site_parser(manager, mock_command)

    def test_delete_site(self):
        mock_args = [commandname, "site-name"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.sitename == "site-name", args

    def test_delete_site_required_name_none(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
