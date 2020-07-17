import unittest
try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from ..pythontabcmd2.parsers import create_project_parser
create_project_command_class = create_project_parser.CreateProjectParser


class CreateProjectParserTest(unittest.TestCase):
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(parent_project_path="abcdef", description=None, content_permission=None))
    def test_create_project_parser_missing_required_name(self, mock_args):
        with self.assertRaises(AttributeError):
            create_project_object = create_project_command_class()
            name, description, content_perm, parent_proj_path = create_project_object.create_project_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name= "testproject", parent_project_path="abcdef", description=None, content_permission=None))
    def test_create_project_parser_optional_arguments(self, mock_args):
        create_project_object = create_project_command_class()
        name, description, content_perm, parent_proj_path = create_project_object.create_project_parser()
        assert name == "testproject"
        assert description == None
        assert content_perm == None
        assert parent_proj_path == "abcdef"

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name= "testproject", parent_project_path="abcdef", description="this is a test desc", content_permission=None))
    def test_create_project_parser_optional_arguments_description(self, mock_args):
        create_project_object = create_project_command_class()
        name, description, content_perm, parent_proj_path = create_project_object.create_project_parser()
        assert name == "testproject"
        assert description == "this is a test desc"
        assert content_perm == None
        assert parent_proj_path == "abcdef"

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name= "testproject", parent_project_path="abcdef", description=None, content_permission="perm"))
    def test_create_project_parser_optional_arguments_description(self, mock_args):
        create_project_object = create_project_command_class()
        name, description, content_perm, parent_proj_path = create_project_object.create_project_parser()
        assert name == "testproject"
        assert description == None
        assert content_perm == "perm"
        assert parent_proj_path == "abcdef"

# if __name__ == "__main__":
#     unittest.main()
