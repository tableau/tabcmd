import unittest
from tabcmd.parsers.delete_project_parser import DeleteProjectParser
from .common_setup import *

commandname = 'deleteproject'


class DeleteProjectParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(commandname)
        DeleteProjectParser.delete_project_parser(manager, mock_command)

    def test_delete_project(self):
        mock_args = [commandname, 'project', '--parent-project-path', 'p']
        args = self.parser_under_test.parse_args(mock_args)
        assert args.parent_project_path == "p"

    def test_delete_project_required_name_none(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
