# Tabcmd

[![Tableau Supported](https://img.shields.io/badge/Support%20Level-Tableau%20Supported-53bd92.svg)](https://www.tableau.com/support-levels-it-and-developer-tools)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python tests](https://github.com/tableau/tabcmd/actions/workflows/run-tests.yml/badge.svg)](https://github.com/tableau/tabcmd/actions/workflows/run-tests.yml)
[![Pypi smoke tests](https://github.com/tableau/tabcmd/actions/workflows/python-app.yml/badge.svg)](https://github.com/tableau/tabcmd/actions/workflows/python-app.yml)

An open source, cross platform command-line utility which you can use to automate site administration tasks on your Tableau Server site. 


## Download exe (or rpm/deb)
* To download the latest release as an executable see https://github.com/tableau/tabcmd/releases
* There is no need to install: open a command line in the same folder as the exe and run
```shell
tabcmd [command_name] [--flags]
```
e.g 
* `tabcmd login --username [username] --password [password] --server [server_name] --site [site_name]`
* `tabcmd createproject --name [project_name]`
* `tabcmd help`

###or
## Install on the command line 

(Note: this requires Python 3.7+. Generally we will actively support versions of Python that are still in security support).

```shell
pip install tabcmd
```

Or install the current work-in-progress version from Git\
*Only do this if you know you want the development version, no guarantee that we won't break APIs during development*

```shell
pip install git+https://github.com/tableau/tabcmd.git@development
```

If you go this route, but want to switch back to the non-development version, you need to run the following command before installing the stable version:

```shell
pip uninstall tabcmd
```

### Run tabcmd

To run tabcmd from your local copy, from a console window in the same directory as the file tabcmd.py:

1. Clone the repo
2. Run `pip install .`

- build
> python setup.py build

- run tests
> pytest
- run tests against a live server
> python -m tabcmd login {your server info here}
> pytest -q tests\e2e\online_tests.py -r pfE
- with coverage calculation (https://coverage.readthedocs.io/en/6.3.2)
> coverage run -m pytest && coverage report -m

- autoformat your code with black (https://pypi.org/project/black/)
> black --line-length 120 tabcmd tests [--check]

- type check with mypy
> mypy tabcmd tests

- packaging is done with pyinstaller. You can only build an executable for the platform you build on.
- To package a release, we first bump the version with `doit version` and build as 2.x.0 before packaging
> pyinstaller tabcmd\tabcmd.py --clean --noconfirm

produces dist/tabcmd.exe
To run tabcmd during development, from a console window in the same directory as the file tabcmd.py:

> dist/tabcmd/tabcmd.exe --help

* `python -m tabcmd.py [command_name] [--flags]`
    * Examples:
        * `tabcmd.py login --username [username] --password [password] --server [server_name] --site [site_name]`
        * `tabcmd.py createproject --name [project_name]`
        * `tabcmd.py help`
        
For more examples and information about the available commands and options, 
see the user documentation at https://tableau.github.io/tabcmd/


## Release Notes
Version 2 is the first version of tabcmd built in python. 
It is specifically targeted to support users of Tableau Online, who are required to have MFA enabled. 
(MFA support is not available in the tabcmd program that ships with Tableau Server). 

Version 2 does not yet fully replace the existing tabcmd client, in particular it **does not support most server admin actions**.
For known gaps in supported functionality, see the latest [release notes](https://github.com/tableau/tabcmd/releases)

## About

Tabcmd has been shipped with Tableau Server, and for at least 2022 it will continue being shipped with new installs of Server. 
This new version of tabcmd can be updated for users at any time, without waiting for a new release of Server. 
Significant new features will only be added to this new version.

#### Which one do I have?
Copies of tabcmd that shipped with Tableau Server are referred to by the version number they shipped in: e.g. tabcmd 2020.4, tabcmd 2021.4, etc. The first version built in python is tabcmd 2.0. To see the version of your current tabcmd, run 

`tabcmd -v`

#### Will one of them go away? 
At some point in the future, tabcmd will no longer be included with Tableau Server. 
*We have no intention of breaking Server install flows.* 
If you have specific suggestions or concerns on what that will look like, feel free to open an issue here or a thread on the Community Forums.

