import unittest
try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from pythontabcmd2.parsers.create_project_parser import CreateProjectParser

class CreateProjectParserTest(unittest.TestCase):

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name= "testproject", parent_project_path="abcdef", description=None, content_permission=None))
    def test_create_project_parser_optional_arguments(self, mock_args):
        create_project_object = CreateProjectParser()
        args, parent_proj_path = create_project_object.create_project_parser()
        assert args == argparse.Namespace(content_permission=None, description=None, name='testproject', parent_project_path='abcdef')
        assert parent_proj_path == "abcdef"

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name= "testproject", parent_project_path="abcdef", description="this is a test desc", content_permission=None))
    def test_create_project_parser_optional_arguments_description(self, mock_args):
        create_project_object = CreateProjectParser()
        args, parent_proj_path = create_project_object.create_project_parser()
        assert args == argparse.Namespace(content_permission=None, description="this is a test desc", name='testproject', parent_project_path='abcdef')
        assert parent_proj_path == "abcdef"

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name= "testproject", parent_project_path="abcdef", description=None, content_permission="perm"))
    def test_create_project_parser_optional_arguments_description(self, mock_args):
        create_project_object = CreateProjectParser()
        args, parent_proj_path = create_project_object.create_project_parser()
        assert parent_proj_path == "abcdef"
        assert args == argparse.Namespace(name= "testproject", parent_project_path="abcdef", description=None, content_permission="perm")

