import unittest
try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from pythontabcmd2.parsers.add_users_parser import AddUserParser


class AddUserParserTest(unittest.TestCase):
    pass

    # @mock.patch('argparse.ArgumentParser.parse_args',
    #             return_value=argparse.Namespace(file= "test.csv", group="testgroup"))
    # def test_create_user_parser_optional_arguments(self, mock_args):
    #     add_user_object = AddUserParser()
    #     file, args = add_user_object.add_user_parser()
    #     assert file == "test.csv"
    #     assert args == argparse.Namespace(file= "test.csv", group="testgroup")
