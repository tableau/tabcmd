import unittest
from unittest import mock
from tabcmd.parsers.create_group_parser import CreateGroupParser
from .common_setup import *

commandname = "creategroup"


class CreateGroupParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(commandname)
        CreateGroupParser.create_group_parser(manager, mock_command)

    def test_creategroup_parser_required_name(self):
        mock_args = [commandname, "name"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.name == "name"

    def test_creategroup_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            self.parser_under_test.parse_args(mock_args)
