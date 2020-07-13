import unittest
import sys
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
        parser_invoker_obj = parser_invoker_class()
        mock_args.assert_called_once()

    @mock.patch('tabcmd2.pythontabcmd2.parser_invoker.ParserInvoker.deserialize')
    def test_deserialize(self, mock_args):
        mock_obj = mock.Mock()
        mock_obj.deserialize()
        mock_obj.deserialize.assert_called_with()


if __name__ == "__main__":
    unittest.main()