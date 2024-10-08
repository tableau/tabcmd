import unittest

from tabcmd.commands.site.list_sites_command import ListSiteCommand
from .common_setup import *

commandname = "listsites"


class ListSitesParserTest(ParserTestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, ListSiteCommand)

    def test_list_site_parser(self):
        mock_args = [commandname]
        args = self.parser_under_test.parse_args(mock_args)
        assert args is not None

    def test_list_site_parser_user_quota_integer(self):
        mock_args = [commandname, "--get-extract-encryption-mode"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.get_extract_encryption_mode is True
