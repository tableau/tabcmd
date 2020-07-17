import unittest
try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from ..pythontabcmd2.parsers import login_parser
login_parser_class = login_parser.LoginParser


class CreateProjectParserTest(unittest.TestCase):
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(site="https://localhost", 
                                                token="abcdef", username=None, token_name="test" ))
    def test_login_parser_missing_required_server(self, mock_args):

        with self.assertRaises(AttributeError):
            login_parser_object = login_parser_class()
            username, password, site, server, token_name, token = login_parser_object.login_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(site="https://localhost", server="test.com",
                                                token="abcdef", username=None, token_name="test" ))
    def test_login_parser_optional_arguments(self, mock_args):

       
        login_parser_object = login_parser_class()
        username, password, site, server, token_name, token = login_parser_object.login_parser()
        assert site == "https://localhost"
        assert token == "abcdef"
        assert username == None
        assert token_name == "test"
        assert server == "test.com"
        
# if __name__ == "__main__":
#     unittest.main()
