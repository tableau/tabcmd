import unittest

from tabcmd.commands.site.delete_site_command import DeleteSiteCommand
from .common_setup import *

commandname = "deletesite"


class DeleteSiteParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, DeleteSiteCommand)

    def test_delete_site(self):
        mock_args = [commandname, "site-name"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.site_name == "site-name", args

    def test_delete_site_required_name_none(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
