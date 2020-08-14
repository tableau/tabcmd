import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from pythontabcmd2.parsers.create_project_parser import CreateProjectParser


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
        args, parent_proj_path = CreateProjectParser.create_project_parser()
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
                                          prompt=False, )
        assert parent_proj_path == "abcdef"

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace())
    def test_create_project_parser_required_arguments_name(self, mock_args):
        raises = False
        try:
            args, parent_proj_path = CreateProjectParser.create_project_parser()
        except Exception:
            raises = True
        self.assertTrue(raises, True)

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
        args, parent_proj_path = CreateProjectParser.create_project_parser()
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
                                          prompt=False, )
        assert parent_proj_path == "abcdef"

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
        args, parent_proj_path = CreateProjectParser.create_project_parser()
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
                                          prompt=False, )
        assert parent_proj_path == "abcdef"

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
        args, parent_proj_path = CreateProjectParser.create_project_parser()
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
                                          prompt=False, )
        assert parent_proj_path is None
