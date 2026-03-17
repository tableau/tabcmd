from importlib.metadata import version as get_version, PackageNotFoundError

try:
    version = get_version("tabcmd")
except PackageNotFoundError:
    version = "2.0.0"
    pass
