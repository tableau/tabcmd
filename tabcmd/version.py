from importlib.metadata import PackageNotFoundError, version as get_version

version: str = "unknown"
try:
    version = get_version("tabcmd")
except PackageNotFoundError:
    # importlib.metadata is unavailable in PyInstaller bundles; fall back to the
    # _version.py file that setuptools_scm writes at build time.
    try:
        from tabcmd._version import version
    except ImportError:
        version = "0.0"
