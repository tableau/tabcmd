import unittest
try:
    from unittest import mock
except ImportError:
    import mock
import argparse
import os 
import sys
from ..pythontabcmd2.parsers import create_group_parser
create_group_command_class = create_group_parser.CreateGroupParser

class CreateGroupParserTest(unittest.TestCase):
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace())
    def test_create_group_parser_missing_required_name(self, mock_args):
        with self.assertRaises(AttributeError):
            create_group_object = create_group_command_class()
            name = create_group_object.create_group_parser()

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name="testgroup"))
    def test_create_group_parser_required_name(self, mock_args):
        raises = False
        try: 
            create_group_object = create_group_command_class()
            name = create_group_object.create_group_parser()
        except:
            raises = True 
        self.assertFalse(raises, "Exception Raised")



if __name__ == "__main__":
    unittest.main()