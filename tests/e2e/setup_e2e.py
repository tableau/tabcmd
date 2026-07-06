import subprocess
import os

try:
    from tests.e2e import credentials  # type: ignore

    _has_credentials = True
except ImportError:
    credentials = {}  # type: ignore
    _has_credentials = False

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
    if _has_credentials:
        return [
            "--server",
            credentials.server,
            "--site",
            credentials.site,
            "--token-value",
            credentials.token,
            "--token-name",
            credentials.token_name,
        ]
    server = os.environ.get("E2E_SERVER")
    site = os.environ.get("E2E_SITE")
    token_name = os.environ.get("E2E_PATNAME")
    token = os.environ.get("E2E_PAT")
    if server and site and token_name and token:
        return ["--server", server, "--site", site, "--token-value", token, "--token-name", token_name]
    return None
