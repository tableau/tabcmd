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

# to run this suite:
# pytest -q tests/e2e/language_tests.py
# you can either run setup with a stored credentials file, or simply log in
# before running the suite so a session is active
# All tests in this suite are about handling non-English language scenarios


def _test_command(test_args: list[str]):
    # this will raise an exception if it gets a non-zero return code
    # that should bubble up and fail the test?
    # dist/exe calling_args = [setup_e2e.exe] + test_args + [debug_log]
    calling_args = ["python", "-m", "tabcmd"] + test_args + [debug_log] + ["--language", "fr", "--no-certcheck"]
    print(calling_args)
    return subprocess.check_call(calling_args)


@pytest.fixture(scope="module", autouse=True)
def login_all_languages():
    """Login fixture that tests login with all supported languages."""
    languages = ["de", "en", "es", "fr", "it", "ja", "ko", "pt", "sv", "zh"]
    failed = False
    for lang in languages:
        try:
            setup_e2e.login("--language", lang)
        except Exception as e:
            failed = True
            print("FAILED on {}".format(lang))
    if failed:
        raise SystemExit(2)


@pytest.fixture(scope="module")
def site_users(login_all_languages):
    """Create site users for tests and clean up after."""
    command = "createsiteusers"
    users = os.path.join("tests", "assets", "detailed_users.csv")
    arguments = [command, users, "--role", "Publisher"]
    _test_command(arguments)
    
    yield
    
    # Cleanup
    command = "deletesiteusers"
    users = os.path.join("tests", "assets", "usernames.csv")
    try:
        _test_command([command, users])
    except Exception as e:
        print(f"Failed to delete site users during cleanup: {e}")


@pytest.fixture(scope="module")
def test_group(site_users):
    """Create a test group and clean up after."""
    groupname = group_name
    command = "creategroup"
    arguments = [command, groupname]
    _test_command(arguments)
    
    yield groupname
    
    # Cleanup
    command = "deletegroup"
    arguments = [command, groupname]
    try:
        _test_command(arguments)
    except Exception as e:
        print(f"Failed to delete group during cleanup: {e}")


@pytest.fixture(scope="module")
def test_projects(login_all_languages):
    """Create test projects and clean up after."""
    def create_project(project_name, parent_path=None):
        command = "createproject"
        arguments = [command, "--name", project_name]
        if parent_path:
            arguments.append("--parent-project-path")
            arguments.append(parent_path)
        _test_command(arguments)
    
    def delete_project(project_name, parent_path=None):
        command = "deleteproject"
        arguments = [command, project_name]
        if parent_path:
            arguments.append("--parent-project-path")
            arguments.append(parent_path)
        _test_command(arguments)
    
    # Create projects
    create_project("project_name")
    time.sleep(indexing_sleep_time)
    create_project("project_name_2", "project_name")
    time.sleep(indexing_sleep_time)
    
    # Publish samples to a project
    command = "publishsamples"
    arguments = [command, "--name", project_name]
    _test_command(arguments)
    
    yield
    
    # Cleanup
    try:
        delete_project("project_name_2", "project_name")
        delete_project("project_name")
    except Exception as e:
        print(f"Failed to delete projects during cleanup: {e}")


