import unittest

from tabcmd.commands.datasources_and_workbooks.export_command import ExportCommand
from .common_setup import *

commandname = "export"


class ExportParserTest(ParserTestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, ExportCommand)

    def test_export_parser_file_type_pdf(self):
        mock_args = mock_args = ["export", "helloworld", "--pdf"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.pdf is True, args
        assert args.url == "helloworld", args

    def test_export_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
