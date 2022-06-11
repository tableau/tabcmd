import pytest
import time
import subprocess
import unittest

from . import setup_e2e

debug_log = "--logging-level=DEBUG"
no_ssl = "--no-certcheck"
indexing_sleep_time = 1  # wait 1 second to confirm server has indexed updates

project_name = "not-default-name"
group_name = "test-ing-group"
workbook_name = "namebasic"

executable = ["python", "-m", "tabcmd"]
# if we want to test the pyinstaller exe
# executable = setup_e2e.Setup.get_executable()


@pytest.fixture(scope="module", autouse=True)
def log_in():
    setup_e2e.login()


# This is where you put tests that require server admin roles/on-prem server
def _test_command(test_args: list[str]):
    # this will raise an exception if it gets a non-zero return code
    # that should bubble up and fail the test?
    calling_args = executable + test_args + [debug_log] + [no_ssl]
    print(calling_args)
    return subprocess.check_call(calling_args)


class E2ETests(unittest.TestCase):
    def test_create_delete_group(self):
        command = "creategroup"
        arguments = [command, group_name]
        _test_command(arguments)

        time.sleep(1)

        command = "deletegroup"
        arguments = [command, group_name]
        _test_command(arguments)

    def test_create_delete_project(self):
        # project 1
        parent_path = project_name
        command = "createproject"
        arguments = [command, "--name", project_name]
        _test_command(arguments)

        time.sleep(indexing_sleep_time)

        # project 2
        parent_path = project_name
        command = "createproject"
        arguments = [command, "--name", project_name, "--parent-project-path", parent_path]
        _test_command(arguments)

        time.sleep(indexing_sleep_time)

        # project 3
        parent_path = "{0}/{1}".format(project_name, project_name)
        command = "createproject"
        arguments = [command, "--name", project_name, "--parent-project-path", parent_path]
        _test_command(arguments)

        time.sleep(indexing_sleep_time)

        # delete project 2 (containing 3)
        command = "deleteproject"
        arguments = [command, project_name, "--parent-project-path", project_name]
        _test_command(arguments)

        time.sleep(indexing_sleep_time)

        # delete project 1
        command = "deleteproject"
        arguments = [command, project_name]
        _test_command(arguments)

    def test_list_sites(self):
        command = "listsites"
        try:
            _test_command([command])
        except Exception as e:
            # often won't have permission for sites
            print(e)

    def test_create_extract(self):
        command = "createextracts"
        arguments = [command, "-d", "Regional", "--project", "Samples", "--encrypt"]
        _test_command(arguments)

    def test_publish_export(self):
        command = "publish"
        local_file = "tests/assets/SampleWB.twbx"
        arguments = [command, local_file]
        _test_command(arguments)
        # TODO: export and get the file we just published
