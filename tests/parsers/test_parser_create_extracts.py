import unittest
import sys
import argparse
from tabcmd.parsers.create_extracts_parser import CreateExtractsParser
from .common_setup import *

commandname = "createextracts"


class CreateExtractsParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(commandname)
        CreateExtractsParser.create_extracts_parser(manager, mock_command)

    def test_create_extract_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_create_extract_parser_missing_project_path(self):
        mock_args = [
            commandname,
            "--project",
            "test123",
            "--workbook",
            "workbooktest",
            "--include-all",
            "test",
        ]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_create_extract_parser_mutually_exclusive_opts(self):
        mock_args = [
            commandname,
            "--project",
            "test123",
            "--workbook",
            "workbooktest",
            "--embedded-datasources",
            "desc",
            "--include-all",
            "test",
        ]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_create_extract_parser_optional_arguments(self):
        mock_args = [
            commandname,
            "--datasource",
            "testproject",
            "--project",
            "test123",
            "--parent-project-path",
            "abcdef",
            "--include-all",
        ]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.datasource == "testproject", args
        assert args.include_all is True, args

    def test_create_extract_parser_missing_workbook(self):
        mock_args = [
            commandname,
            "--workbook",  # no workbook name 'testproject',
            "--project",
            "test123",
            "--parent_project_path",
            "abcdef",
            "--embedded_datasources",
            "desc",
            "--workbook",
            "workbooktest",
            "--include_all",
        ]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_create_extract_parser_missing_datasource(self):
        mock_args = [
            commandname,
            "--datasource",  # no name 'testproject',
            "--project",
            "test123",
            "--parent-project-path",
            "abcdef",
            "--embedded-datasources",
            "desc",
            "--workbook",
            "workbooktest",
            "--include-all",
        ]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_create_extract_parser_missing_embedded_datasources(self):
        mock_args = [
            commandname,
            "--datasource",
            "testproject",
            "--project",
            "test123",
            "--parent-project-path",
            "abcdef",
            "--embedded-datasources",
        ]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
