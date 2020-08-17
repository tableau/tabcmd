# @mock.patch('argparse.ArgumentParser.parse_args',
#                 return_value=(argparse.Namespace(role="Unlicensed",
#                                                  username="test",
#                                                  password="testpass",
#                                                  server="http://test")))
#     def test_create_site_parser_file(self, mock_args):
#         fake_file = mock.Mock()
#         fake_file.__iter__.return_value = ["data.csv"]
#         with mock.patch('builtins.open', create=True, return_value=fake_file):
#             sys.argv = ["test_csv.csv", "test", "test1", "test2"]
#             csv_lines, args = CreateSiteUsersParser.create_site_user_parser()
#             args_from_command = vars(args)
#             args_from_mock = vars(mock_args.return_value)
#             self.assertEqual(args_from_command, args_from_mock)
