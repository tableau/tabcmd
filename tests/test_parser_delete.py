import sys
import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.delete_parser import DeleteParser
from .common_setup import *

commandname = "delete"


class DeleteParserTestT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(
            commandname
        )
        DeleteParser.delete_parser(manager, mock_command)

    def test_delete_parser_no_object(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_delete_parser(self):
        mock_args = [commandname, "ds", "-r", "proj"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.name == "ds", args
        assert args.projectname == "proj", args

    def test_delete_parser_missing_args(self):
        mock_args = [commandname, "--datasource"]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
