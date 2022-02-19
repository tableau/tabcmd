import os
import subprocess
from tests.e2e import credentials

"""
This script expects an executable to have been built by pyinstaller
> pyinstaller tabcmd.py --clean --noconfirm
"""
our_program = "tabcmd.exe"
launch_path = os.path.join("dist", "tabcmd")
exe = os.path.join(launch_path, our_program)


def login():
    # --server, --site, --username, --password
    args = [exe, "login", "--server", credentials.SERVER_URL, "--site", credentials.SITE_NAME,
            "--token", credentials.PAT, "--token-name", credentials.PAT_NAME, "--no-certcheck"]
    print(args)
    return subprocess.check_call(args, stderr=subprocess.STDOUT, shell=True)


def prechecks():
    print("script is running in:")
    subprocess.check_call(["chdir"], shell=True)
    print("expecting built executable to be in " + launch_path + ":")
    subprocess.check_call(["dir", launch_path], shell=True)

    print("running", our_program)


if __name__ == "__main__":
    prechecks()
    login()
