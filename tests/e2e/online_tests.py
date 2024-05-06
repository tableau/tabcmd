import os
import pytest
import subprocess
import time
import unittest

from typing import Optional

try:
    from credentials import waremart_password, waremart_user
    database_password = waremart_password
    database_user = waremart_user
except ModuleNotFoundError:
    waremart_user = None
    waremart_password = None
    print("Could not import datasource creds from credentials file")

from tests.e2e import setup_e2e


# to run this suite
# pytest -q tests/e2e/online_tests.py
# you can either run setup with a stored credentials file, or simply log in
# before running the suite so a session is active

debug_log = "--logging-level=DEBUG"
indexing_sleep_time = 1  # wait 1 second to confirm server has indexed updates

# object names
unique = str(time.gmtime().tm_sec)

default_project_name = "default-proj" + unique
group_name = "test-ing-group" + unique
workbook_name = "wb_1_" + unique

parent_location = "parent" + unique
project_name = "test-proj-" + unique

server_admin = False
site_admin = True
project_admin = True


def _test_command(test_args: list[str]):
    if test_args == []:
        test_args = ["version"]
    else: 
        test_args.append("--no-certcheck")
    # this will raise an exception if it gets a non-zero return code
    # that should bubble up and fail the test?
    # call the executable directly: lets us drop in classic tabcmd
    calling_args = [
        "python", "-m", "tabcmd"
        # "c:\\Program Files\\Tableau\\Tableau Server\\2023.1\\extras\\Command Line Utility\\tabcmd.exe"
    ] + test_args
    # uncomment this line instead to use the current build of tabcmd 2
    # calling_args = ["python", "-m", "tabcmd"] + test_args + [debug_log] + ["--no-certcheck"]
    print(calling_args)
    return subprocess.check_call(calling_args)


