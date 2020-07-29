# import unittest
# try:
#     from unittest import mock
# except ImportError:
#     import mock
# import argparse
# from ..pythontabcmd2.parsers import create_users_parser
# create_user_command_class = create_users_parser.CreateUserParser
#
#
# class CreateUserParserTest(unittest.TestCase):
#     @mock.patch('argparse.ArgumentParser.parse_args',
#                 return_value=argparse.Namespace())
#     def test_create_user_parser_missing_required_name(self, mock_args):
#         with self.assertRaises(AttributeError):
#             create_user_object = create_user_command_class()
#             csv_files = create_user_object.create_user_parser()
#
#     @mock.patch('argparse.ArgumentParser.parse_args',
#                 return_value=argparse.Namespace(file= "test.csv"))
#     def test_create_project_parser_optional_arguments(self, mock_args):
#         create_user_object = create_user_command_class()
#         file = create_user_object.create_user_parser()
#         assert file == "test.csv"
