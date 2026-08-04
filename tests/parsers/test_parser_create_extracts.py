import unittest

from tabcmd.commands.extracts.create_extracts_command import CreateExtracts
from .common_setup import *

commandname = "createextracts"


class CreateExtractsParserTest(ParserTest):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, CreateExtracts)

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

    # --encrypt Classic-parity: accepts yes|no|true|false, bare flag still True, omitted False
    def _base_args(self):
        return [commandname, "--datasource", "ds", "--project", "p", "--parent-project-path", "pp"]

    def test_encrypt_omitted_is_false(self):
        args = self.parser_under_test.parse_args(self._base_args())
        assert args.encrypt is False, args

    def test_encrypt_bare_flag_is_true(self):
        args = self.parser_under_test.parse_args(self._base_args() + ["--encrypt"])
        assert args.encrypt is True, args

    def test_encrypt_yes_is_true(self):
        args = self.parser_under_test.parse_args(self._base_args() + ["--encrypt", "yes"])
        assert args.encrypt is True, args

    def test_encrypt_no_is_false(self):
        args = self.parser_under_test.parse_args(self._base_args() + ["--encrypt", "no"])
        assert args.encrypt is False, args

    def test_encrypt_true_is_true(self):
        args = self.parser_under_test.parse_args(self._base_args() + ["--encrypt", "true"])
        assert args.encrypt is True, args

    def test_encrypt_false_is_false(self):
        args = self.parser_under_test.parse_args(self._base_args() + ["--encrypt", "false"])
        assert args.encrypt is False, args

    def test_encrypt_case_insensitive(self):
        args = self.parser_under_test.parse_args(self._base_args() + ["--encrypt", "YES"])
        assert args.encrypt is True, args

    def test_encrypt_bad_value_rejected(self):
        with self.assertRaises(SystemExit):
            self.parser_under_test.parse_args(self._base_args() + ["--encrypt", "maybe"])
