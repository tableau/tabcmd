import subprocess
import os

try:
    from tests.e2e import credentials  # type: ignore
except ImportError:
    credentials = {}  # type: ignore

our_program = "tabcmd.exe"
launch_path = os.path.join("dist", "tabcmd")
exe = os.path.join(launch_path, our_program)


def login(extra="--language", value="en"):
    if not credentials:
        return  # when run on github
    # --server, --site, --username, --password
    args = [
        "python",
        "-m",
        "tabcmd",
        "login",
        "--server",
        credentials.server,
        "--site",
        credentials.site,
        "--token-value",
        credentials.token,
        "--token-name",
        credentials.token_name,
        "--no-certcheck",
        extra,
        value,
    ]
    print(args)
    return subprocess.check_call(args, stderr=subprocess.STDOUT, shell=True)


def get_executable():
    print("script is running in:")
    subprocess.check_call(["chdir"], shell=True)
    print("expecting built executable to be in " + launch_path + ":")
    subprocess.check_call(["dir", launch_path], shell=True)
    print("running", our_program)
    return exe


def get_login_args():
    return [
        "--server",
        credentials.server,
        "--site",
        credentials.site,
        "--token-value",
        credentials.token,
        "--token-name",
        credentials.token_name
    ]
