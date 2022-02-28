import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.list_sites_parser import ListSitesParser
from .common_setup import *


commandname = "listsites"


class ListSitesParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(
            commandname
        )
        ListSitesParser.list_site_parser(manager, mock_command)

    def test_list_site_parser(self):
        mock_args = [commandname]
        args = self.parser_under_test.parse_args(mock_args)
        assert args is not None

    def test_list_site_parser_user_quota_integer(self):
        mock_args = [commandname, "--get-extract-encryption-mode"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.get_extract_encryption_mode is True
