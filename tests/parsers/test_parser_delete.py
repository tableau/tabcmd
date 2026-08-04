import unittest

from tabcmd.commands.datasources_and_workbooks.delete_command import DeleteCommand
from .common_setup import *

commandname = "delete"


class DeleteParserTest(ParserTest):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, DeleteCommand)

    def test_delete_parser_no_object_parses(self):
        # With Classic-parity support (positional name optional so `--workbook Name`
        # works), a bare `delete` now parses; the command-level check enforces that
        # a name arrived via either form.
        mock_args = [commandname]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.name is None, args
        assert args.workbook is False, args
        assert args.datasource is False, args

    def test_delete_parser(self):
        mock_args = [commandname, "ds", "-r", "proj"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.name == "ds", args
        assert args.project_name == "proj", args

    def test_delete_parser_bare_datasource_flag(self):
        # tabcmd 2 form: `delete "Name" --datasource`. Bare --datasource -> True.
        mock_args = [commandname, "ds", "--datasource"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.name == "ds", args
        assert args.datasource is True, args

    def test_delete_parser_classic_workbook_form(self):
        # Classic form: `delete --workbook "Name"`. The value is the target name.
        mock_args = [commandname, "--workbook", "MyWorkbook"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.workbook == "MyWorkbook", args

    def test_delete_parser_classic_datasource_form(self):
        mock_args = [commandname, "--datasource", "MyDatasource"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.datasource == "MyDatasource", args

    def test_delete_parser_mutually_exclusive_still_holds(self):
        # --workbook and --datasource are still mutually exclusive.
        mock_args = [commandname, "--workbook", "A", "--datasource", "B"]
        with self.assertRaises(SystemExit):
            self.parser_under_test.parse_args(mock_args)
