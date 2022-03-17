import unittest

import argparse
from tabcmd.parsers.publish_samples_parser import PublishSamplesParser
from .common_setup import *

commandname = "publishsamples"


class PublishParserParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(commandname)
        PublishSamplesParser.publish_samples_parser(manager, mock_command)

    def test_publish_samples_parser_name(self):
        mock_args = [commandname, "-n", "project"]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.project_name == "project", args

    def test_publish_samples_parser_missing_all_args(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)

    def test_publish_samples_parser_optional_args(self):
        mock_args = [
            commandname,
            "--name",
            "project",
            "--parent-project-path",
            "parent",
        ]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.parent_project_path == "parent", args
        assert args.project_name == "project", args
