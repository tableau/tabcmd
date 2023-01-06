# when we drop python 3.8, this could be replaced with this lighter weight option
# from importlib.metadata import version, PackageNotFoundError
from pkg_resources import get_distribution, DistributionNotFound

try:
    version = get_distribution("tabcmd").version
except DistributionNotFound:
    version = "2.0.0"
    pass
