import sys
import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from pythontabcmd2.parsers.delete_project_parser import DeleteProjectParser


class DeleteProjectParserTest(unittest.TestCase):

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name="helloworld",
                                                username="test",
                                                password="testpass",
                                                server="http://test",
                                                parent_project_path="/test/",
                                                site="helloworld"))
    def test_delete_project(self, mock_args):

        args, parent_project_path = DeleteProjectParser.delete_project_parser()
        assert parent_project_path == "test"
        assert args == mock_args.return_value


    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name=None,
                                                username="test",
                                                password="testpass",
                                                server="http://test",
                                                parent_project_path="/test/",
                                                site="helloworld"))
    def test_delete_project_required_name_none(self, mock_args):
        args, parent_project_path = DeleteProjectParser.delete_project_parser()
        assert parent_project_path == "test"
        assert args == mock_args.return_value
        assert args.name == mock_args.return_value.name


    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace())
    def test_delete_project_missing_args(self, mock_args):
        with self.assertRaises(AttributeError):
            args, path = DeleteProjectParser.delete_project_parser()
