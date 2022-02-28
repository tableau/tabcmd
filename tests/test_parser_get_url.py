import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.get_url_parser import GetUrlParser
from .common_setup import *

commandname = "listsites"


class GetUrlParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(
            commandname
        )
        GetUrlParser.get_url_parser(manager, mock_command)

    def test_get_url_parser_file(self):
        mock_args = vars(argparse.Namespace(filename="helloworld"))
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_get_url_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
