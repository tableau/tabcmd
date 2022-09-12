import os
import pytest
import subprocess
import time
import unittest

from tests.e2e import setup_e2e

debug_log = "--logging-level=DEBUG"
indexing_sleep_time = 1  # wait 1 second to confirm server has indexed updates

project_name = "not-default-name"
group_name = "test-ing-group"
workbook_name = "namebasic"

# to run this suite
# pytest -q tests/e2e/online_tests.py
# you can either run setup with a stored credentials file, or simply log in
# before running the suite so a session is active

# alpodev
parent_location = "WAM"
project_name = "Developer Platform"

server_admin = False
site_admin = True
project_admin = True


def _test_command(test_args: list[str]):
    # this will raise an exception if it gets a non-zero return code
    # that should bubble up and fail the test?
    # dist/exe calling_args = [setup_e2e.exe] + test_args + [debug_log]
    calling_args = ["python", "-m", "tabcmd"] + test_args + [debug_log] + ["--no-certcheck"]
    print(calling_args)
    return subprocess.check_call(calling_args)


# This calls dist/tabcmd/tabcmd.exe
class OnlineCommandTest(unittest.TestCase):
    published = False
    gotten = False

    @classmethod
    def setup_class(cls):
        print("running python -m")
        # call this if we are using the built exe setup_e2e.prechecks()

    ## Individual methods that implement a command

    def _create_project(self, project_name, parent_path=None):
        command = "createproject"
        arguments = [command, "--name", project_name]
        if parent_path or parent_location:
            arguments.append("--parent-project-path")
            arguments.append(parent_path)
        _test_command(arguments)

    def _delete_project(self, project_name, parent_path=None):
        command = "deleteproject"
        arguments = [command, project_name]
        if parent_path or parent_location:
            arguments.append("--parent-project-path")
            arguments.append(parent_path or parent_location)
        _test_command(arguments)

    def _publish_samples(self, project_name):
        command = "publishsamples"
        arguments = [command, "--name", project_name]
        _test_command(arguments)

    def _publish_wb(self, file, name):
        command = "publish"
        arguments = [command, file, "--name", name, "--overwrite"]
        return _test_command(arguments)

    def _delete_wb(self, file):
        command = "delete"
        arguments = [command, file]
        _test_command(arguments)

    def _get_view(self, wb_name_on_server, sheet_name):
        server_file = "/views/" + wb_name_on_server + "/" + sheet_name
        command = "get"
        arguments = [command, server_file]
        _test_command(arguments)

    def _get_custom_view(self):
        command = "get"

    def _get_view_with_filters(self):
        command = "get"

    def _get_workbook(self, server_file):
        command = "get"
        server_file = "/workbooks/" + server_file
        arguments = [command, server_file]
        _test_command(arguments)

    def _create_extract(self, wb_name):
        command = "createextracts"
        arguments = [command, "-w", wb_name, "--encrypt"]
        _test_command(arguments)

    # variation: url
    def _refresh_extract(self, wb_name):
        command = "refreshextracts"
        arguments = [command, "--workbook", wb_name]
        _test_command(arguments)

    def _delete_extract(self, wb_name):
        command = "deleteextracts"
        arguments = [command, "-w", wb_name]
        _test_command(arguments)

    def _list(self, item_type: str):
        command = "list"
        arguments = [command, item_type]
        _test_command(arguments)

    # actual tests
    TWBX_FILE_WITH_EXTRACT = "extract-data-access.twbx"
    TWBX_WITH_EXTRACT_NAME = "WorkbookWithExtract"
    TWBX_WITH_EXTRACT_SHEET = "sheet1"
    TWBX_FILE_WITHOUT_EXTRACT = "simple-data.twbx"
    TWBX_WITHOUT_EXTRACT_NAME = "WorkbookWithoutExtract"
    TWBX_WITHOUT_EXTRACT_SHEET = "Testsheet1"

    @pytest.mark.order(1)
    def test_login(self):
        try:
            setup_e2e.login()
        except Exception as e:
            raise SystemExit(2)

    @pytest.mark.order(1)
    def test_version(self):
        command = "-v"
        arguments = [command]
        _test_command(arguments)

    @pytest.mark.order(1)
    def test_help(self):
        command = "help"
        arguments = [command]
        _test_command(arguments)

    @pytest.mark.order(2)
    def test_users_create_site_users(self):
        if not server_admin and not site_admin:
            pytest.skip("Must be server or site administrator to create site users")
        command = "createsiteusers"
        users = os.path.join("tests", "assets", "detailed_users.csv")
        arguments = [command, users, "--role", "Publisher"]
        _test_command(arguments)

    @pytest.mark.order(3)
    def test_group_creategroup(self):
        if not server_admin and not site_admin:
            pytest.skip("Must be server or site administrator to create groups")
        groupname = group_name
        command = "creategroup"
        arguments = [command, groupname]
        _test_command(arguments)

    @pytest.mark.order(4)
    def test_users_add_to_group(self):
        if not server_admin and not site_admin:
            pytest.skip("Must be server or site administrator to add to groups")

        groupname = group_name
        command = "addusers"
        filename = os.path.join("tests", "assets", "usernames.csv")
        arguments = [command, groupname, "--users", filename]
        _test_command(arguments)

    @pytest.mark.order(5)
    def test_users_remove_from_group(self):
        if not server_admin and not site_admin:
            pytest.skip("Must be server or site administrator to remove from groups")

        groupname = group_name
        command = "removeusers"
        filename = os.path.join("tests", "assets", "usernames.csv")
        arguments = [command, groupname, "--users", filename]
        _test_command(arguments)

    @pytest.mark.order(6)
    def test_group_deletegroup(self):
        if not server_admin and not site_admin:
            pytest.skip("Must be server or site administrator to delete groups")

        groupname = group_name
        command = "deletegroup"
        arguments = [command, groupname]
        _test_command(arguments)

    @pytest.mark.order(8)
    def test_create_projects(self):
        if not project_admin:
            pytest.skip("Must be project administrator to create projects")

        # project 1
        self._create_project(parent_location)
        time.sleep(indexing_sleep_time)
        # project 1
        self._create_project(project_name)
        time.sleep(indexing_sleep_time)
        # project 2
        self._create_project("project_name_2", project_name)
        time.sleep(indexing_sleep_time)
        # project 3
        parent_path = "{0}/{1}".format(project_name, project_name)
        self._create_project(project_name, parent_path)
        time.sleep(indexing_sleep_time)

    @pytest.mark.order(8)
    def test_list_projects(self):
        self._list("projects")

    """
        @pytest.mark.order(9)
        def test_publish_samples(self):
            self._publish_samples(project_name)
    """

    @pytest.mark.order(10)
    def test_delete_projects(self):
        if not project_admin:
            pytest.skip("Must be project administrator to create projects")
        self._delete_project("project_name_2", project_name)  # project 2
        self._delete_project(project_name)

    @pytest.mark.order(10)
    def test_wb_publish(self):
        name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        file = os.path.join("tests", "assets", OnlineCommandTest.TWBX_FILE_WITH_EXTRACT)
        self._publish_wb(file, name_on_server)

    @pytest.mark.order(10)
    def test_wb_get(self):
        self._get_workbook(OnlineCommandTest.TWBX_WITH_EXTRACT_NAME + ".twbx")

    @pytest.mark.order(10)
    def test_view_get_pdf(self):
        wb_name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        sheet_name = OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET
        self._get_view(wb_name_on_server, sheet_name + ".pdf")

    @pytest.mark.order(10)
    def test_view_get_csv(self):
        wb_name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        sheet_name = OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET
        self._get_view(wb_name_on_server, sheet_name + ".csv")

    @pytest.mark.order(10)
    def test_view_get_png(self):
        wb_name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        sheet_name = OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET
        self._get_view(wb_name_on_server, sheet_name + ".png")

    @pytest.mark.order(11)
    def test_wb_delete(self):
        name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        self._delete_wb(name_on_server)

    @pytest.mark.order(12)
    def test_extract_delete(self):
        # fails because the extract has a bad data connection :/
        name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        file = os.path.join("tests", "assets", OnlineCommandTest.TWBX_FILE_WITH_EXTRACT)
        self._publish_wb(file, name_on_server)
        self._delete_extract(name_on_server)

    @pytest.mark.order(13)
    def test_extract_create(self):
        # Fails because it 'already has an extract' :/
        name_on_server = OnlineCommandTest.TWBX_WITHOUT_EXTRACT_NAME
        self._create_extract(name_on_server)

    @pytest.mark.order(14)
    def test_extract_refresh(self):
        # must be a datasource owned by the test user
        name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        file = os.path.join("tests", "assets", OnlineCommandTest.TWBX_FILE_WITH_EXTRACT)
        self._publish_wb(file, name_on_server)

        name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        self._refresh_extract(name_on_server)
        self._delete_wb(name_on_server)

    @pytest.mark.order(15)
    def test_export_wb_pdf(self):
        name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        file = os.path.join("tests", "assets", OnlineCommandTest.TWBX_FILE_WITH_EXTRACT)
        self._publish_wb(file, name_on_server)
        command = "export"
        friendly_name = name_on_server + "/" + OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET
        arguments = [command, friendly_name, "--fullpdf", "-f", "exported_wb.pdf"]
        _test_command(arguments)

    @pytest.mark.order(15)
    def test_export_view_pdf(self):
        name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        file = os.path.join("tests", "assets", OnlineCommandTest.TWBX_FILE_WITH_EXTRACT)
        self._publish_wb(file, name_on_server)
        command = "export"
        friendly_name = name_on_server + "/" + OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET + "?param1=3"
        arguments = [command, friendly_name, "--pdf", "-f", "exported_view.pdf"]
        _test_command(arguments)

    @pytest.mark.order(16)
    def test_users_delete_site_users(self):
        if not server_admin and not site_admin:
            pytest.skip("Must be server or site administrator to delete site users")

        command = "deletesiteusers"
        users = os.path.join("tests", "assets", "usernames.csv")
        _test_command([command, users])

    @pytest.mark.order(20)
    def test_list_sites(self):
        if not server_admin:
            pytest.skip("Must be server administrator to list sites")

        command = "listsites"
        try:
            _test_command([command])
        except Exception as E:
            print("yay")
            result = True
        assert result
