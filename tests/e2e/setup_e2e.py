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
    # --server, --site, then a token or --username/--password
    args = ["python", "-m", "tabcmd", "login"] + get_login_args() + ["--no-certcheck", extra, value]
    print(args)
    return subprocess.check_call(args, stderr=subprocess.STDOUT, shell=True)


def get_executable():
    print("script is running in:")
    subprocess.check_call(["chdir"], shell=True)
    print("expecting built executable to be in " + launch_path + ":")
    subprocess.check_call(["dir", launch_path], shell=True)
    print("running", our_program)
    return exe


def _auth_args(server, site, token_name=None, token=None, username=None, password=None):
    """Login arguments for a personal access token, or for a username and password. None if neither is complete."""
    if server is None or site is None:
        return None
    if token_name and token:
        return ["--server", server, "--site", site, "--token-value", token, "--token-name", token_name]
    if username and password:
        return ["--server", server, "--site", site, "--username", username, "--password", password]
    return None


def get_login_args():
    if _has_credentials:
        return _auth_args(
            getattr(credentials, "server", None),
            getattr(credentials, "site", None),
            getattr(credentials, "token_name", None),
            getattr(credentials, "token", None),
            getattr(credentials, "username", None),
            getattr(credentials, "password", None),
        )
    return _auth_args(
        os.environ.get("E2E_SERVER"),
        os.environ.get("E2E_SITE"),
        os.environ.get("E2E_PATNAME"),
        os.environ.get("E2E_PAT"),
        os.environ.get("E2E_USERNAME"),
        os.environ.get("E2E_PASSWORD"),
    )
