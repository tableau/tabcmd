import argparse
import unittest
from unittest.mock import *
import tableauserverclient as TSC

from tabcmd.commands.auth import login_command
from tabcmd.commands.datasources_and_workbooks import delete_command, export_command, get_url_command, publish_command


from typing import List, NamedTuple, TextIO, Union
import io

mock_args = argparse.Namespace()

fake_item = MagicMock()
fake_item.name = "fake-name"
fake_item.id = "fake-id"
fake_item.pdf = b"/pdf-representation-of-view"
fake_item.extract_encryption_mode = "Disabled"

fake_item_pagination = MagicMock()
fake_item_pagination.page_number = 1
fake_item_pagination.total_available = 1
fake_item_pagination.page_size = 100

fake_job = MagicMock()
fake_job.id = "fake-job-id"

creator = MagicMock()
getter = MagicMock()
getter.get = MagicMock("get", return_value=([fake_item], fake_item_pagination))
getter.publish = MagicMock("publish", return_value=fake_item)


@patch("tableauserverclient.Server")
@patch("tabcmd.commands.auth.session.Session.create_session")
class RunCommandsTest(unittest.TestCase):
    @staticmethod
    def _set_up_session(mock_session, mock_server):
        mock_session.return_value = mock_server
        assert mock_session is not None
        mock_session.assert_not_called()
        global mock_args
        mock_args = argparse.Namespace(logging_level="DEBUG")
        # set values for things that should always have a default
        # should refactor so this can be automated
        mock_args.continue_if_exists = False
        mock_args.project_name = None
        mock_args.parent_project_path = None
        mock_args.parent_path = None
        mock_args.timeout = None
        mock_args.username = None

    def test_publish(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
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
        mock_server.projects = getter
        publish_command.PublishCommand.run_command(mock_args)
        mock_session.assert_called()

    def test_publish_with_creds(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
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

        mock_server.projects = getter
        publish_command.PublishCommand.run_command(mock_args)
        mock_session.assert_called()
