import os
import pytest
import subprocess
import time
import unittest

from typing import Optional

try:
    from tests.e2e.credentials import database_password, database_user
except ModuleNotFoundError:
    database_user = None
    database_password = None
    print("Could not import datasource creds from credentials file")

from tests.e2e import setup_e2e


# to run this suite
# pytest -q tests/e2e/online_tests.py
# you can either run setup with a stored credentials file, or simply log in
# before running the suite so a session is active

debug_log = "--logging-level=DEBUG"
indexing_sleep_time = 1  # wait 1 second to confirm server has indexed updates

# object names: helpful if they are always unique
unique = str(time.gmtime().tm_sec)
group_name = "test-ing-group" + unique
workbook_name = "wb_1_" + unique
default_project_name = "Personal Work"  # "default-proj" + unique
parent_location = "parent" + unique
project_name = "test-proj-" + unique

# Flags to let us skip tests if we know we don't have the required access
server_admin = False
site_admin = False
project_admin = False
extract_encryption_enabled = False
use_tabcmd_classic = False  # toggle between testing using tabcmd 2 or tabcmd classic


def _test_command(test_args: list[str]):
    # this will raise an exception if it gets a non-zero return code
    # that will bubble up and fail the test

    # default: run tests using tabcmd 2
    calling_args = ["python", "-m", "tabcmd"] + test_args + [debug_log] + ["--no-certcheck"]

    # call the executable directly: lets us drop in classic tabcmd
    if use_tabcmd_classic:
        calling_args = (
            ["C:\\Program Files\\Tableau\\Tableau Server\\2023.3\\extras\\Command Line Utility\\tabcmd.exe"]
            + test_args
            + ["--no-certcheck"]
        )
    if database_password not in calling_args:
        print(calling_args)
    return subprocess.check_call(calling_args)


