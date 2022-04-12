import argparse
import unittest
from unittest.mock import *

from tabcmd.commands.auth import login_command, logout_command
from tabcmd.commands.datasources_and_workbooks import (
    delete_command,
    export_command,
    get_url_command,
    publish_command,
    runschedule_command,
)
from tabcmd.commands.extracts import (
    create_extracts_command,
    delete_extracts_command,
    decrypt_extracts_command,
    encrypt_extracts_command,
    reencrypt_extracts_command,
    refresh_extracts_command,
)
from tabcmd.commands.group import create_group_command, delete_group_command
from tabcmd.commands.help import help_command
from tabcmd.commands.project import create_project_command, delete_project_command
from tabcmd.commands.site import (
    create_site_command,
    delete_site_command,
    edit_site_command,
    list_sites_command,
)
from tabcmd.commands.user import (
    add_users_command,
    create_site_users,
    remove_users_command,
    delete_site_users_command,
)
from typing import List, NamedTuple, TextIO, Union
import io

mock_args = argparse.Namespace()
mock_args.logging_level = "info"

fake_item = MagicMock()
fake_item.name = "fake-name"
fake_item.id = "fake-id"
fake_item.pdf = b"/pdf-representation-of-view"
fake_item.extract_encryption_mode = "Disabled"

fake_job = MagicMock()
fake_job.id = "fake-job-id"

