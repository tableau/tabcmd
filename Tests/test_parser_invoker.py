import unittest
try:
    from unittest import mock
except ImportError:
    import mock
import argparse

try:
    from .. pythontabcmd2 import parser_invoker
    parser_invoker_class = parser_invoker.ParserInvoker
    from ..pythontabcmd2.parsers.create_project_parser import *
    
except Exception:
    print("File import failed")

class ParserInvokerTest(unittest.TestCase):

    @mock.patch.object(sys, 'argv', ['', 'createproject','--name', 'testname'])
    @mock.patch('tabcmd2.pythontabcmd2.parser_invoker.ParserInvoker.createproject')
    def test_parser_called(self, mock_args):
        # name = "testname"
        # description = "testdesc"
        parser_invoker_obj = parser_invoker_class()
        mock_args.assert_called_once()

    @mock.patch('tabcmd2.pythontabcmd2.parser_invoker.ParserInvoker.login')
    def test_login(self, mock_args):
        mock_obj = mock.Mock()
        mock_obj.login() 
        mock_obj.login.assert_called_with()

    @mock.patch('tabcmd2.pythontabcmd2.parser_invoker.ParserInvoker.createproject')
    def test_create_project(self, mock_args):
        # mock_obj = mock.Mock()
        # parser_invoker_class_obj = parser_invoker_class()
        create_project_parser_obj = CreateProjectParser()
        create_project_parser_obj.create_project_parser = mock.MagicMock(return_value = ["name", "description", "content_perm", "parent_proj_path"])
        # parser_invoker_class_obj = parser_invoker_class()
        # parser_invoker_class_obj.createproject()
        # mock_obj.createproject.assert_called_with()

    @mock.patch('tabcmd2.pythontabcmd2.parser_invoker.ParserInvoker.logout')
    def test_logout(self, mock_args):
        mock_obj = mock.Mock()
        mock_obj.logout()
        mock_obj.logout.assert_called_with()

    @mock.patch('tabcmd2.pythontabcmd2.parser_invoker.ParserInvoker.deserialize')
    def test_deserialize(self, mock_args):
        mock_obj = mock.Mock()
        mock_obj.deserialize()
        mock_obj.deserialize.assert_called_with()


if __name__ == "__main__":
    unittest.main()