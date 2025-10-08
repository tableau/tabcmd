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

# config variables for test run
debug_log = "--logging-level=DEBUG"
indexing_sleep_time = 1  # wait 1 second to confirm server has indexed updates
# Flags to let us skip tests if we know we don't have the required access
server_admin = False
site_admin = True
project_admin = False
extract_encryption_enabled = False
use_tabcmd_classic = False  # toggle between testing using tabcmd 2 or tabcmd classic


default_project_name = "Personal Work"  # not unique, has to exist already when you run random test cases


class TestAssets:

    unique = str(time.gmtime().tm_sec)

    # names unique for each test run
    group_name = "test-ing-group" + unique
    parent_location = "parent" + unique

    # if we publish something with a name that already exists, it will get a random int appended to the name
    # to avoid this, we add our own random int to each name so we actually know what it is
    # this is why we have workbook_name+unique everywhere
    # BUG: this means you pretty much can't run a random individual test case without giving the already-unique name
    def get_publishable_name(file_value: str) -> str:
        return os.path.splitext(os.path.basename(file_value))[0] + TestAssets.unique

    # assets for tests - these files are kept in the repo in tests/assets
    TWBX_FILE_WITH_EXTRACT = "WorkbookWithExtract.twbx"
    TWBX_WITH_EXTRACT_SHEET = "Sheet1"

    TWBX_FILE_WITHOUT_EXTRACT = "WorkbookWithoutExtract.twbx"
    TWBX_WITHOUT_EXTRACT_SHEET = "Testsheet1"

    # problem:  803311: Remove Extract is not supported for this Datasources (errorCode=310030))
    TDSX_FILE_WITH_EXTRACT = "WorldIndicators.tdsx"
    # WorldIndicators.tds

    TDS_FILE_LIVE = "live_mysql.tds"

    TWB_FILE_WITH_EMBEDDED_CONNECTION = "EmbeddedCredentials.twb"

    USERS_DETAILS_FILE = "detailed_users.csv"
    USERNAMES_FILE = "usernames.csv"


def _test_command(test_args: list[str]):
    # this will raise an exception if it gets a non-zero return code
    # that will bubble up and fail the test

    # default: run tests using tabcmd 2
    calling_args = (
        ["python", "-m", "tabcmd"] + test_args + setup_e2e.get_login_args() + [debug_log] + ["--no-certcheck"]
    )

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


class TabcmdCall:

    # Individual methods that implement a command

    def _create_project(project_name, parent_path=None):
        command = "createproject"
        arguments = [command, "--name", project_name]
        if parent_path:
            arguments.append("--parent-project-path")
            arguments.append(parent_path)
        if not use_tabcmd_classic:
            arguments.append("--continue-if-exists")
        _test_command(arguments)

    def _delete_project(project_name, parent_path=None):
        command = "deleteproject"
        arguments = [command, project_name]
        if parent_path:
            arguments.append("--parent-project-path")
            arguments.append(parent_path)
        _test_command(arguments)

    def _publish_samples(project_name):
        command = "publishsamples"
        arguments = [command, "--name", project_name]
        _test_command(arguments)

    def _publish_args(file, name, optional_args=None):
        command = "publish"
        arguments = [command, file, "--name", name, "--project", default_project_name, "--overwrite"]
        if optional_args:
            arguments.append(optional_args)
        return arguments

    def _publish_creds_args(arguments, db_user=None, db_pass=None, db_save=None, oauth_user=None, oauth_save=None):
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

    def _delete_wb(name):
        command = "delete"
        arguments = [command, "--project", default_project_name, name]
        _test_command(arguments)

    def _delete_ds(name):
        command = "delete"
        arguments = [command, "--project", default_project_name, "--datasource", name]
        _test_command(arguments)

    def _get_view(wb_name_on_server, sheet_name, filename=None, additional_args=None):
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
        raise NotImplementedError("get_custom_view is not implemented")

    def _export_wb(friendly_name, filename=None, additional_args=None):
        command = "export"
        arguments = [command, friendly_name, "--fullpdf"]

        if filename:
            arguments = arguments + ["--filename", filename]
        if additional_args:
            arguments = arguments + additional_args
        _test_command(arguments)

    def _export_view(wb_name_on_server, sheet_name, export_type, filename=None, additional_args=None):
        server_file = "/" + wb_name_on_server + "/" + sheet_name
        command = "export"
        arguments = [command, server_file, export_type]
        if filename:
            arguments = arguments + ["--filename", filename]
        if additional_args:
            arguments = arguments + additional_args
        _test_command(arguments)

    def _get_workbook(server_file):
        command = "get"
        server_file = "/workbooks/" + server_file
        arguments = [command, server_file, "-f", "get_workbook.twbx"]
        _test_command(arguments)
        os.path.exists("get_workbook.twbx")

    def _get_datasource(server_file):
        command = "get"
        server_file = "/datasources/" + server_file
        arguments = [command, server_file]
        _test_command(arguments)

    def _create_extract(item_name, type="-w"):
        command = "createextracts"
        arguments = [command, type, item_name, "--project", default_project_name]
        if extract_encryption_enabled and not use_tabcmd_classic:
            arguments.append("--encrypt")
        _test_command(arguments)

    # variation: url
    def _refresh_extract(item_name, type="-w"):
        command = "refreshextracts"
        arguments = [command, type, item_name, "--project", default_project_name]  # bug: should not need -w
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

    def _delete_extract(item_name, type="-w"):
        command = "deleteextracts"
        arguments = [command, type, item_name, "--include-all", "--project", default_project_name]
        _test_command(arguments)

    def _list(item_type: str):
        command = "list"
        arguments = [command, item_type]
        _test_command(arguments)


