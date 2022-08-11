import unittest

from tabcmd.commands.datasources_and_workbooks.delete_command import DeleteCommand
from .common_setup import *

commandname = "delete"


class DeleteParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, DeleteCommand)

    def test_delete_parser_no_object(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_delete_parser(self):
        mock_args = [commandname, "ds", "-r", "proj"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.name == "ds", args
        assert args.project_name == "proj", args

    def test_delete_parser_missing_args(self):
        mock_args = [commandname, "--datasource"]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
