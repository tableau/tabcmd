import sys
import unittest

import argparse
from tabcmd.parsers.delete_group_parser import DeleteGroupParser
from common_setup import *

commandname = "deletegroup"


class DeleteGroupParserTestT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(commandname)
        DeleteGroupParser.delete_group_parser(manager, mock_command)

    def test_delete_group(self):
        mock_args = [commandname, "group-name"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.name == "group-name", args

    def test_delete_group_parser_required_name_missing(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
