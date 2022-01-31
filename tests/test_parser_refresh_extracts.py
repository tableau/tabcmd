import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from pythontabcmd.parsers.refresh_extracts_parser \
    import RefreshExtractsParser


class RefreshExtractsParserTest(unittest.TestCase):

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(
                    username="helloworld",
                    site="",
                    logging_level="info",
                    password="testing123",
                    no_prompt=True, token=None,
                    token_name=None,
                    cookie=True,
                    no_cookie=False,
                    prompt=False,
                    datasource="hello",
                    incremental=True,
                    synchronous=True,
                    addcalculations=False,
                    removecalculations=True,
                    project="testproject",
                    url="testurl",
                    workbook="testworkbook"
                ))
    def test_refresh_extract_parser_optional_arguments(self, mock_args):
        args = RefreshExtractsParser.refresh_extracts_parser()
        assert args == argparse.Namespace(
            username="helloworld",
            site="",
            logging_level="info",
            password="testing123",
            no_prompt=True, token=None,
            token_name=None,
            cookie=True,
            no_cookie=False,
            prompt=False,
            datasource="hello",
            incremental=True,
            synchronous=True,
            addcalculations=False,
            removecalculations=True,
            project="testproject",
            url="testurl",
            workbook="testworkbook")

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace())
    def test_refresh_extract_parser_missing_all_args(self, mock_args):
        with self.assertRaises(AttributeError):
            args = RefreshExtractsParser \
                .refresh_extracts_parser()