# test cases that use the API calls
class OnlineCommandTest(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        print("running python -m")
        # call this if we are using the built exe setup_e2e.prechecks()

    # check for the required files in the test assets
    @pytest.mark.order(0)
    def test_asset_files_exist(self):
        assets_dir = os.path.join("tests", "assets")
        checks = [
            ("TWBX_FILE_WITH_EXTRACT", TestAssets.TWBX_FILE_WITH_EXTRACT),
            ("TWBX_FILE_WITHOUT_EXTRACT", TestAssets.TWBX_FILE_WITHOUT_EXTRACT),
            ("TDSX_FILE_WITH_EXTRACT", TestAssets.TDSX_FILE_WITH_EXTRACT),
            ("TDS_FILE_LIVE", TestAssets.TDS_FILE_LIVE),
            ("TWB_FILE_WITH_EMBEDDED_CONNECTION", TestAssets.TWB_FILE_WITH_EMBEDDED_CONNECTION),
        ]
        missing = []
        for var_name, filename in checks:
            path = os.path.join(assets_dir, filename)
            if not os.path.exists(path):
                missing.append(f"{var_name} -> {path}")
        assert not missing, "Missing asset files: " + ", ".join(missing)

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

    @pytest.mark.order(1)
    def test_publish_simple(self):
        file = os.path.join("tests", "assets", TestAssets.TWBX_FILE_WITHOUT_EXTRACT)
        name_on_server = TestAssets.get_publishable_name(TestAssets.TWBX_FILE_WITHOUT_EXTRACT)
        arguments = TabcmdCall._publish_args(file, name_on_server)
        _test_command(arguments)

    @pytest.mark.order(2)
    def test_users_create_site_users(self):
        if not server_admin and not site_admin:
            pytest.skip("Must be server or site administrator to create site users")
        command = "createsiteusers"
        users = os.path.join("tests", "assets", TestAssets.USERS_DETAILS_FILE)
        arguments = [command, users, "--role", "Publisher"]
        _test_command(arguments)

    @pytest.mark.order(3)
    def test_group_creategroup(self):
        if not server_admin and not site_admin:
            pytest.skip("Must be server or site administrator to create groups")
        groupname = TestAssets.group_name
        command = "creategroup"
        arguments = [command, groupname]
        if not use_tabcmd_classic:
            arguments.append("--continue-if-exists")
        _test_command(arguments)

    @pytest.mark.order(4)
    def test_users_add_to_group(self):
        if not server_admin and not site_admin:
            pytest.skip("Must be server or site administrator to add to groups")

        groupname = TestAssets.group_name
        command = "addusers"
        filename = os.path.join("tests", "assets", TestAssets.USERNAMES_FILE)
        arguments = [command, groupname, "--users", filename]
        if not use_tabcmd_classic:
            arguments.append("--continue-if-exists")
        _test_command(arguments)

    @pytest.mark.order(5)
    def test_users_remove_from_group(self):
        if not server_admin and not site_admin:
            pytest.skip("Must be server or site administrator to remove from groups")

        groupname = TestAssets.group_name
        command = "removeusers"
        filename = os.path.join("tests", "assets", TestAssets.USERNAMES_FILE)
        arguments = [command, groupname, "--users", filename]
        _test_command(arguments)

    @pytest.mark.order(6)
    def test_group_deletegroup(self):
        if not server_admin and not site_admin:
            pytest.skip("Must be server or site administrator to delete groups")

        groupname = TestAssets.group_name
        command = "deletegroup"
        arguments = [command, groupname]
        _test_command(arguments)

    @pytest.mark.order(8)
    def test_create_projects(self):
        if not project_admin and not server_admin and not site_admin:
            pytest.skip("Must be project administrator to create projects")

        # project 1
        TabcmdCall._create_project(TestAssets.parent_location)
        time.sleep(indexing_sleep_time)
        # project 1
        TabcmdCall._create_project(default_project_name)
        time.sleep(indexing_sleep_time)
        # project 2
        TabcmdCall._create_project("project_name_2", default_project_name)
        time.sleep(indexing_sleep_time)
        # project 3
        parent_path = "{0}/{1}".format(default_project_name, "project_name_2")
        TabcmdCall._create_project(default_project_name, parent_path)
        time.sleep(indexing_sleep_time)

    @pytest.mark.order(8)
    def test_list_projects(self):
        if use_tabcmd_classic:
            pytest.skip("not for tabcmd classic")
        TabcmdCall._list("projects")

    @pytest.mark.order(8)
    def test_list_flows(self):
        if use_tabcmd_classic:
            pytest.skip("not for tabcmd classic")
        TabcmdCall._list("flows")

    @pytest.mark.order(8)
    def test_list_workbooks(self):
        if use_tabcmd_classic:
            pytest.skip("not for tabcmd classic")
        TabcmdCall._list("workbooks")

    @pytest.mark.order(8)
    def test_list_datasources(self):
        if use_tabcmd_classic:
            pytest.skip("not for tabcmd classic")
        TabcmdCall._list("datasources")

    @pytest.mark.order(10)
    def test_delete_projects(self):
        if not project_admin:
            pytest.skip("Must be project administrator to create projects")
        TabcmdCall._delete_project(TestAssets.parent_location)
        TabcmdCall._delete_project("project_name_2", default_project_name)  # project 2
        self._delete_project(default_project_name)

    @pytest.mark.order(10)
    def test_wb_publish(self):
        for file in [TestAssets.TWBX_FILE_WITH_EXTRACT, TestAssets.TWBX_FILE_WITHOUT_EXTRACT]:
            file = os.path.join("tests", "assets", file)
            name_on_server = TestAssets.get_publishable_name(file)
            arguments = TabcmdCall._publish_args(file, name_on_server)
            val = _test_command(arguments)
            if val != 0:
                print(f"publishing {file} failed: cancel test run")
                exit(val)

    @pytest.mark.order(11)
    def test_wb_get(self):
        # add .twbx to the end to tell the server what we are getting
        name_on_server = TestAssets.get_publishable_name(TestAssets.TWBX_FILE_WITH_EXTRACT) + ".twbx"
        TabcmdCall._get_workbook(name_on_server)

    @pytest.mark.order(11)
    def test_view_get_pdf(self):
        wb_name_on_server = TestAssets.get_publishable_name(TestAssets.TWBX_FILE_WITH_EXTRACT)
        sheet_name = TestAssets.TWBX_WITH_EXTRACT_SHEET
        # bug in tabcmd classic: doesn't work without download name
        TabcmdCall._get_view(wb_name_on_server, sheet_name, "downloaded_file.pdf")

    @pytest.mark.order(11)
    def test_view_get_png_sizes(self):
        wb_name_on_server = TestAssets.get_publishable_name(TestAssets.TWBX_FILE_WITH_EXTRACT)
        sheet_name = TestAssets.TWBX_WITH_EXTRACT_SHEET

        TabcmdCall._get_view(wb_name_on_server, sheet_name, "get_view_default_size.png")
        url_params = "?:size=100,200"
        TabcmdCall._get_view(wb_name_on_server, sheet_name + url_params, "get_view_sized_sm.png")
        url_params = "?:size=500,700"
        TabcmdCall._get_view(wb_name_on_server, sheet_name + url_params, "get_view_sized_LARGE.png")

    @pytest.mark.order(11)
    def test_view_get_csv(self):
        wb_name_on_server = TestAssets.get_publishable_name(TestAssets.TWBX_FILE_WITH_EXTRACT)
        sheet_name = TestAssets.TWBX_WITH_EXTRACT_SHEET
        TabcmdCall._get_view(wb_name_on_server, sheet_name + ".csv")

    @pytest.mark.order(11)
    def test_view_get_png(self):
        wb_name_on_server = TestAssets.get_publishable_name(TestAssets.TWBX_FILE_WITH_EXTRACT)
        sheet_name = TestAssets.TWBX_WITH_EXTRACT_SHEET
        TabcmdCall._get_view(wb_name_on_server, sheet_name + ".png")

    @pytest.mark.order(11)
    def test_wb_publish_embedded(self):
        file = os.path.join("tests", "assets", TestAssets.TWB_FILE_WITH_EMBEDDED_CONNECTION)
        name_on_server = TestAssets.get_publishable_name(TestAssets.TWB_FILE_WITH_EMBEDDED_CONNECTION)
        arguments = TabcmdCall._publish_args(file, name_on_server)
        arguments = TabcmdCall._publish_creds_args(arguments, database_user, database_password, True)
        arguments.append("--tabbed")
        arguments.append("--skip-connection-check")
        _test_command(arguments)

    @pytest.mark.order(12)
    def test_publish_ds(self):
        file = os.path.join("tests", "assets", TestAssets.TDSX_FILE_WITH_EXTRACT)
        name_on_server = TestAssets.get_publishable_name(TestAssets.TDSX_FILE_WITH_EXTRACT)
        arguments = TabcmdCall._publish_args(file, name_on_server)
        _test_command(arguments)

    @pytest.mark.order(12)
    def test_publish_live_ds(self):
        file = os.path.join("tests", "assets", TestAssets.TDS_FILE_LIVE)
        name_on_server = TestAssets.get_publishable_name(TestAssets.TDS_FILE_LIVE)
        arguments = TabcmdCall._publish_args(file, name_on_server)
        _test_command(arguments)

    @pytest.mark.order(13)
    def test__get_ds(self):
        name_on_server = TestAssets.get_publishable_name(TestAssets.TDSX_FILE_WITH_EXTRACT)
        TabcmdCall._get_datasource(name_on_server + ".tdsx")

    @pytest.mark.order(13)
    def test_refresh_ds_extract(self):
        name_on_server = TestAssets.get_publishable_name(TestAssets.TDSX_FILE_WITH_EXTRACT)
        TabcmdCall._refresh_extract(name_on_server, "-d")

    @pytest.mark.order(14)
    def test_delete_extract(self):
        name_on_server = TestAssets.get_publishable_name(TestAssets.TDSX_FILE_WITH_EXTRACT)
        TabcmdCall._delete_extract(name_on_server, "-d")

    @pytest.mark.order(16)
    def test_create_extract(self):
        name_on_server = TestAssets.get_publishable_name(TestAssets.TDS_FILE_LIVE)
        TabcmdCall._create_extract(name_on_server, "-d")

    @pytest.mark.order(17)
    def test_refresh_wb_extract(self):
        name_on_server = TestAssets.get_publishable_name(TestAssets.TWBX_FILE_WITH_EXTRACT)
        TabcmdCall._refresh_extract(name_on_server, "-w")

    @pytest.mark.order(19)
    def test_export_wb_filters(self):
        wb_name_on_server = TestAssets.get_publishable_name(TestAssets.TWBX_FILE_WITH_EXTRACT)
        sheet_name = TestAssets.TWBX_WITH_EXTRACT_SHEET
        friendly_name = wb_name_on_server + "/" + sheet_name
        filters = ["--filter", "Product Type=Tea", "--fullpdf", "--pagelayout", "landscape"]
        TabcmdCall._export_wb(friendly_name, "filter_a_wb_to_tea_and_two_pages.pdf", filters)
        # NOTE: this test needs a visual check on the returned pdf to confirm the expected appearance

    @pytest.mark.order(19)
    def test_export_wb_pdf(self):
        wb_name_on_server = TestAssets.get_publishable_name(TestAssets.TWBX_FILE_WITH_EXTRACT)
        friendly_name = wb_name_on_server + "/" + TestAssets.TWBX_WITH_EXTRACT_SHEET
        filename = "exported_wb.pdf"
        TabcmdCall._export_wb(friendly_name, filename)

    @pytest.mark.order(19)
    def test_export_data_csv(self):
        wb_name_on_server = TestAssets.get_publishable_name(TestAssets.TWBX_FILE_WITH_EXTRACT)
        sheet_name = TestAssets.TWBX_WITH_EXTRACT_SHEET
        TabcmdCall._export_view(wb_name_on_server, sheet_name, "--csv", "exported_data.csv")

    @pytest.mark.order(19)
    def test_export_view_png(self):
        wb_name_on_server = TestAssets.get_publishable_name(TestAssets.TWBX_FILE_WITH_EXTRACT)
        sheet_name = TestAssets.TWBX_WITH_EXTRACT_SHEET
        TabcmdCall._export_view(wb_name_on_server, sheet_name, "--png", "export_view.png")

    @pytest.mark.order(19)
    def test_export_view_pdf(self):
        wb_name_on_server = TestAssets.get_publishable_name(TestAssets.TWBX_FILE_WITH_EXTRACT)
        sheet_name = TestAssets.TWBX_WITH_EXTRACT_SHEET
        TabcmdCall._export_view(wb_name_on_server, sheet_name, "--pdf", "export_view_pdf.pdf")

    @pytest.mark.order(19)
    def test_export_view_filtered(self):
        wb_name_on_server = TestAssets.get_publishable_name(TestAssets.TWBX_FILE_WITH_EXTRACT)
        sheet_name = TestAssets.TWBX_WITH_EXTRACT_SHEET
        filename = "view_with_filters.pdf"

        filters = ["--filter", "Product Type=Tea"]
        TabcmdCall._export_view(wb_name_on_server, sheet_name, "--pdf", filename, filters)

    @pytest.mark.order(20)
    def test_delete_site_users(self):
        if not server_admin and not site_admin:
            pytest.skip("Must be server or site administrator to delete site users")

        command = "deletesiteusers"
        users = os.path.join("tests", "assets", TestAssets.USERNAMES_FILE)
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

    @pytest.mark.order(30)
    def test_wb_delete(self):
        name_on_server = TestAssets.get_publishable_name(TestAssets.TWBX_FILE_WITH_EXTRACT)
        TabcmdCall._delete_wb(name_on_server)

    @pytest.mark.order(30)
    def test__delete_ds(self):
        name_on_server = TestAssets.get_publishable_name(TestAssets.TDSX_FILE_WITH_EXTRACT)
        TabcmdCall._delete_ds(name_on_server)

    @pytest.mark.order(30)
    def test__delete_ds_live(self):
        name_on_server = TestAssets.get_publishable_name(TestAssets.TDS_FILE_LIVE)
        TabcmdCall._delete_ds(name_on_server)
