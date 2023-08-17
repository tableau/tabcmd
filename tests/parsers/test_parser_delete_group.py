import unittest

from tabcmd.commands.group.delete_group_command import DeleteGroupCommand
from .common_setup import *

commandname = "deletegroup"


class DeleteGroupParserTestT(ParserTestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, DeleteGroupCommand)

    def test_delete_group(self):
        mock_args = [commandname, "group-name"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.name == "group-name", args

    def test_delete_group_parser_required_name_missing(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
