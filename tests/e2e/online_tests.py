import os
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


def _test_command(test_args: list[str]):
    # this will raise an exception if it gets a non-zero return code
    # that should bubble up and fail the test?
    # dist/exe calling_args = [setup_e2e.exe] + test_args + [debug_log]
    calling_args = ["python", "-m", "tabcmd"] + test_args + [debug_log] + ["--no-certcheck"]
    print(calling_args)
    # return subprocess.check_call(calling_args)


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

    def _delete_wb(self, file):
        command = "delete"
        arguments = [command, "-w", file]
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

    # actual tests
    TWBX_FILE_WITH_EXTRACT = "extract-data-access.twbx"
    TWBX_WITH_EXTRACT_NAME = "WorkbookWithExtract"
    TWBX_WITH_EXTRACT_SHEET = "sheet1"
    TWBX_FILE_WITHOUT_EXTRACT = "simple-data.twbx"
    TWBX_WITHOUT_EXTRACT_NAME = "WorkbookWithoutExtract"

    def test_login(self):
        try:
            setup_e2e.Setup.login()
        except Exception as e:
            raise SystemExit(2)

    def test_create_site_users(self):
        command = "createsiteusers"
        users = os.path.join("tests", "assets", "detailed_users.csv")
        arguments = [command, users, "--role", "Publisher"]
        _test_command(arguments)

    def test_creategroup(self):
        groupname = group_name
        command = "creategroup"
        arguments = [command, groupname]
        _test_command(arguments)

    def test_add_users_to_group(self):
        groupname = group_name
        command = "addusers"
        filename = os.path.join("tests", "assets", "usernames.csv")
        arguments = [command, groupname, "--users", filename]
        _test_command(arguments)

    def test_remove_users_to_group(self):
        groupname = group_name
        command = "removeusers"
        filename = os.path.join("tests", "assets", "usernames.csv")
        arguments = [command, groupname, "--users", filename]
        _test_command(arguments)

    def test_deletegroup(self):
        groupname = group_name
        command = "deletegroup"
        arguments = [command, groupname]
        _test_command(arguments)

    def test_publish_samples(self):
        project_name = "sample-proj"
        self._create_project(project_name)
        time.sleep(indexing_sleep_time)

        self._publish_samples(project_name)
        self._delete_project(project_name)

    def test_create_projects(self):
        # project 1
        self._create_project(project_name)
        time.sleep(indexing_sleep_time)
        # project 2
        self._create_project(project_name, project_name)
        time.sleep(indexing_sleep_time)
        # project 3
        parent_path = "{0}/{1}".format(project_name, project_name)
        self._create_project(project_name, parent_path)
        time.sleep(indexing_sleep_time)

    def test_delete_projects(self):
        self._delete_project(project_name, project_name)  # project 2
        self._delete_project(project_name)

    def test_publish(self):
        name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        file = os.path.join("tests", "assets", OnlineCommandTest.TWBX_FILE_WITH_EXTRACT)
        self._publish_wb(file, name_on_server)

    """
    I have no idea why but these exact same commands succeed run alone,
    and fail here 
    def test__get_wb(self):
        wb_name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        self._get_workbook(wb_name_on_server + ".twbx")

    def test__get_view(self):
        wb_name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        sheet_name = OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET
        self._get_view(wb_name_on_server, sheet_name + ".pdf")
    """

    def test__delete_wb(self):
        name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        self._delete_wb(name_on_server)

    def test_create_extract(self):
        # This workbook doesn't work for creating an extract
        name_on_server = OnlineCommandTest.TWBX_WITHOUT_EXTRACT_NAME
        file = os.path.join("tests", "assets", OnlineCommandTest.TWBX_FILE_WITHOUT_EXTRACT)
        self._publish_wb(file, name_on_server)
        # which damn workbook will work here self._create_extract(name_on_server)

    def test_refresh_extract(self):
        name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        self._refresh_extract(name_on_server)

    def test_delete_extract(self):
        name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        file = os.path.join("tests", "assets", OnlineCommandTest.TWBX_FILE_WITH_EXTRACT)
        self._publish_wb(file, name_on_server)
        # waiting for tsc update self._delete_extract(name_on_server)
        self._delete_wb(name_on_server)

    def test_version(self):
        _test_command(["-v"])

    def test_help(self):
        _test_command(["help"])

    # this just gets in the way :(
    # def test_logout(self):
    #   _test_command(["logout"])

    def test_export(self):
        name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        file = os.path.join("tests", "assets", OnlineCommandTest.TWBX_FILE_WITH_EXTRACT)
        self._publish_wb(file, name_on_server)
        command = "export"
        friendly_name = name_on_server + "/" + OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET
        arguments = [command, friendly_name, "--fullpdf", "-f", "exported_file.pdf"]
        _test_command(arguments)

    def test_delete_site_users(self):
        command = "deletesiteusers"
        users = os.path.join("tests", "assets", "usernames.csv")
        _test_command([command, users])