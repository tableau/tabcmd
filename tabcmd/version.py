# Updated to use importlib.metadata (available in Python 3.8+, required >= 3.9)
from importlib.metadata import version, PackageNotFoundError

try:
    version = version("tabcmd")
except PackageNotFoundError:
    version = "2.0.0"
    pass
