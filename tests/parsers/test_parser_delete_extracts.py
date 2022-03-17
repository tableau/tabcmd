import unittest

from tabcmd.parsers.delete_extracts_parser import DeleteExtractsParser
from .common_setup import *

commandname = "deleteextracts"


class DeleteExtractsParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(commandname)
        DeleteExtractsParser.delete_extracts_parser(manager, mock_command)

    def test_delete_extract_parser_datasource(self):
        mock_args = [
            commandname,
            "-d",
            "ds-name",
            "--project",
            "prjt",
            "--parent-project-path",
            "ppp",
        ]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.datasource == "ds-name", args
        assert args.project_name == "prjt", args
        assert args.parent_project_path == "ppp"

    def test_delete_extract_parser_workbook(self):
        mock_args = [commandname, "-w", "wb-name"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.workbook == "wb-name", args
        assert args.project_name == "", args

    def test_delete_extract_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_delete_extract_parser_ds_and_wb(self):
        mock_args = [commandname, "-d", "ds", "-w", "wb"]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
