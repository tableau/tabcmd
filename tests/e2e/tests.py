import subprocess

from tests.e2e import setup_e2e
from tests.e2e import vars


def _test_command(test_args: list[str]):
    # this will raise an exception if it gets a non-zero return code
    # that should bubble up and fail the test?
    calling_args = [setup_e2e.exe] + test_args
    print(calling_args)
    return subprocess.check_call(calling_args)


def test_create_delete_group():
    command = "creategroup"
    arguments = [command, vars.group_name]
    _test_command(arguments)

    sleep(1)

    command = "deletegroup"
    arguments = [command, vars.group_name]
    _test_command(arguments)


def test_login():
    setup_e2e.prechecks()
    setup_e2e.login()


def test_create_delete_project():
        project_name = vars.project_name

        # project 1
        parent_path = project_name
        command = "createproject"
        arguments = [command, "--name", project_name]
        self._run_command(arguments)

        time.sleep(1)

        # project 2
        parent_path = project_name
        command = "createproject"
        arguments = [command, "--name", project_name, "--parent-project-path", parent_path]
        self._run_command(arguments)

        time.sleep(1)

        # project 3
        parent_path = "{0}/{1}".format(project_name, project_name)
        command = "createproject"
        arguments = [command, "--name", project_name, "--parent-project-path", parent_path]
        self._run_command(arguments)

        time.sleep(1)

        # delete project 2 (containing 3)
        command = "deleteproject"
        arguments = [command, project_name, "--parent-project-path", project_name]
        self._run_command(arguments)

        time.sleep(1)

        # delete project 1
        command = "deleteproject"
        arguments = [command, project_name]
        self._run_command(arguments)

    def test_list_sites(self):
        command = "listsites"
        try:
            self._run_command([command])
        except Exception as e:
            # often won't have permission for sites
            print(e)
