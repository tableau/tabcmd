import subprocess
import os
import pytest

try:
    from tests.e2e import credentials
except ImportError:
    credentials = None  # type: ignore

our_program = "tabcmd.exe"
launch_path = os.path.join("dist", "tabcmd")
exe = os.path.join(launch_path, our_program)
is_ready = False


class Setup:
    @staticmethod
    def login():
        if not credentials:
            pytest.skip("No credentials file found to run tests against a live server")

        # --server, --site, --username, --password
        args = [
            exe,
            "login",
            "--server",
            credentials.server,
            "--site",
            credentials.site,
            "--token",
            credentials.token,
            "--token-name",
            credentials.token_name,
            "--no-certcheck",
        ]
        print(args)
        return subprocess.check_call(args, stderr=subprocess.STDOUT, shell=True)

    @staticmethod
    def prechecks():
        global is_ready
        print("script is running in:")
        subprocess.check_call(["chdir"], shell=True)
        print("expecting built executable to be in " + launch_path + ":")
        subprocess.check_call(["dir", launch_path], shell=True)

        print("running", our_program)
        is_ready = True
