import unittest

from tabcmd.commands.extracts.encrypt_extracts_command import EncryptExtracts
from .common_setup import *

commandname = "encryptextracts"


class EncryptExtractsParserTest(ParserTestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, EncryptExtracts)

    def test_encrypt_extract_parser_optional_arguments(self):
        mock_args = [commandname, "value"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.site_name == "value", args

    def test_encrypt_extract_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
