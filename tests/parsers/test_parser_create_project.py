import unittest

from tabcmd.commands.project.create_project_command import CreateProjectCommand
from .common_setup import *

commandname = "createproject"


class CreateProjectParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser_under_test = initialize_test_pieces(commandname, CreateProjectCommand)

    def test_create_project_parser_optional_arguments(self):
        mock_args = [
            commandname,
            "--name",
            "testproject",
            "--parent-project-path",
            "abcdef",
            "--description",
            "desc",
        ]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.project_name == "testproject"
        assert args.parent_project_path == "abcdef"

    def test_create_project_parser_required_arguments_name(self):
        mock_args = [
            commandname,
            "-n",
            "project-name",
            "--parent-project-path",
            "abcdef",
            "--description",
            "desc",
        ]
        args = self.parser_under_test.parse_args(mock_args)
        assert args.project_name == "project-name"
        assert args.parent_project_path == "abcdef"

    def test_create_project_parser_required_arguments_missing_name(self):
        mock_args = [
            commandname,
            "--parent-project-path",
            "abcdef",
            "--description",
            "desc",
        ]
        with self.assertRaises(SystemExit):
            self.parser_under_test.parse_args(mock_args)

    def test_create_project_parser_optional_arguments_missing_project_path(self):
        mock_args = [
            commandname,
            "-n",
            "project-name",
            "--parent-project-path",
            "--description",
            "desc",
        ]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
