import unittest
from unittest import mock
from tabcmd.parsers.publish_parser import PublishParser
from .common_setup import *

commandname = "Publish"


class PublishParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(commandname)
        PublishParser.publish_parser(manager, mock_command)

    def test_publish_parser_required_name(self):
        mock_args = [commandname, "filename.hyper"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.filename == "filename.hyper", args

    def test_publish_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_publish_parser_tabbed(self):
        mock_args = [commandname, "filename.twbx", "--tabbed"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.tabbed is True, args
