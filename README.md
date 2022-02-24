# Tabcmd

[![Tableau Supported](https://img.shields.io/badge/Support%20Level-Tableau%20Supported-53bd92.svg)](https://www.tableau.com/support-levels-it-and-developer-tools)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Tests](https://github.com/tableau/tabcmd/actions/workflows/run-tests/badge.svg)
![Coverage](https://github.com/tableau/tabcmd/actions/workflows/coverage/badge.svg)]

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

- run tests
> pytest
- with coverage calculation (https://coverage.readthedocs.io/en/6.3.2)
> coverage run -m pytest && coverage report -m

- autoformat your code with black (https://pypi.org/project/black/)
> black --line-length 120 tabcmd tests [--check]

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

### To add a new command
0. choose the single word that will be used as your command. Let's call this one `dream`
1. add parsers/dream_parser.py, and use methods from parent_parser to define the arguments
2. add commands/dreams/dream_command.py. It must have a method run_command.py(args) and the args object must contain all information needed from the user.
3. in map_of_parsers.py, add an entry for your new parser, like "dreams": DreamParser.dream_parser
4. in map_of_commands.py, add an entry for your new command, like "dream": ("dream", DreamCommand, "Think about picnics"),"
5. add tests! 