import argparse
import unittest
from unittest.mock import *

from tabcmd.commands.auth import login_command, logout_command
from tabcmd.commands.datasources_and_workbooks import delete_command, \
    export_command, get_url_command, publish_command, runschedule_command
from tabcmd.commands.extracts import create_extracts_command, delete_extracts_command, decrypt_extracts_command, \
    encrypt_extracts_command, reencrypt_extracts_command, refresh_extracts_command
from tabcmd.commands.group import create_group_command, delete_group_command
from tabcmd.commands.help import help_command
from tabcmd.commands.project import create_project_command, delete_project_command, publish_samples_command
from tabcmd.commands.site import create_site_command, delete_site_command, delete_site_users_command, \
    edit_site_command, list_sites_command
from tabcmd.commands.user import add_users_command, create_site_users, remove_users_command, user_command

mock_args = argparse.Namespace()
mock_args.logging_level = 'info'

getter = MagicMock()
getter.get = MagicMock('get', return_value=([], 1))
fake_item = MagicMock()
fake_item.name = 'fake-name'
getter.publish = MagicMock('publish', return_value=fake_item)

fake_job = MagicMock()
fake_job.id = 'fake-job-id'
getter.create_extract = MagicMock('create_extract', return_value=fake_job)
getter.decrypt_extract = MagicMock('decrypt_extract', return_value=fake_job)
getter.delete_extract = MagicMock('delete_extract', return_value=fake_job)
getter.encrypt_extracts = MagicMock('encrypt_extracts', return_value=fake_job)
getter.reencrypt_extract = MagicMock('reencrypt_extract', return_value=fake_job)
getter.refresh = MagicMock('refresh', return_value=fake_job)


