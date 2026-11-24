import unittest

from tabcmd.commands.group.create_group_command import CreateGroupCommand
from .common_setup import *

commandname = "creategroup"


class CreateGroupParserTest(ParserTest):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, CreateGroupCommand)

    def test_creategroup_parser_required_name(self):
        mock_args = [commandname, "name"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.name == "name"

    def test_creategroup_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            self.parser_under_test.parse_args(mock_args)

    def test_creategroup_parser_role_flag(self):
        args = self.parser_under_test.parse_args([commandname, "name", "--role", "Viewer"])
        assert args.role == "Viewer"

    def test_creategroup_parser_role_short_flag(self):
        args = self.parser_under_test.parse_args([commandname, "name", "-r", "Explorer"])
        assert args.role == "Explorer"

    def test_creategroup_parser_role_case_insensitive(self):
        args = self.parser_under_test.parse_args([commandname, "name", "--role", "creator"])
        assert args.role == "Creator"

    def test_creategroup_parser_role_optional(self):
        args = self.parser_under_test.parse_args([commandname, "name"])
        assert args.role is None
