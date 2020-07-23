# import unittest
# try:
#     from unittest import mock
# except ImportError:
#     import mock
# import argparse
# from ..pythontabcmd2.parsers import delete_group_parser
# delete_group_command_class = delete_group_parser.DeleteGroupParser
#
# class DeleteGroupParserTest(unittest.TestCase):
#     @mock.patch('argparse.ArgumentParser.parse_args',
#                 return_value=argparse.Namespace())
#     def test_delete_group_parser_missing_required_name(self, mock_args):
#         with self.assertRaises(AttributeError):
#             delete_group_object = delete_group_command_class()
#             name = delete_group_object.delete_group_parser()
#
#     @mock.patch('argparse.ArgumentParser.parse_args',
#                 return_value=argparse.Namespace(name="testgroup"))
#     def test_delete_group_parser_required_name(self, mock_args):
#         raises = False
#         try:
#             delete_group_object = delete_group_command_class()
#             name = delete_group_object.delete_group_parser()
#         except:
#             raises = True
#         self.assertFalse(raises, "Exception Raised")
#
