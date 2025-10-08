import importlib.metadata as libs

try:
    version = libs.version("tabcmd")
except libs.PackageNotFoundError:
    version = "2.0.0"
    pass