getter = MagicMock()
getter.get = MagicMock("get", return_value=([fake_item], 1))
getter.publish = MagicMock("publish", return_value=fake_item)
getter.create_extract = MagicMock("create_extract", return_value=fake_job)
getter.decrypt_extract = MagicMock("decrypt_extract", return_value=fake_job)
getter.delete_extract = MagicMock("delete_extract", return_value=fake_job)
getter.encrypt_extracts = MagicMock("encrypt_extracts", return_value=fake_job)
getter.reencrypt_extract = MagicMock("reencrypt_extract", return_value=fake_job)
getter.refresh = MagicMock("refresh", return_value=fake_job)


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

    # auth
    def test_login(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        login_command.LoginCommand.run_command(mock_args)
        mock_session.assert_called_with(mock_args)

    @patch("tabcmd.commands.auth.session.Session.end_session_and_clear_data")
    def test_logout(self, mock_end_session, mock_create_session, mock_server):
        logout_command.LogoutCommand.run_command(mock_args)
        mock_create_session.assert_not_called()
        mock_end_session.assert_called()

    def test_delete(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_server.workbooks = getter
        mock_server.datasources = getter
        mock_args.workbook = True
        mock_args.datasource = False
        mock_args.name = "name for on server"
        delete_command.DeleteCommand.run_command(mock_args)

    def test_export(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_server.workbooks = getter
        mock_args.fullpdf = True
        mock_args.filename = "filename.pdf"
        mock_args.url = "url/split/pieces"
        export_command.ExportCommand.run_command(mock_args)
        mock_session.assert_called()

    def test_get(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_server.views = getter
        mock_args.url = "views/workbook-name/view-name"
        mock_args.filename = "filename.pdf"
        get_url_command.GetUrl.run_command(mock_args)
        mock_session.assert_called()

    def test_publish(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_args.overwrite = False
        mock_args.filename = "existing_file.twbx"
        mock_args.project_name = "project-name"
        mock_args.parent_project_path = "projects"
        mock_args.name = ""
        mock_args.tabbed = True
        mock_server.projects = getter
        publish_command.PublishCommand.run_command(mock_args)
        mock_session.assert_called()

    def test_runschedule(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_server.schedules = getter
        mock_args.schedule = "myschedule"
        with self.assertRaises(SystemExit):
            runschedule_command.RunSchedule.run_command(mock_args)
        # mock_session.assert_called()

    # extracts
    def test_create_extract(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_server.workbooks = getter
        mock_args.encrypt = False
        mock_args.include_all = True
        mock_args.datasource = None
        mock_args.embedded_datasources = None
        mock_args.workbook = "workbook"
        create_extracts_command.CreateExtracts.run_command(mock_args)
        mock_session.assert_called()

    def test_decrypt(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_args.site_name = "mock site"
        mock_server.sites = getter
        decrypt_extracts_command.DecryptExtracts.run_command(mock_args)
        mock_session.assert_called()

    def test_delete_extract(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_server.datasources = getter
        mock_args.datasource = True
        delete_extracts_command.DeleteExtracts.run_command(mock_args)
        mock_session.assert_called()

    def test_encrypt_extract(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_server.sites = getter
        mock_args.site_name = "name"
        encrypt_extracts_command.EncryptExtracts.run_command(mock_args)
        mock_session.assert_called()

    def test_reencrypt_extract(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_args.site_name = "name"
        mock_server.sites = getter
        reencrypt_extracts_command.ReencryptExtracts.run_command(mock_args)
        mock_session.assert_called()

    def test_refresh_extract(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_args.datasource = "datasource"
        mock_server.datasources = getter
        refresh_extracts_command.RefreshExtracts.run_command(mock_args)
        mock_session.assert_called()

    # groups
    def test_create_group(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_args.name = "name"
        create_group_command.CreateGroupCommand.run_command(mock_args)
        mock_session.assert_called()

    def test_delete_group(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_args.name = "name"
        mock_server.groups = getter
        delete_group_command.DeleteGroupCommand.run_command(mock_args)
        mock_session.assert_called()

    # help
    def test_help(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        help_command.HelpCommand.run_command(mock_args)
        mock_session.assert_not_called()

    # project
    def test_create_project(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_server.projects = getter
        mock_args.project_name = "name"
        mock_args.description = ""
        mock_args.content_permission = None
        mock_args.parent_project_path = "projects"
        create_project_command.CreateProjectCommand.run_command(mock_args)
        mock_session.assert_called()

    def test_delete_project(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_server.projects = getter
        mock_args.project_name = "project-name"
        mock_session.assert_not_called()
        mock_args.parent_project_path = "projects"
        delete_project_command.DeleteProjectCommand.run_command(mock_args)
        mock_session.assert_called()

    def test_publish_project(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_server.projects = getter
        mock_args.parent_project_name = ""
        # Not yet implemented
        # publish_samples_command.PublishSamplesCommand.run_command(mock_args)
        # mock_session.assert_called()

    # site
    def test_create_site(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_args.site_name = "site-name"
        mock_args.url = "site-content-url"
        mock_args.admin_mode = None
        mock_args.user_quota = (None,)
        mock_args.storage_quota = None
        create_site_command.CreateSiteCommand.run_command(mock_args)
        mock_session.assert_called()

    def test_delete_site(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_server.sites = getter
        mock_args.site_name = "site-name"
        delete_site_command.DeleteSiteCommand.run_command(mock_args)
        mock_session.assert_called()

    def test_edit_site(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_server.sites = getter
        mock_args.site_name = "site-name"
        mock_args.new_site_name = None
        mock_args.url = "new-url"
        mock_args.user_quota = "1"
        mock_args.storage_quota = "1"
        mock_args.status = "Suspended"
        mock_session.assert_not_called()
        edit_site_command.EditSiteCommand.run_command(mock_args)
        mock_session.assert_called()

    def test_list_sites(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_server.sites = getter
        mock_args.get_extract_encryption_mode = "Disabled"
        list_sites_command.ListSiteCommand.run_command(mock_args)
        mock_session.assert_called()

    # TODO: get typings for argparse
    class NamedObject(NamedTuple):
        name: str

    ArgparseFile = Union[TextIO, NamedObject]

    @staticmethod
    def _set_up_file(content=["Test", "", "Test", ""]) -> ArgparseFile:
        # the empty string represents EOF
        # the tests run through the file twice, first to validate then to fetch
        mock = MagicMock(io.TextIOWrapper)
        mock.readline.side_effect = content
        mock.name = "file-mock"
        return mock

    def test_add_users(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_server.groups = getter
        mock_server.users = getter
        mock_args.users = RunCommandsTest._set_up_file()
        mock_args.name = "the-group"
        mock_args.require_all_valid = False
        add_users_command.AddUserCommand.run_command(mock_args)
        mock_session.assert_called()

    def test_remove_users(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_server.groups = getter
        mock_server.users = getter
        mock_args.name = "group-removing-from"
        mock_args.users = RunCommandsTest._set_up_file()
        mock_args.require_all_valid = False
        remove_users_command.RemoveUserCommand.run_command(mock_args)
        mock_session.assert_called()

    def test_create_site_users(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_args.filename = RunCommandsTest._set_up_file()
        mock_args.require_all_valid = False
        mock_args.site_name = None
        create_site_users.CreateSiteUsersCommand.run_command(mock_args)
        mock_session.assert_called()

    def test_delete_site_users(self, mock_session, mock_server):
        RunCommandsTest._set_up_session(mock_session, mock_server)
        mock_server.users = getter
        mock_args.filename = RunCommandsTest._set_up_file()
        mock_args.site_name = None
        mock_args.require_all_valid = True
        delete_site_users_command.DeleteSiteUsersCommand.run_command(mock_args)
        mock_session.assert_called()
