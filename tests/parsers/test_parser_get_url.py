import unittest
import argparse
from src.commands.datasources_and_workbooks.get_url_command import GetUrl
from .common_setup import *

commandname = "listsites"


class GetUrlParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, GetUrl)

    def test_get_url_parser_file(self):
        mock_args = vars(argparse.Namespace(filename="helloworld"))
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_get_url_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
