import sys
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

# Only install pytest and runner when test command is run
# This makes work easier for offline installs or low bandwidth machines
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []
test_requirements = ['mock', 'pycodestyle', 'pytest', 'requests-mock>=1.0,<2.0', 'pyinstaller']

setup(
    name="tabcmd",
    author="Tableau",
    author_email="github@tableau.com",
    description="A command line client for working with Tableau Server.",
    long_description="A command line client for working with Tableau Server.",
    license="MIT",
    url="https://github.com/tableau/tabcmd",
    python_requires=">=3.7",
    packages=find_packages(),
    package_data={"tabcmd": ["src.locales/**/*.mo"]},
    include_package_data=True,
    entry_points={"console_scripts": ["tabcmd = src.tabcmd:main"]},
    setup_requires=[
        # copy of pyproject.toml for back compat
        "build",
        "setuptools>=62",
        "setuptools_scm>=6.2",
        "wheel",
    ],
    install_requires=[
        "polling2",
        "requests>=2.11,<3.0",
        "tableauserverclient>=0.19",
        "urllib3>=1.24.3,<2.0",
    ],
    extras_require={
        "localize": [
            "doit",
            "ftfy",
        ],
        "build": [
            "appdirs",
            "black",
            "doit",
            "ftfy",
            "mypy",
            "pyinstaller_versionfile",
            "setuptools>=62",
            "setuptools_scm",
            "types-appdirs",
            "types-mock",
            "types-requests",
            "types-setuptools",
        ],
        "package": [
            "pyinstaller>=5.1",
            "pyinstaller-versionfile",
        ],
        "test": [
            "mock",
            "pytest",
            "pytest-cov",
            "pytest-order",
            "pytest-runner",
            "requests-mock>=1.0,<2.0",
        ],
    },
    test_suite="tests",
    zip_safe=False,
)
