import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.create_project_parser import CreateProjectParser


class CreateProjectParserTest(unittest.TestCase):

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name="testproject",
                                                parent_project_path="abcdef",
                                                description='desc',
                                                content_permission=None,
                                                server="https://localhost/",
                                                username="helloworld",
                                                site="",
                                                logging_level="info",
                                                password="testing123",
                                                no_prompt=True, token=None,
                                                token_name=None,
                                                cookie=True,
                                                no_cookie=False,
                                                prompt=False,
                                                ))
    def test_create_project_parser_optional_arguments(self, mock_args):
        args = CreateProjectParser.create_project_parser()
        assert args == argparse.Namespace(name="testproject",
                                          parent_project_path="abcdef",
                                          description='desc',
                                          content_permission=None,
                                          server="https://localhost/",
                                          username="helloworld",
                                          site="",
                                          logging_level="info",
                                          password="testing123",
                                          no_prompt=True, token=None,
                                          token_name=None,
                                          cookie=True,
                                          no_cookie=False,
                                          prompt=False, ), args
        assert args.parent_project_path == "abcdef"

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace())
    def test_create_project_parser_required_arguments_name(self, mock_args):
        with self.assertRaises(Exception):
            args = CreateProjectParser.create_project_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    parent_project_path="abcdef",
                    description='desc',
                    content_permission=None,
                    server="https://localhost/",
                    username="helloworld",
                    site="",
                    logging_level="info",
                    password="testing123",
                    no_prompt=True, token=None,
                    token_name=None,
                    cookie=True,
                    no_cookie=False,
                    prompt=False,
                ))
    def test_create_project_parser_required_arguments_missing_name(self,
                                                                   mock_args):
        args = CreateProjectParser.create_project_parser()
        assert args != argparse.Namespace(name="testproject",
                                          parent_project_path="abcdef",
                                          description='desc',
                                          content_permission=None,
                                          server="https://localhost/",
                                          username="helloworld",
                                          site="",
                                          logging_level="info",
                                          password="testing123",
                                          no_prompt=True, token=None,
                                          token_name=None,
                                          cookie=True,
                                          no_cookie=False,
                                          prompt=False, ), args
        assert args.parent_project_path == "abcdef"

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    parent_project_path="abcdef",
                    description='desc',
                    content_permission=None,
                    server="https://localhost/",
                    username="helloworld",
                    site="",
                    logging_level="info",
                    password="testing123",
                    no_prompt=True, token=None,
                    token_name=None,
                    cookie=True,
                    no_cookie=False,
                    prompt=False,
                ))
    def test_create_project_parser_required_arguments_missing_name(self,
                                                                   mock_args):
        args = CreateProjectParser.create_project_parser()
        assert args != argparse.Namespace(name="testproject",
                                          parent_project_path="abcdef",
                                          description='desc',
                                          content_permission=None,
                                          server="https://localhost/",
                                          username="helloworld",
                                          site="",
                                          logging_level="info",
                                          password="testing123",
                                          no_prompt=True, token=None,
                                          token_name=None,
                                          cookie=True,
                                          no_cookie=False,
                                          prompt=False, ), args
        assert args.parent_project_path == "abcdef"

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    description='desc',
                    parent_project_path=None,
                    content_permission=None,
                    server="https://localhost/",
                    username="helloworld",
                    site="",
                    logging_level="info",
                    password="testing123",
                    no_prompt=True, token=None,
                    token_name=None,
                    cookie=True,
                    no_cookie=False,
                    prompt=False,
                ))
    def test_create_project_parser_optional_arguments_missing_project_path(
            self, mock_args):
        args = CreateProjectParser.create_project_parser()
        assert args != argparse.Namespace(name="testproject",
                                          parent_project_path=None,
                                          description='desc',
                                          content_permission=None,
                                          server="https://localhost/",
                                          username="helloworld",
                                          site="",
                                          logging_level="info",
                                          password="testing123",
                                          no_prompt=True, token=None,
                                          token_name=None,
                                          cookie=True,
                                          no_cookie=False,
                                          prompt=False, ), args
        assert args.parent_project_path is None
