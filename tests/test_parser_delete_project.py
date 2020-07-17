import unittest
try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from ..pythontabcmd2.parsers import delete_project_parser
delete_project_parser_class = delete_project_parser.DeleteProjectParser


class DeleteProjectParserTest(unittest.TestCase):
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace())
    def test_delete_project_parser_missing_required_name(self, mock_args):
        with self.assertRaises(AttributeError):
            delete_project_object = delete_project_parser_class()
            name = delete_project_object.delete_project_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name="testproject", parent_project_path=None))
    def test_delete_project_parser_required_name(self, mock_args):
        raises = False
        try:
            delete_project_object = delete_project_parser_class()
            name = delete_project_object.delete_project_parser()
        except:
            raises = True
        self.assertFalse(raises, "Exception Raised")

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name="testproject", parent_project_path="abcdef"))
    def test_delete_project_parser_optional_arguments_parent_path(self, mock_args):
        delete_project_object = delete_project_parser_class()
        name, parent_proj_path = delete_project_object.delete_project_parser()
        assert name == "testproject"
        assert parent_proj_path == "abcdef"

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name="testproject", parent_project_path=None))
    def test_delete_project_parser_optional_arguments_parent_path_None(self, mock_args):
        delete_project_object = delete_project_parser_class()
        name, parent_proj_path = delete_project_object.delete_project_parser()
        assert name == "testproject"
        assert parent_proj_path == None

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name="hello"))
    def test_delete_project_parser_missing_path(self, mock_args):
        with self.assertRaises(AttributeError):
            delete_project_object = delete_project_parser_class()
            name = delete_project_object.delete_project_parser()
