# Tabcmd

[![Tableau Supported](https://img.shields.io/badge/Support%20Level-Tableau%20Supported-53bd92.svg)](https://www.tableau.com/support-levels-it-and-developer-tools)

An open source Python based app that replicates the functionality of the existing [Tabcmd command line utility](https://help.tableau.com/current/server/en-us/tabcmd.htm).

**Important Note:** tabcmd is a work in progress ("beta") which may be useful for test and development purposes, but is not yet recommended for production environments.


## For user documentation see https://tableau.github.io/tabcmd/

## For developers

* [Why Python\?](#why-python)
* [Get started](#get-started)
* [Contributing](#contributing)

## Why Python?

* Cross-platform
* Build on our existing Python [Tableau Server Client](https://github.com/tableau/server-client-python/)

## Get started

####To work with tabcmd, you need to have **Python 3.7+** installed.

To install tabcmd, follow these steps:

1. Clone the repo
2. Run `pip install .`

- build
> python setup.py build

- run tests:
> python setup.py test (deprecated)
> pytest

- style is enforced with pycodestyle, mostly using default settings. https://www.mankier.com/1/pycodestyle
> pycodestyle tabcmd tests

- packaging is done with pyinstaller. You can only build an executable for the platform you build on.
> pyinstaller tabcmd.py --clean --noconfirm

produces dist/tabcmd.exe
To run tabcmd during development, from a console window in the same directory as the file tabcmd.py:


> dist/tabcmd/tabcmd.exe --help

or 
* `python -m tabcmd.py [command_name] [--flags]`
    * Examples:
        * `tabcmd.py login --username [username] --password [password] --server [server_name] --site [site_name]`
        * `tabcmd.py createproject --name [project_name]`
        * `tabcmd.py help`
        
For more examples and information about the available commands and options, see the user documentation


## Contributions

Code contributions and improvements by the community are welcomed!

See the LICENSE file for current open-source licensing and use information. 

Before we can accept pull requests from contributors, we require a signed [Contributor License Agreement (CLA)](http://tableau.github.io/contributing.html).


## Project structure
The core design principles for this app are
- it must provide the functionality  of the instance of tabcmd, with drop-in replacement CLI options
- it should be able to call [tsc](https://github.com/tableau/server-client-python/) for all server actions
- architecture is as simple as possible

1. tabcmd.py exists only as a module entry point that calls TabCmdController.
2. the 'parsers' module contains only argument and option definitions, no logic.
3. the 'commands' module contains the logic required to translate the tabcmd CLI interface into calls to tsc. This is completely dissociated from the parsers, and could theoretically be called from a completely different interface.
4. The 'execution' module is the core logic. TabcmdController gets an argparse parser, then attaches all the defined parsers to it and associates one command with each parser.