class OnlineCommandTest(unittest.TestCase):
    published = False
    gotten = False

    @classmethod
    def setup_class(cls):
        _test_command([])

    # Individual methods that implement a command

    def _create_project(self, project_name, parent_path=None):
        command = "createproject"
        arguments = [command, "--name", project_name]
        if parent_path:
            arguments.append("--parent-project-path")
            arguments.append(parent_path)
        # classic doesn't have this arg arguments.append("--continue-if-exists")
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

    def _publish_args(self, file, name, tabbed=None):
        command = "publish"
        arguments = [command, file, "--name", name, "--overwrite"]
        return arguments

    def _publish_creds_args(
        self, arguments, db_user=None, db_pass=None, db_save=None, oauth_user=None, oauth_save=None
    ):
        if db_user:
            arguments.append("--db-username")
            arguments.append(db_user)
        if db_pass:
            arguments.append("--db-password")
            arguments.append(db_pass)
        if db_save:
            arguments.append("--save-db-password")
        if oauth_user:
            arguments.append("--oauth-username")
            arguments.append(oauth_user)
        if oauth_save:
            arguments.append("--save-oauth")
        return arguments

    def _delete_wb(self, file):
        command = "delete"
        arguments = [command, file]
        _test_command(arguments)

    def _delete_ds(self, file):
        command = "delete"
        arguments = [command, "--datasource", file]
        _test_command(arguments)

    def _get_view(self, wb_name_on_server, sheet_name, filename=None):
        server_file = "/views/" + wb_name_on_server + "/" + sheet_name
        command = "get"
        arguments = [command, server_file]
        if filename:
            arguments = arguments + ["--filename", filename]
        _test_command(arguments)

    def _get_custom_view(self):
        # TODO
        command = "get"

    def _get_view_with_filters(self):
        # TODO
        command = "get"

    def _get_workbook(self, server_file):
        command = "get"
        server_file = "/workbooks/" + server_file
        arguments = [command, server_file, "-f", "get_workbook.twbx"]
        _test_command(arguments)
        os.path.exists("get_workbook.twbx")

    def _get_datasource(self, server_file):
        command = "get"
        server_file = "/datasources/" + server_file
        arguments = [command, server_file]
        _test_command(arguments)

    def _create_extract(self, type, wb_name):
        command = "createextracts"
        arguments = [command, type, wb_name, "--encrypt"]
        _test_command(arguments)

    # variation: url
    def _refresh_extract(self, type, wb_name):
        command = "refreshextracts"
        arguments = [command, wb_name]  # should not need -w
        try:
            _test_command(arguments)
        except Exception as e:
            print(e)
            print("expected (tabcmd classic)")
            print("  *** Unexpected response from the server: Bad request")
            print("This refresh extracts operation is not allowed for workbook World Indicators (errorCode=80030)")

    def _delete_extract(self, type, item_name):
        command = "deleteextracts"
        arguments = [command, type, item_name, "--include-all"]
        try:
            _test_command(arguments)
        except Exception as e:
            print(e)
            print("Expected (tabcmd classic:")
            print("*** Unexpected response from the server: Unable to load Data Source")
            print("Remove extract operation failed. (errorCode=310028)")
            print("8530479: Remove Extract is not supported for this Datasources (errorCode=310030)")

    def _list(self, item_type: str):
        command = "list"
        arguments = [command, item_type]
        _test_command(arguments)

    # actual tests
    TWBX_FILE_WITH_EXTRACT = "WorkbookWithExtract.twbx"
    TWBX_WITH_EXTRACT_NAME = "WorkbookWithExtract"
    TWBX_WITH_EXTRACT_SHEET = "Sheet1"

    TWBX_FILE_WITHOUT_EXTRACT = "simple-data.twbx"
    TWBX_WITHOUT_EXTRACT_NAME = "WorkbookWithoutExtract"
    TWBX_WITHOUT_EXTRACT_SHEET = "Testsheet1"

    TDSX_WITH_EXTRACT_NAME = "WorldIndicators"
    TDSX_FILE_WITH_EXTRACT = "World Indicators.tdsx"
    # fill in
    TDS_FILE_LIVE_NAME = ""
    TDS_FILE_LIVE = ""
    # only works on linux servers, need to also publish the datasource
    TWB_WITH_EMBEDDED_CONNECTION = "embedded_connection_waremart.twb"
    EMBEDDED_TWB_NAME = "waremart"



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
        # classic doesn't have this arg arguments.append("--continue-if-exists")
        _test_command(arguments)

    @pytest.mark.order(4)
    def test_users_add_to_group(self):
        if not server_admin and not site_admin:
            pytest.skip("Must be server or site administrator to add to groups")

        groupname = group_name
        command = "addusers"
        filename = os.path.join("tests", "assets", "usernames.csv")
        arguments = [command, groupname, "--users", filename]
        # classic doesn't have this arg arguments.append("--continue-if-exists")
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
        self._create_project(default_project_name)
        time.sleep(indexing_sleep_time)
        # project 2
        self._create_project("project_name_2", default_project_name)
        time.sleep(indexing_sleep_time)
        # project 3
        parent_path = "{0}/{1}".format(default_project_name, "project_name_2")
        self._create_project(default_project_name, parent_path)
        time.sleep(indexing_sleep_time)

    @pytest.mark.order(8)
    def test_list_projects(self):
        pytest.skip("not for tabcmd classic")
        self._list("projects")

    @pytest.mark.order(8)
    def test_list_flows(self):
        pytest.skip("not for tabcmd classic")
        self._list("flows")

    @pytest.mark.order(8)
    def test_list_workbooks(self):
        pytest.skip("not for tabcmd classic")
        self._list("workbooks")

    @pytest.mark.order(10)
    def test_delete_projects(self):
        if not project_admin:
            pytest.skip("Must be project administrator to create projects")
        self._delete_project("project_name_2", default_project_name)  # project 2
        self._delete_project(default_project_name)

    @pytest.mark.order(10)
    def test_wb_publish(self):
        file = os.path.join("tests", "assets", OnlineCommandTest.TWBX_FILE_WITH_EXTRACT)
        arguments = self._publish_args(file, OnlineCommandTest.TWBX_WITH_EXTRACT_NAME)
        _test_command(arguments)

    @pytest.mark.order(11)
    def test_wb_get(self):
        # add .twbx to the end to tell the server what we are getting
        self._get_workbook(OnlineCommandTest.TWBX_WITH_EXTRACT_NAME + ".twbx")

    @pytest.mark.order(11)
    def test_view_get_pdf(self):
        wb_name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        sheet_name = OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET
        # bug in tabcmd classic: doesn't work without download name
        # verify that the download works with a . in the file path
        self._get_view(wb_name_on_server, sheet_name, "c://users//jac.fitzgerald//Documents//downloaded_file.pdf")
        # self._get_view(wb_name_on_server, sheet_name, "downloaded_file.pdf")

    @pytest.mark.order(11)
    def test_view_get_csv(self):
        wb_name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        sheet_name = OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET
        self._get_view(wb_name_on_server, sheet_name + ".csv")

    @pytest.mark.order(11)
    def test_view_get_png(self):
        wb_name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        sheet_name = OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET
        self._get_view(wb_name_on_server, sheet_name + ".png")

    @pytest.mark.order(11)
    def test_wb_publish_embedded(self):
        pytest.skip("Waremart datasource is not available")
        file = os.path.join("tests", "assets", OnlineCommandTest.TWB_WITH_EMBEDDED_CONNECTION)
        arguments = self._publish_args(file, OnlineCommandTest.EMBEDDED_TWB_NAME)
        arguments = self._publish_creds_args(arguments, waremart_user, waremart_password, True)
        _test_command(arguments)

    @pytest.mark.order(12)
    def test_publish_ds(self):
        file = os.path.join("tests", "assets", OnlineCommandTest.TDSX_FILE_WITH_EXTRACT)
        arguments = self._publish_args(file, OnlineCommandTest.TDSX_WITH_EXTRACT_NAME)
        _test_command(arguments)

    @pytest.mark.order(12)
    def test_publish_ds_replace(self):
        file = os.path.join("tests", "assets", OnlineCommandTest.TDSX_FILE_WITH_EXTRACT)
        arguments = self._publish_args(file, OnlineCommandTest.TDSX_WITH_EXTRACT_NAME, "--replace")
        _test_command(arguments)

    @pytest.mark.order(12)
    def test_publish_ds_append(self):
        file = os.path.join("tests", "assets", OnlineCommandTest.TDSX_FILE_WITH_EXTRACT)
        arguments = self._publish_args(file, OnlineCommandTest.TDSX_WITH_EXTRACT_NAME, "--append")
        _test_command(arguments)

    @pytest.mark.order(12)
    def test_publish_live_ds(self):
        if not OnlineCommandTest.TDS_FILE_LIVE:
            pytest.skip("No live datasource to publish")
        file = os.path.join("tests", "assets", OnlineCommandTest.TDS_FILE_LIVE)
        arguments = self._publish_args(file, OnlineCommandTest.TDS_FILE_LIVE_NAME)
        _test_command(arguments)

    @pytest.mark.order(13)
    def test__get_ds(self):
        self._get_datasource(OnlineCommandTest.TDSX_WITH_EXTRACT_NAME + ".tdsx")

    @pytest.mark.order(13)
    def test_refresh_ds_extract(self):
        self._refresh_extract("-d", OnlineCommandTest.TDSX_WITH_EXTRACT_NAME)

    @pytest.mark.order(14)
    def test_delete_extract(self):
        self._delete_extract("-d", OnlineCommandTest.TDSX_WITH_EXTRACT_NAME)

    @pytest.mark.order(16)
    def test_create_extract(self):
        if not OnlineCommandTest.TDS_FILE_LIVE:
            pytest.skip("No live datasource to publish")
        self._create_extract("-d", OnlineCommandTest.TDS_FILE_LIVE_NAME)

    @pytest.mark.order(17)
    def test_refresh_wb_extract(self):
        self._refresh_extract("-w", OnlineCommandTest.TWBX_WITH_EXTRACT_NAME)

    @pytest.mark.order(19)
    def test_wb_delete(self):
        name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        self._delete_wb(name_on_server)

    @pytest.mark.order(19)
    def test__delete_ds(self):
        name_on_server = OnlineCommandTest.TDSX_WITH_EXTRACT_NAME
        self._delete_ds(name_on_server)

    @pytest.mark.order(19)
    def test__delete_ds_live(self):
        if not OnlineCommandTest.TDS_FILE_LIVE:
            pytest.skip("No live datasource to publish")
        name_on_server = OnlineCommandTest.TDS_FILE_LIVE_NAME
        self._delete_ds(name_on_server)

    @pytest.mark.order(19)
    def test_export_wb_pdf(self):
        command = "export"
        friendly_name = (
            OnlineCommandTest.TWBX_WITH_EXTRACT_NAME + "/" + OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET + "?param1=3"
        )
        arguments = [command, friendly_name, "--fullpdf", "-f", "exported_wb.pdf"]
        _test_command(arguments)

    @pytest.mark.order(19)
    def test_export_view_pdf(self):
        command = "export"
        friendly_name = (
            OnlineCommandTest.TWBX_WITH_EXTRACT_NAME + "/" + OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET + "?param1=3"
        )
        arguments = [command, friendly_name, "--pdf", "-f", "exported_view.pdf"]
        _test_command(arguments)

    @pytest.mark.order(20)
    def test_delete_site_users(self):
        if not server_admin and not site_admin:
            pytest.skip("Must be server or site administrator to delete site users")

        command = "deletesiteusers"
        users = os.path.join("tests", "assets", "usernames.csv")
        _test_command([command, users])

    @pytest.mark.order(21)
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
