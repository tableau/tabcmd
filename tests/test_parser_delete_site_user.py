import sys
import unittest

try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from tabcmd.parsers.delete_site_users_parser import DeleteSiteUsersParser
from .common_setup import *

commandname = "deletesiteusers"


class DeleteSiteUsersParserTest(unittest.TestCase):
    csv = ("testname", "testpassword", "test", "test", "test", "test")

    @classmethod
    def setUpClass(cls):
        cls.parser_under_test, manager, mock_command = initialize_test_pieces(
            commandname
        )
        DeleteSiteUsersParser.delete_site_users_parser(manager, mock_command)

    def test_delete_site_user_parser(self):
        with mock.patch("builtins.open", mock.mock_open(read_data="test")) as open_file:
            mock_args = [commandname, "users.csv"]
            args = self.parser_under_test.parse_args(mock_args)
            open_file.assert_called_with("users.csv", "r", -1, "UTF-8", None)

    def test_delete_site_user_parser_missing_arguments(self):
        mock_args = [commandname]
        with self.assertRaises(SystemExit):
            args = self.parser_under_test.parse_args(mock_args)
