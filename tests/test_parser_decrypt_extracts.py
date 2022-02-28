import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.decrypt_extracts_parser import DecryptExtractsParser
from .common_setup import *


commandname = "decryptextracts"


class DecryptExtractsParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(commandname)
        DecryptExtractsParser.decrypt_extracts_parser(manager, mock_command)

    def test_decrypt_extract_parser_required_name(self):
        mock_args = [commandname, "site-name"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.sitename == "site-name", args

    """
    bug: the site name is supposed to be optional
    def test_decrypt_extract_parser_missing_site_name(self):
        mock_args = [commandname]
        args = self.parser_under_test.parse_args(mock_args)
    """