@patch('tableauserverclient.Server')
@patch('tabcmd.commands.auth.session.Session.create_session')
class RunCommandsTest(unittest.TestCase):

    # auth
    def test_login(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        assert mock_session is not None
        mock_session.assert_not_called()
        login_command.LoginCommand.run_command(mock_args)
        mock_session.assert_called_with(mock_args)

    def test_logout(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_session.assert_not_called()
        logout_command.LogoutCommand.run_command(mock_args)
        mock_session.assert_called()

    # datasources and workbooks
    #     workbook_from_list = matching_workbook[0]
    # IndexError: list index out of range
    def test_delete(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_server.workbooks = getter
        mock_server.datasources = getter
        mock_args.workbook = True
        mock_args.datasource = False
        mock_session.assert_not_called()
        with self.assertRaises(SystemExit):
            delete_command.DeleteCommand.run_command(mock_args)
            mock_session.assert_called()

    #     workbook_from_list = matching_workbook[0]
    # IndexError: list index out of range
    def test_export(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_server.workbooks = getter
        mock_args.fullpdf = True
        mock_args.url = 'url/split/pieces'
        mock_session.assert_not_called()
        with self.assertRaises(SystemExit):
            export_command.ExportCommand.run_command(mock_args)
            mock_session.assert_called()

    #     views_from_list = matching_view[0]
    # IndexError: list index out of range
    def test_get(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_server.views = getter
        mock_args.url = 'url/split/stuff'
        mock_args.filename = 'filename.pdf'
        mock_session.assert_not_called()
        with self.assertRaises(SystemExit):
            get_url_command.GetUrl.run_command(mock_args)
            mock_session.assert_called()

    def test_publish(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_args.overwrite = False
        mock_args.source = 'dont.know'
        mock_args.project = 'project-name'
        mock_server.projects = getter

        mock_session.assert_not_called()
        publish_command.PublishCommand.run_command(mock_args)
        mock_session.assert_called()

    def test_runschedule(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_session.assert_not_called()
        runschedule_command.RunSchedule.run_command(mock_args)
        mock_session.assert_called()

    # extracts
    def test_create_extract(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_server.datasources = getter
        mock_args.datasource = True
        mock_args.encrypt = False
        mock_session.assert_not_called()
        create_extracts_command.CreateExtracts.run_command(mock_args)
        mock_session.assert_called()

    def test_decrypt(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_server.sites = getter
        mock_session.assert_not_called()
        decrypt_extracts_command.DecryptExtracts.run_command(mock_args)
        mock_session.assert_called()

    def test_delete_extract(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_server.datasources = getter
        mock_args.datasource = True
        mock_session.assert_not_called()
        delete_extracts_command.DeleteExtracts.run_command(mock_args)
        mock_session.assert_called()

    def test_encrypt_extract(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_server.sites = getter
        mock_args.site_name = 'name'
        mock_session.assert_not_called()
        encrypt_extracts_command.EncryptExtracts.run_command(mock_args)
        mock_session.assert_called()

    def test_reencrypt_extract(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_args.site_name = 'name'
        mock_server.sites = getter
        mock_session.assert_not_called()
        reencrypt_extracts_command.ReencryptExtracts.run_command(mock_args)
        mock_session.assert_called()

    def test_refresh_extract(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_args.datasource = 'datasource'
        mock_server.datasources = getter
        mock_session.assert_not_called()
        refresh_extracts_command.RefreshExtracts.run_command(mock_args)
        mock_session.assert_called()

    # groups
    def test_create_group(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_args.name = 'name'
        mock_session.assert_not_called()
        create_group_command.CreateGroupCommand.run_command(mock_args)
        mock_session.assert_called()

    def test_delete_group(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_args.groupname = 'name'
        mock_server.groups = getter
        mock_session.assert_not_called()
        delete_group_command.DeleteGroupCommand.run_command(mock_args)
        mock_session.assert_called()

    # help
    def test_help(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_session.assert_not_called()
        help_command.HelpCommand.run_command(mock_args)
        mock_session.assert_not_called()

    # project
    def test_create_project(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_server.projects = getter
        mock_args.name = 'name'
        mock_args.description = ''
        mock_args.content_permission = None
        mock_args.parent_project_path = 'projects'
        mock_session.assert_not_called()
        create_project_command.CreateProjectCommand.run_command(mock_args)
        mock_session.assert_called()

    def test_delete_project(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_server.projects = getter
        mock_args.name = 'project-name'
        mock_session.assert_not_called()
        delete_project_command.DeleteProjectCommand.run_command(mock_args)
        mock_session.assert_called()

    def test_publish_project(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_server.projects = getter
        mock_args.parent_path_name = ''
        mock_session.assert_not_called()
        # Not yet implemented
        # publish_samples_command.PublishSamplesCommand.run_command(mock_args)
        # mock_session.assert_called()

    # site
    def test_create_site(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_args.site_name = 'site-name'
        mock_args.url = 'site-content-url'
        mock_args.admin_mode = None
        mock_args.user_quota = None,
        mock_args.storage_quota = None
        mock_session.assert_not_called()
        create_site_command.CreateSiteCommand.run_command(mock_args)
        mock_session.assert_called()

    def test_delete_site(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_server.sites = getter
        mock_args.site_name = 'site-name'
        mock_session.assert_not_called()
        delete_site_command.DeleteSiteCommand.run_command(mock_args)
        mock_session.assert_called()

    @patch('tabcmd.commands.user.user_command.UserCommand.get_users_from_file')
    def test_delete_site_users(self, mock_file, mock_session, mock_server):
        mock_args.csv_users = []
        mock_file.return_value = []
        mock_session.return_value = mock_server
        mock_session.assert_not_called()
        delete_site_users_command.DeleteSiteUsersCommand.run_command(mock_args)
        mock_session.assert_called()

    def test_edit_site(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_server.sites = getter
        mock_args.site_name = 'site-name'
        mock_session.assert_not_called()
        with self.assertRaises(SystemExit):
            edit_site_command.EditSiteCommand.run_command(mock_args)
            mock_session.assert_called()

    def test_list_sites(self, mock_session, mock_server):
        mock_session.return_value = mock_server
        mock_server.sites = getter
        mock_session.assert_not_called()
        list_sites_command.ListSiteCommand.run_command(mock_args)
        mock_session.assert_called()

    # users
    @patch('tabcmd.commands.user.user_command.UserCommand.get_users_from_file')
    def test_add_users(self, mock_file, mock_session, mock_server):
        mock_file.return_value = []
        mock_session.return_value = mock_server
        mock_server.sites = getter
        mock_args.csv_lines = []
        mock_session.assert_not_called()
        add_users_command.AddUserCommand.run_command(mock_args)
        mock_session.assert_called()

    @patch('tabcmd.commands.user.user_command.UserCommand.get_users_from_file')
    def test_create_site_users(self, mock_file, mock_session, mock_server):
        mock_file.return_value = []
        mock_session.return_value = mock_server
        mock_session.assert_not_called()
        create_site_users.CreateSiteUsersCommand.run_command(mock_args)
        mock_session.assert_called()

    @patch('tabcmd.commands.user.user_command.UserCommand.get_users_from_file')
    def test_remove_users(self, mock_file, mock_session, mock_server):
        mock_file.return_value = []
        mock_session.return_value = mock_server
        mock_args.csv_lines = []
        mock_session.assert_not_called()
        remove_users_command.RemoveUserCommand.run_command(mock_args)
        mock_session.assert_called()
