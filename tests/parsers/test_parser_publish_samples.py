import unittest

from tabcmd.commands.project.publish_samples_command import PublishSamplesCommand
from .common_setup import *

commandname = "publishsamples"


class PublishSamplesParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, PublishSamplesCommand)

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
