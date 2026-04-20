import logging
import unittest
import tableauserverclient as TSC
from ..assets import mock_data
from unittest.mock import *
from unittest import mock
from tabcmd.commands.datasources_and_workbooks.publish_command import PublishCommand
from tabcmd.commands.datasources_and_workbooks import publish_command

from ..assets.mock_data import set_up_mock_args, set_up_mock_file, set_up_mock_path, set_up_mock_server

mock_args = set_up_mock_args()
mock_logger = mock.MagicMock()


# mock the module as it is imported *when used*
@patch("tabcmd.commands.datasources_and_workbooks.publish_command.Session", autospec=True)
@patch("tabcmd.commands.datasources_and_workbooks.publish_command.glob.glob", return_value=["one.twbx", "two.hyper"])
@patch("tabcmd.commands.datasources_and_workbooks.publish_command.os.path", autospec=True)
class PublishCommandTests(unittest.TestCase):
    def test_publish(self, mock_path, mock_glob, mock_session):
        # TODO move to init method
        set_up_mock_server(mock_session)
        mock_path = set_up_mock_path(mock_path)

        mock_args.overwrite = False
        mock_args.filename = "existing_file.twbx"
        mock_args.project_name = "project-name"
        mock_args.parent_project_path = "projects"
        mock_args.name = ""
        mock_args.tabbed = True
        mock_args.db_username = None
        mock_args.oauth_username = None
        mock_args.append = False
        mock_args.replace = False
        mock_args.thumbnail_username = None
        mock_args.thumbnail_group = None
        mock_args.skip_connection_check = False
        PublishCommand.run_command(mock_args)
        mock_session.internal_server.workbooks.publish.assert_called()

    def test_publish_with_creds(self, mock_path, mock_glob, mock_session):
        set_up_mock_server(mock_session)
        mock_path = set_up_mock_path(mock_path)

        mock_args.overwrite = False
        mock_args.append = True
        mock_args.replace = False

        mock_args.filename = "existing_file.twbx"
        mock_args.project_name = "project-name"
        mock_args.parent_project_path = "projects"
        mock_args.name = ""
        mock_args.tabbed = True

        mock_args.db_username = "username"
        mock_args.db_password = "oauth_u"
        mock_args.save_db_password = True
        mock_args.oauth_username = None
        mock_args.embed = False

        mock_args.thumbnail_username = None
        mock_args.thumbnail_group = None
        mock_args.skip_connection_check = False

        PublishCommand.run_command(mock_args)
        mock_session.internal_server.workbooks.publish.assert_called()

    def test_get_files_to_publish_twbx(self, mock_path, mock_glob, mock_session):
        set_up_mock_server(mock_session)
        mock_path = set_up_mock_path(mock_path)
        mock_args.filename = "existing.twbx"
        expected = ["existing.twbx"]
        actual = PublishCommand.get_files_to_publish(mock_args, logging)
        assert actual == expected

    # if the filename given is a directory, publish all relevant files in the directory to the server
    def test_get_files_to_publish_folder(self, mock_path, mock_glob, mock_session):
        set_up_mock_server(mock_session)
        mock_path = set_up_mock_path(mock_path)
        mock_path.isfile = lambda x: False  # this time it is a directory

        mock_args.filename = "directory"
        mock_args.filetype = None
        expected = ["directory/one.twbx", "directory/two.hyper"]
        actual = PublishCommand.get_files_to_publish(mock_args, logging)
        assert actual == expected

    def test_default_publish_mode(self, mock_path, mock_glob, mock_session):
        mock_args.replace = False
        mock_args.append = False
        mock_args.overwrite = False

        publish_mode = publish_command.PublishCommand.get_publish_mode(mock_args, mock_logger)
        self.assertEqual(publish_mode, TSC.Server.PublishMode.CreateNew)

    def test_replace_publish_mode(self, mock_path, mock_glob, mock_session):
        mock_args.replace = True
        mock_args.append = False
        mock_args.overwrite = False

        publish_mode = publish_command.PublishCommand.get_publish_mode(mock_args, mock_logger)
        self.assertEqual(publish_mode, TSC.Server.PublishMode.Replace)

    def test_append_publish_mode(self, mock_path, mock_glob, mock_session):
        mock_args.replace = False
        mock_args.append = True
        mock_args.overwrite = False

        publish_mode = publish_command.PublishCommand.get_publish_mode(mock_args, mock_logger)
        self.assertEqual(publish_mode, TSC.Server.PublishMode.Append)

    def test_overwrite_publish_mode(self, mock_path, mock_glob, mock_session):
        mock_args.replace = False
        mock_args.append = False
        mock_args.overwrite = True

        publish_mode = publish_command.PublishCommand.get_publish_mode(mock_args, mock_logger)
        self.assertEqual(publish_mode, TSC.Server.PublishMode.Overwrite)

    def test_invalid_combination_of_modes(self, mock_path, mock_glob, mock_session):
        mock_args.replace = True
        mock_args.append = True
        mock_args.overwrite = False

        with self.assertRaises(SystemExit):
            publish_command.PublishCommand.get_publish_mode(mock_args, mock_logger)
