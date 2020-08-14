# import unittest
# try:
#     from unittest import mock
# except ImportError:
#     import mock
# import argparse
# from pythontabcmd2.parsers.add_users_parser import AddUserParser
#
#
# class AddUserParserTest(unittest.TestCase):
#
#         @mock.patch('argparse.ArgumentParser.parse_args',
#                     return_value=argparse.Namespace(name="test"))
#         def test_create_group_parser_required_name(self, mock_args):
#             create_group_object = AddUserParser()
#             args = create_group_object.create_group_parser()
#             assert getattr(args, "name") == getattr(mock_args.return_value,
#                                                     "name")
#
#         @mock.patch('argparse.ArgumentParser.parse_args',
#                     return_value=argparse.Namespace())
#         def test_create_group_parser_missing_required_name(self, mock_args):
#             create_group_object = AddUserParser()
#             args = create_group_object.create_group_parser()
#             args_from_command = vars(args)
#             args_from_mock = vars(mock_args.return_value)
#             assert args_from_command == args_from_mock
