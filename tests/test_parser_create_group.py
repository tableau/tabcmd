import unittest
try:
    from unittest import mock
except ImportError:
    import mock
import argparse
from pythontabcmd2.parsers.create_group_parser import CreateGroupParser


class CreateGroupParserTest(unittest.TestCase):
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(args="test"))
    def test_create_group_parser_missing_required_name(self, mock_args):
        create_group_object = CreateGroupParser()
        group_name = create_group_object.create_group_parser()
        assert group_name == argparse.Namespace(args='test')

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=argparse.Namespace(name="testgroup"))
    def test_create_group_parser_required_name(self, mock_args):
        raises = False
        try:
            create_group_object = CreateGroupParser()
            name = create_group_object.create_group_parser()
        except Exception:
            raises = True
        self.assertFalse(raises, "Exception Raised")
