import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.reencrypt_parser import ReencryptExtractsParser
from .common_setup import *

commandname = "reencryptextracts"


class ReencryptExtractsParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(
            commandname
        )
        ReencryptExtractsParser.reencrypt_extracts_parser(manager, mock_command)

    def test_reencrypt_extract_parser_optional_arguments(self):
        mock_args = [commandname, "sitename"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.sitename == "sitename", args

    def test_reencrypt_extract_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
