import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.encrypt_extracts_parser import EncryptExtractsParser
from .common_setup import *

commandname = 'encryptextracts'


class EncryptExtractsParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(commandname)
        EncryptExtractsParser.encrypt_extracts_parser(manager, mock_command)

    def test_encrypt_extract_parser_optional_arguments(self):
        mock_args = [commandname, 'value']
        args = self.parser_under_test.parse_args(mock_args)
        assert args.sitename == 'value', args

    def test_encrypt_extract_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
