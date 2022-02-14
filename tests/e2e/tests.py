import subprocess

from tests.e2e import setup_e2e
from tests.e2e import vars


def _test_command(test_args: list[str]):
    # this will raise an exception if it gets a non-zero return code
    # that should bubble up and fail the test?
    calling_args = [setup_e2e.exe] + test_args
    print(calling_args)
    return subprocess.check_call(calling_args)


# this test fails because we don't have the positional groupname implemented
"""
def test_create_delete_group():
    command = "creategroup"
    arguments = [command, vars.group_name]
    _test_command(arguments)

    command = "deletegroup"
    arguments = [command, vars.group_name]
    _test_command(arguments)
"""


def test_login():
    setup_e2e.prechecks()
    setup_e2e.login()


if __name__ == "__main__":
    test_login()
