import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.decrypt_extracts_parser \
    import DecryptExtractsParser


class DecryptExtractsParserTest(unittest.TestCase):

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(site_name="hellohello",
                                                username="helloworld",
                                                site="",
                                                logging_level="info",
                                                password="testing123",
                                                no_prompt=True, token=None,
                                                token_name=None,
                                                cookie=True,
                                                no_cookie=False,
                                                prompt=False
                                                ))
    def test_decrypt_extract_parser_optional_arguments(self, mock_args):
        args = DecryptExtractsParser.decrypt_extracts_parser()
        assert args == argparse.Namespace(site_name="test1", #reading from sys.argv
                                          username="helloworld",
                                          site="",
                                          logging_level="info",
                                          password="testing123",
                                          no_prompt=True,
                                          token=None,
                                          token_name=None,
                                          cookie=True,
                                          no_cookie=False,
                                          prompt=False, ), args

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace())
    def test_decrypt_extract_parser_missing_all_args(self, mock_args):
        with self.assertRaises(AttributeError):
            args = DecryptExtractsParser.decrypt_extracts_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(site_name=None,
                                                username="helloworld",
                                                site="",
                                                logging_level="info",
                                                password="testing123",
                                                no_prompt=True, token=None,
                                                token_name=None,
                                                cookie=True,
                                                no_cookie=False,
                                                prompt=False
                                                ))
    def test_decrypt_extract_parser_missing_site_name(self, mock_args):
        args = DecryptExtractsParser.decrypt_extracts_parser()
        with self.assertRaises(AssertionError):
            assert args == argparse.Namespace(site_name=None,
                                              username="helloworld",
                                              site="",
                                              logging_level="info",
                                              password="testing123",
                                              no_prompt=True, token=None,
                                              token_name=None,
                                              cookie=True,
                                              no_cookie=False,
                                              prompt=False)
