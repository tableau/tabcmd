import unittest

from tabcmd.commands.extracts.reencrypt_extracts_command import ReencryptExtracts
from .common_setup import *

commandname = "reencryptextracts"


class ReencryptExtractsParserTest(ParserTestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, ReencryptExtracts)

    def test_reencrypt_extract_parser_optional_arguments(self):
        mock_args = [commandname, "site-name"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.site_name == "site-name", args

    def test_reencrypt_extract_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
