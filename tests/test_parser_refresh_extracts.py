import unittest
from tabcmd.parsers.refresh_extracts_parser import RefreshExtractsParser
from .common_setup import *

commandname = "refreshextracts"


class RefreshExtractsParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(
            commandname
        )
        RefreshExtractsParser.refresh_extracts_parser(manager, mock_command)

    def test_refresh_extract_parser_conflicting_arguments(self):
        mock_args = [commandname, "--datasource", "hello", "--workbook", "testworkbook"]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_refresh_extract_parser_optional_arguments(self):
        mock_args = [
            commandname,
            "--datasource",
            "hello",
            "--incremental",
            "True",
            "--removecalculations",
            "--project",
            "testproject",
            "--url",
            "testurl",
        ]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.incremental == "True", args

    def test_refresh_extract_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
