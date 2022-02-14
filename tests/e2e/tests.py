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
    setup_e2e.prechecks()
    setup_e2e.login()
    command = "creategroup"
    arguments = [command, vars.group_name]
    _test_command(arguments)

    # PAUSE FOR THOUGHT ?

    command = "deletegroup"
    arguments = [command, vars.group_name]
    _test_command(arguments)


if __name__ == "__main__":
    # expect that we are already logged in because user called setup_exe
    test_create_delete_group()