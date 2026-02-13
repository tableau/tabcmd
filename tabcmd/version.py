from importlib.metadata import version, PackageNotFoundError

try:
    version = version("tabcmd")
except PackageNotFoundError:
    version = "2.0.0"