class OnlineCommandTest(unittest.TestCase):
    published = False
    gotten = False

    @classmethod
    def setup_class(cls):
        print("running python -m")
        # call this if we are using the built exe setup_e2e.prechecks()

    # Individual methods that implement a command

    def _create_project(self, project_name, parent_path=None):
        command = "createproject"
        arguments = [command, "--name", project_name]
        if parent_path:
            arguments.append("--parent-project-path")
            arguments.append(parent_path)
        if not use_tabcmd_classic:
            arguments.append("--continue-if-exists")
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

    def _publish_args(self, file, name, optional_args=None):
        command = "publish"
        arguments = [command, file, "--name", name, "--project", default_project_name, "--overwrite"]
        if optional_args:
            arguments.append(optional_args)
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

    def _delete_wb(self, name):
        command = "delete"
        arguments = [command, "--project", default_project_name, name]
        _test_command(arguments)

    def _delete_ds(self, name):
        command = "delete"
        arguments = [command, "--project", default_project_name, "--datasource", name]
        _test_command(arguments)

    def _get_view(self, wb_name_on_server, sheet_name, filename=None, additional_args=None):
        server_file = "/views/" + wb_name_on_server + "/" + sheet_name
        command = "get"
        arguments = [command, server_file]
        if filename:
            arguments = arguments + ["--filename", filename]
        if additional_args:
            arguments = arguments + additional_args
        _test_command(arguments)

    def _get_custom_view(self):
        # TODO
        command = "get"

    def _export_wb(self, friendly_name, filename=None, additional_args=None):
        command = "export"
        arguments = [command, friendly_name, "--fullpdf"]

        if filename:
            arguments = arguments + ["--filename", filename]
        if additional_args:
            arguments = arguments + additional_args
        _test_command(arguments)

    def _export_view(self, wb_name_on_server, sheet_name, export_type, filename=None, additional_args=None):
        server_file = "/" + wb_name_on_server + "/" + sheet_name
        command = "export"
        arguments = [command, server_file, export_type]
        if filename:
            arguments = arguments + ["--filename", filename]
        if additional_args:
            arguments = arguments + additional_args
        _test_command(arguments)

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
        arguments = [command, type, wb_name, "--project", default_project_name]
        if extract_encryption_enabled and not use_tabcmd_classic:
            arguments.append("--encrypt")
        _test_command(arguments)

    # variation: url
    def _refresh_extract(self, type, wb_name):
        command = "refreshextracts"
        arguments = [command, "-w", wb_name, "--project", default_project_name]  # bug: should not need -w
        try:
            _test_command(arguments)
        except Exception as e:
            print(e)
            if use_tabcmd_classic:
                print("expected (tabcmd classic)")
                print("  *** Unexpected response from the server: Bad request")
                print("This refresh extracts operation is not allowed for workbook World Indicators (errorCode=80030)")
            else:
                raise e

    def _delete_extract(self, type, item_name):
        command = "deleteextracts"
        arguments = [command, type, item_name, "--include-all", "--project", default_project_name]
        try:
            _test_command(arguments)
        except Exception as e:
            print(e)
            if use_tabcmd_classic:
                print("Expected (tabcmd classic):")
                print("*** Unexpected response from the server: Unable to load Data Source")
                print("Remove extract operation failed. (errorCode=310028)")
                print("8530479: Remove Extract is not supported for this Datasources (errorCode=310030)")
            else:
                raise e

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
    TDS_FILE_LIVE_NAME = "SampleDS"
    TDS_FILE_LIVE = "SampleDS.tds"

    TWB_WITH_EMBEDDED_CONNECTION = "EmbeddedCredentials.twb"
    EMBEDDED_TWB_NAME = "EmbeddedCredentials"

    @pytest.mark.order(1)
    def test_login(self):
        if use_tabcmd_classic:
            pytest.skip("not for tabcmd classic")
        try:
            # this will silently do nothing when run in github
            setup_e2e.login()
        except Exception as e:
            print(e)
            raise SystemExit(2)

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
        if not use_tabcmd_classic:
            arguments.append("--continue-if-exists")
        _test_command(arguments)

    @pytest.mark.order(4)
    def test_users_add_to_group(self):
        if not server_admin and not site_admin:
            pytest.skip("Must be server or site administrator to add to groups")

        groupname = group_name
        command = "addusers"
        filename = os.path.join("tests", "assets", "usernames.csv")
        arguments = [command, groupname, "--users", filename]
        if not use_tabcmd_classic:
            arguments.append("--continue-if-exists")
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
        if use_tabcmd_classic:
            pytest.skip("not for tabcmd classic")
        self._list("projects")

    @pytest.mark.order(8)
    def test_list_flows(self):
        if use_tabcmd_classic:
            pytest.skip("not for tabcmd classic")
        self._list("flows")

    @pytest.mark.order(8)
    def test_list_workbooks(self):
        if use_tabcmd_classic:
            pytest.skip("not for tabcmd classic")
        self._list("workbooks")

    @pytest.mark.order(8)
    def test_list_datasources(self):
        if use_tabcmd_classic:
            pytest.skip("not for tabcmd classic")
        self._list("datasources")

    @pytest.mark.order(10)
    def test_delete_projects(self):
        if not project_admin:
            pytest.skip("Must be project administrator to create projects")
        self._delete_project(parent_location)
        self._delete_project("project_name_2", default_project_name)  # project 2
        self._delete_project(default_project_name)

    @pytest.mark.order(10)
    def test_wb_publish(self):
        file = os.path.join("tests", "assets", OnlineCommandTest.TWBX_FILE_WITH_EXTRACT)
        arguments = self._publish_args(file, OnlineCommandTest.TWBX_WITH_EXTRACT_NAME)
        val = _test_command(arguments)
        if val != 0:
            print("publishing failed: cancel test run")
            exit(val)

    @pytest.mark.order(11)
    def test_wb_get(self):
        # add .twbx to the end to tell the server what we are getting
        self._get_workbook(OnlineCommandTest.TWBX_WITH_EXTRACT_NAME + ".twbx")

    @pytest.mark.order(11)
    def test_view_get_pdf(self):
        wb_name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        sheet_name = OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET
        # bug in tabcmd classic: doesn't work without download name
        self._get_view(wb_name_on_server, sheet_name, "downloaded_file.pdf")

    @pytest.mark.order(11)
    def test_view_get_png_sizes(self):
        wb_name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        sheet_name = OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET

        self._get_view(wb_name_on_server, sheet_name, "get_view_default_size.png")
        url_params = "?:size=100,200"
        self._get_view(wb_name_on_server, sheet_name + url_params, "get_view_sized_sm.png")
        url_params = "?:size=500,700"
        self._get_view(wb_name_on_server, sheet_name + url_params, "get_view_sized_LARGE.png")

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
        file = os.path.join("tests", "assets", OnlineCommandTest.TWB_WITH_EMBEDDED_CONNECTION)
        arguments = self._publish_args(file, OnlineCommandTest.EMBEDDED_TWB_NAME)
        arguments = self._publish_creds_args(arguments, database_user, database_password, True)
        arguments.append("--tabbed")
        arguments.append("--skip-connection-check")
        _test_command(arguments)

    @pytest.mark.order(12)
    def test_publish_ds(self):
        file = os.path.join("tests", "assets", OnlineCommandTest.TDSX_FILE_WITH_EXTRACT)
        arguments = self._publish_args(file, OnlineCommandTest.TDSX_WITH_EXTRACT_NAME)
        _test_command(arguments)

    @pytest.mark.order(12)
    def test_publish_live_ds(self):
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
        name_on_server = OnlineCommandTest.TDS_FILE_LIVE_NAME
        self._delete_ds(name_on_server)

    @pytest.mark.order(19)
    def test_export_wb_filters(self):
        wb_name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        sheet_name = OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET
        friendly_name = wb_name_on_server + "/" + sheet_name
        filters = ["--filter", "Product Type=Tea", "--fullpdf", "--pagelayout", "landscape"]
        self._export_wb(friendly_name, "filter_a_wb_to_tea_and_two_pages.pdf", filters)
        # NOTE: this test needs a visual check on the returned pdf to confirm the expected appearance

    @pytest.mark.order(19)
    def test_export_wb_pdf(self):
        wb_name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        friendly_name = wb_name_on_server + "/" + OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET
        filename = "exported_wb.pdf"
        self._export_wb(friendly_name, filename)

    @pytest.mark.order(19)
    def test_export_data_csv(self):
        wb_name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        sheet_name = OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET
        self._export_view(wb_name_on_server, sheet_name, "--csv", "exported_data.csv")

    @pytest.mark.order(19)
    def test_export_view_png(self):
        wb_name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        sheet_name = OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET
        self._export_view(wb_name_on_server, sheet_name, "--png", "export_view.png")

    @pytest.mark.order(19)
    def test_export_view_pdf(self):
        wb_name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        sheet_name = OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET
        self._export_view(wb_name_on_server, sheet_name, "--pdf", "export_view_pdf.pdf")

    @pytest.mark.order(19)
    def test_export_view_filtered(self):
        wb_name_on_server = OnlineCommandTest.TWBX_WITH_EXTRACT_NAME
        sheet_name = OnlineCommandTest.TWBX_WITH_EXTRACT_SHEET
        filename = "view_with_filters.pdf"

        filters = ["--filter", "Product Type=Tea"]
        self._export_view(wb_name_on_server, sheet_name, "--pdf", filename, filters)

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

        result = True
        command = "listsites"
        try:
            _test_command([command])
        except Exception as E:
            result = False
        assert result
