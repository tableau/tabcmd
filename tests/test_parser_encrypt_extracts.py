import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from pythontabcmd2.parsers.encrypt_extracts_parser \
    import EncryptExtractsParser


class EncryptExtractsParserTest(unittest.TestCase):

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(datasource="testproject",
                                                parent_project_path="abcdef",
                                                embedded_datasources='desc',
                                                url="1234",
                                                encrypt=None,
                                                project="test123",
                                                workbook="workbooktest",
                                                include_all=
                                                "https://localhost/",
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
    def test_delete_extract_parser_optional_arguments(self, mock_args):
        args = EncryptExtractsParser.encrypt_extracts_parser()
        assert args == argparse.Namespace(datasource="testproject",
                                          parent_project_path="abcdef",
                                          embedded_datasources='desc',
                                          url="1234",
                                          encrypt=None,
                                          project="test123",
                                          workbook="workbooktest",
                                          include_all=
                                          "https://localhost/",
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
                return_value=argparse.Namespace())
    def test_delete_extract_parser_missing_all_args(self, mock_args):
        with self.assertRaises(AttributeError):
            args = DeleteExtractsParser.delete_extracts_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(datasource="testproject",
                                                embedded_datasources='desc',
                                                url="1234",
                                                encrypt=None,
                                                project="test123",
                                                workbook="workbooktest",
                                                include_all=
                                                "https://localhost/",
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
    def test_delete_extract_parser_missing_project_path(self, mock_args):
        args = DeleteExtractsParser.delete_extracts_parser()
        with self.assertRaises(AssertionError):
            assert args != argparse.Namespace(datasource="testproject",
                                              embedded_datasources='desc',
                                              url="1234",
                                              encrypt=None,
                                              project="test123",
                                              workbook="workbooktest",
                                              include_all=
                                              "https://localhost/",
                                              username="helloworld",
                                              site="",
                                              logging_level="info",
                                              password="testing123",
                                              no_prompt=True, token=None,
                                              token_name=None,
                                              cookie=True,
                                              no_cookie=False,
                                              prompt=False)
