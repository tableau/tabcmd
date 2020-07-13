
import unittest
try:
    from unittest import mock
except ImportError:
    import mock
import argparse
import os 
import sys

from tabcmd2.pythontabcmd2 import session
session_class = session.Session


class SessionTest(unittest.TestCase):
    @mock.patch('tabcmd2.pythontabcmd2.session.Session.create_session')
    def test_create_project_parser(self, mock_args):
        mock_obj = mock.Mock()
        mock_obj.create_session()
        mock_obj.create_session.assert_called_with()

    @mock.patch('tabcmd2.pythontabcmd2.session.Session.create_session')
    def test_create_project_parser_exception(self, mock_args):
        mock_obj = mock.Mock()
        ServerResponseError = Exception
        mock_args.side_effect = ServerResponseError
        with self.assertRaises(ServerResponseError) as mock_error:
            Session.create_session()

    @mock.patch('tabcmd2.pythontabcmd2.session.Session.pickle_auth_objects')
    def test_pickle_auth_objects(self, mock_args):
        mock_obj = mock.Mock()
        mock_obj.pickle_auth_objects()
        mock_obj.pickle_auth_objects.assert_called_with()


if __name__ == "__main__":
    unittest.main()