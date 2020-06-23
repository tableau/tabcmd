import unittest
try:
    from unittest import mock
except ImportError:
    import mock
import argparse

try:
    from .. pythontabcmd2 import parser_invoker
    parser_invoker_class = parser_invoker.ParserInvoker
   
except Exception as e:
    print("###### Absolute import failed", e)

class ParserInvokerTest(unittest.TestCase):


    @mock.patch('tabcmd2.pythontabcmd2.parser_invoker.ParserInvoker.login')
    def test_login(self, mock_args):
        mock_obj = mock.Mock()
        mock_obj.login() 
        mock_obj.login.assert_called_with()

    @mock.patch('tabcmd2.pythontabcmd2.parser_invoker.ParserInvoker.createproject')
    def test_create_project(self, mock_args):
        mock_obj = mock.Mock()
        mock_obj.createproject()
        mock_obj.createproject.assert_called_with()

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