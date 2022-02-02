import unittest
import sys

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.create_extracts_parser import CreateExtractsParser


class CreateExtractsParserTest(unittest.TestCase):

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace())
    def test_create_extract_parser_missing_all_args(self, mock_args):
        with self.assertRaises(AttributeError):
            args = CreateExtractsParser.create_extracts_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(datasource="testproject",
                                                embedded_datasources='desc',
                                                url="1234",
                                                encrypt=None,
                                                project="test123",
                                                workbook="workbooktest",
                                                include_all="test",
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
    def test_create_extract_parser_missing_project_path(self, mock_args):
        args = CreateExtractsParser.create_extracts_parser()
        with self.assertRaises(AssertionError):
            assert args != argparse.Namespace(datasource="testproject",
                                              embedded_datasources='desc',
                                              url="1234",
                                              encrypt=None,
                                              project="test123",
                                              workbook="workbooktest",
                                              include_all="test",
                                              username="helloworld",
                                              site="",
                                              logging_level="info",
                                              password="testing123",
                                              no_prompt=True, token=None,
                                              token_name=None,
                                              cookie=True,
                                              no_cookie=False,
                                              prompt=False)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(datasource="testproject",
                                                parent_project_path="abcdef",
                                                embedded_datasources='desc',
                                                url="1234",
                                                encrypt=None,
                                                project="test123",
                                                workbook="workbooktest",
                                                include_all="test",
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
    def test_create_extract_parser_optional_arguments(self, mock_args):
        args = CreateExtractsParser.create_extracts_parser()
        assert args == argparse.Namespace(datasource="testproject",
                                          parent_project_path="abcdef",
                                          embedded_datasources='desc',
                                          url="1234",
                                          encrypt=None,
                                          project="test123",
                                          workbook="workbooktest",
                                          include_all="test",
                                          username="helloworld",
                                          site="",
                                          logging_level="info",
                                          password="testing123",
                                          no_prompt=True, token=None,
                                          token_name=None,
                                          cookie=True,
                                          no_cookie=False,
                                          prompt=False)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(datasource="testproject",
                                                embedded_datasources='desc',
                                                url="1234",
                                                project="test123",
                                                workbook="workbooktest",
                                                include_all="test",
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
    def test_create_extract_parser_missing_encrypt(self, mock_args):
        args = CreateExtractsParser.create_extracts_parser()
        with self.assertRaises(AssertionError):
            assert args != argparse.Namespace(datasource="testproject",
                                              embedded_datasources='desc',
                                              url="1234",
                                              project="test123",
                                              workbook="workbooktest",
                                              include_all="test",
                                              username="helloworld",
                                              site="",
                                              logging_level="info",
                                              password="testing123",
                                              no_prompt=True, token=None,
                                              token_name=None,
                                              cookie=True,
                                              no_cookie=False,
                                              prompt=False)

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(datasource="testproject",
                                                embedded_datasources='desc',
                                                url="1234",
                                                project="test123",
                                                workbook="workbooktest",
                                                include_all="test",
                                                site="helloworld"
                                                ))
    def test_create_extract_parser_missing_login(self, mock_args):
        args = CreateExtractsParser.create_extracts_parser()
        with self.assertRaises(AssertionError):
            assert args == argparse.Namespace(datasource="testproject",
                                              embedded_datasources='desc',
                                              url="1234",
                                              project="test123",
                                              workbook="workbooktest",
                                              include_all="test")

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(datasource="testproject",
                                                embedded_datasources='desc',
                                                url="1234",
                                                project="test123",
                                                workbook="workbooktest",
                                                include_all="test",
                                                site="helloworld"
                                                ))
    def test_create_extract_parser_missing_workbook(self, mock_args):
        args = CreateExtractsParser.create_extracts_parser()
        with self.assertRaises(AssertionError):
            assert args == argparse.Namespace(datasource="testproject",
                                              embedded_datasources='desc',
                                              url="1234",
                                              project="test123",
                                              include_all="test")

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(datasource="testproject",
                                                embedded_datasources='desc',
                                                url="1234",
                                                project="test123",
                                                workbook="workbooktest",
                                                include_all="test",
                                                site="helloworld"
                                                ))
    def test_create_extract_parser_missing_datasource(self, mock_args):
        args = CreateExtractsParser.create_extracts_parser()
        with self.assertRaises(AssertionError):
            assert args == argparse.Namespace(
                embedded_datasources='desc',
                url="1234",
                project="test123",
                include_all="test")

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(datasource="testproject",
                                                encrypt="encrypt",
                                                embedded_datasources='desc',
                                                url="1234",
                                                project="test123",
                                                workbook="workbooktest",
                                                include_all="test",
                                                site="helloworld"
                                                ))
    def test_create_extract_parser_missing_encypt(self, mock_args):
        args = CreateExtractsParser.create_extracts_parser()
        with self.assertRaises(AssertionError):
            assert args == argparse.Namespace(
                embedded_datasources='desc',
                url="1234",
                project="test123",
                include_all="test")

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(datasource="testproject",
                                                encrypt="encrypt",
                                                embedded_datasources='desc',
                                                url="1234",
                                                project="test123",
                                                workbook="workbooktest",
                                                include_all="test",
                                                site="helloworld"
                                                ))
    def test_create_extract_parser_missing_embedded_datasources(self,
                                                                mock_args):
        args = CreateExtractsParser.create_extracts_parser()
        with self.assertRaises(AssertionError):
            assert args == argparse.Namespace(
                url="1234",
                project="test123",
                include_all="test")
