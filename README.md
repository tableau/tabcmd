# Tabcmd

[![Tableau Supported](https://img.shields.io/badge/Support%20Level-Tableau%20Supported-53bd92.svg)](https://www.tableau.com/support-levels-it-and-developer-tools)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An open source Python based app that replicates the functionality of the existing [Tabcmd command line utility](https://help.tableau.com/current/server/en-us/tabcmd.htm).

**Important Note:** tabcmd is a work in progress ("beta") which may be useful for test and development purposes, but is not yet recommended for production environments.

tabcmd.exe is available at ____
## For user documentation see https://tableau.github.io/tabcmd/


## For developers

* [Why Python\?](#why-python)
* [Get started](#get-started)
* [Contributing](#contributing)

## Why Python?

* Cross-platform
* Build on our existing Python [Tableau Server Client](https://github.com/tableau/server-client-python/)

## Get started

To install tabcmd, follow these steps:
0. To work with tabcmd, you need to have **Python 3.7** or higher installed, and pip
*see > https://pip.pypa.io/en/stable/installation/ *
1. Clone the repo and install the app
> $ git clone https://github.com/tableau/tabcmd.git
> 
> $ pip install .
2. run tests
> $ pytest
4. run tabcmd 
> $ python -m tabcmd.py [command_name] [--flags]`
    * Examples:
        * `tabcmd.py login --username [username] --password [password] --server [server_name] --site [site_name]`
        * `tabcmd.py createproject --name [project_name]`
        * `tabcmd.py help`
        
For more examples and information about the available commands and options, see the user documentation


Build scripts
- run tests against a live server (you must provide server info and credentials)
> $ python setup.py e2e
- run tests with coverage calculation (https://coverage.readthedocs.io/en/6.3.2)
> $ python setup.py coverage
- autoformat your code with black (https://pypi.org/project/black/)
> $ python setup.py check

- packaging is done with pyinstaller. You can only build an executable for the platform you build on.
> $ python setup.py make 

> $ dist/tabcmd/tabcmd.exe --help


## Contributions

Code contributions and improvements by the community are welcomed!

See the LICENSE file for current open-source licensing and use information. 

Before we can accept pull requests from contributors, we require a signed [Contributor License Agreement (CLA)](http://tableau.github.io/contributing.html).


## Project design
The core design principles for this app are
- it must provide the functionality  of the existing tabcmd program, with drop-in replacement CLI options
- it should be able to call [tsc](https://github.com/tableau/server-client-python/) for all server actions
- architecture is as simple as possible

1. tabcmd.py exists only as a module entry point that calls TabCmdController.
2. the 'commands' module contains the logic required to translate the tabcmd CLI interface into calls to tsc. This is completely dissociated from the parsers, and could theoretically be called from a completely different interface.
3. The 'execution' module is the core logic. TabcmdController gets an argparse parser, then attaches all the defined parsers to it and associates one command with each parser.

### To add a new command
0. choose the single word that will be used as your command. Let's call this one `dream`
1. add commands/dreams/dream_command.py, inheriting from Commands and implementing the given functions
2. in map_of_commands.py, add an entry for your new command
3. add tests! 
4. add new strings to ____ if required

### Localization
* We store strings in .properties files to fit the existing in-house localization process
* New strings must be manually assigned a label and added to the en-US file in the format
>"string.identifying.label": "the actual string"
* TODO define steps to get them back to loc team and fetch new updated files 
* We use prop2po to transform the properties file into .po files to use with gettext
* We use gettext to transform the .po files into .mo files
* Re-using strings is good, but only if the entire string can be re-used: do not create new strings by combining others.


