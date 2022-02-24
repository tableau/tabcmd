import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.export_parser import ExportParser
from .common_setup import *

commandname = "export"


class ExportParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(commandname)
        ExportParser.export_parser(manager, mock_command)

    def test_export_parser_file_type_pdf(self):
        mock_args = mock_args = ["export", "helloworld", "--pdf"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.pdf is True, args
        assert args.url == "helloworld", args

    def test_export_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