# This calls dist/tabcmd/tabcmd.exe
class OnlineCommandTest(unittest.TestCase):
    published = False
    gotten = False

    def _create_project(self, project_name, parent_path=None):
        command = "createproject"
        arguments = [command, "--name", project_name]
        if parent_path:
            arguments.append("--parent-project-path")
            arguments.append(parent_path)
        print(arguments)
        _test_command(arguments)

    def _delete_project(self, project_name, parent_path=None):
        command = "deleteproject"
        arguments = [command, project_name]
        if parent_path:
            arguments.append("--parent-project-path")
            arguments.append(parent_path)
        _test_command(arguments)

    def _publish_samples(self, project_name):
        command = "publishsamples"
        arguments = [command, "--name", project_name]
        _test_command(arguments)

    def _publish_wb(self, file, name):
        command = "publish"
        arguments = [command, file, "--name", name, "--overwrite"]
        return _test_command(arguments)

    def _publish_ds(self, file, name):
        command = "publish"
        arguments = [command, file, "--name", name, "--overwrite"]
        return _test_command(arguments)

    def _delete_wb(self, file):
        command = "delete"
        arguments = [command, "-w", file]
        _test_command(arguments)

    def _delete_ds(self, file):
        command = "delete"
        arguments = [command, file, "--datasource"]
        _test_command(arguments)

    def _get_view(self, wb_name_on_server, sheet_name):
        server_file = "/views/" + wb_name_on_server + "/" + sheet_name
        command = "get"
        arguments = [command, server_file]
        _test_command(arguments)

    def _get_datasource(self, server_file):
        command = "get"
        server_file = "/datasources/" + server_file
        arguments = [command, server_file]
        _test_command(arguments)

    def _get_custom_view(self):
        command = "get"

    def _get_view_with_filters(self):
        command = "get"

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

    # actual tests
    TWBX_FILE_WITH_EXTRACT = "extract-data-access.twbx"
    TWBX_WITH_EXTRACT_NAME = "WorkbookWithExtract"
    TWBX_WITH_EXTRACT_SHEET = "sheet1"
    TWBX_FILE_WITHOUT_EXTRACT = "simple-data.twbx"
    TWBX_WITHOUT_EXTRACT_NAME = "WorkbookWithoutExtract"
    TDSX_WITH_EXTRACT_NAME = "WorldIndicators"
    TDSX_FILE_WITH_EXTRACT = "World Indicators.tdsx"

    def test_add_users_to_group(self, test_group):
        groupname = test_group
        command = "addusers"
        filename = os.path.join("tests", "assets", "usernames.csv")
        arguments = [command, groupname, "--users", filename]
        _test_command(arguments)

    def test_remove_users_to_group(self, test_group):
        groupname = test_group
        command = "removeusers"
        filename = os.path.join("tests", "assets", "usernames.csv")
        arguments = [command, groupname, "--users", filename]
        _test_command(arguments)

    def test_publish(self, test_projects):
        name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        file = os.path.join("tests", "assets", OnlineCommandTest.TWBX_FILE_WITH_EXTRACT)
        self._publish_wb(file, name_on_server)

    def test__get_wb(self, test_projects):
        wb_name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        self._get_workbook(wb_name_on_server + ".twbx")

    def test__get_view(self, test_projects):
        wb_name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        sheet_name = OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET
        self._get_view(wb_name_on_server, sheet_name + ".pdf")

    def test__delete_wb(self, test_projects):
        name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        self._delete_wb(name_on_server)

    def test_publish_ds(self, test_projects):
        name_on_server = OnlineCommandTest.TDSX_WITH_EXTRACT_NAME
        file = os.path.join("tests", "assets", OnlineCommandTest.TDSX_FILE_WITH_EXTRACT)
        self._publish_ds(file, name_on_server)

    def test__get_ds(self, test_projects):
        ds_name_on_server = OnlineCommandTest.TDSX_WITH_EXTRACT_NAME
        self._get_datasource(ds_name_on_server + ".tdsx")

    def test__delete_ds(self, test_projects):
        name_on_server = OnlineCommandTest.TDSX_WITH_EXTRACT_NAME
        self._delete_ds(name_on_server)

    def test_create_extract(self, test_projects):
        # This workbook doesn't work for creating an extract
        name_on_server = OnlineCommandTest.TWBX_WITHOUT_EXTRACT_NAME
        file = os.path.join("tests", "assets", OnlineCommandTest.TWBX_FILE_WITHOUT_EXTRACT)
        self._publish_wb(file, name_on_server)
        # which damn workbook will work here self._create_extract(name_on_server)

    def test_refresh_extract(self, test_projects):
        name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        self._refresh_extract(name_on_server)

    def test_delete_extract(self, test_projects):
        name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        file = os.path.join("tests", "assets", OnlineCommandTest.TWBX_FILE_WITH_EXTRACT)
        self._publish_wb(file, name_on_server)
        # self._delete_extract(name_on_server)
        self._delete_wb(name_on_server)

    def test_version(self):
        _test_command(["-v"])

    def test_help(self):
        _test_command(["help"])

    # this just gets in the way :(
    # def test_logout(self):
    #   _test_command(["logout"])

    def test_export(self, test_projects):
        name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        file = os.path.join("tests", "assets", OnlineCommandTest.TWBX_FILE_WITH_EXTRACT)
        self._publish_wb(file, name_on_server)
        command = "export"
        friendly_name = name_on_server + "/" + OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET
        arguments = [command, friendly_name, "--fullpdf", "-f", "exported_file.pdf"]
        _test_command(arguments)
