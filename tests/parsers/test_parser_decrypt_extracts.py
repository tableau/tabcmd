import unittest

from tabcmd.commands.extracts.decrypt_extracts_command import DecryptExtracts
from .common_setup import *

commandname = "decryptextracts"


class DecryptExtractsParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, DecryptExtracts)

    def test_decrypt_extract_parser_required_name(self):
        mock_args = [commandname, "site-name"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.site_name == "site-name", args

    """
    bug: the site name is supposed to be optional
    def test_decrypt_extract_parser_missing_site_name(self):
        mock_args = [commandname]
        args = self.parser_under_test.parse_args(mock_args)
    """
