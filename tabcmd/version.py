from importlib.metadata import PackageNotFoundError, version as get_version

version: str = "unknown"
try:
    version = get_version("tabcmd")
except PackageNotFoundError:
    version = "2.0.0"
