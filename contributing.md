
# For developers
* [Install tabcmd](#install-tabcmd)
* [Run tabcmd](#run-tabcmd)
* [Development commands](#development-commands)
* [Contributing](#contributing)
* [To add a new command](#to-add-a-new-command)
* [Why Python\?](#why-python)
* [Project Structure](#project-structure)



## Install tabcmd
These instructions are only necessary if you want to download the code and run it directly. If you are interested in tabcmd but not the code, see [here](Readme.md).
####To work with tabcmd, you need to have **Python 3.7+** installed.

### 



## Development

To work on the tabcmd code, use these scripts. On Windows, 
_(note that running mypy and black is required for code being submitted to the repo)_

- build
> python setup.py build
- run tests
> pytest
- run tests against a live server
> python -m tabcmd login {your server info here}
> bin/e2e.sh
- autoformat your code with black (https://pypi.org/project/black/)
> bin/black.sh
- check types 
> mypy tabcmd tests
- do test coverage calculation (https://coverage.readthedocs.io/en/6.3.2)
> bin/coverage.sh

- packaging is done with pyinstaller. You can only build an executable for the platform you build on.
> bin/pyinstaller.sh

 Packaging produces dist/tabcmd.exe (or equivalent)
- Run the package
> dist/tabcmd/tabcmd.exe --help


## Why Python?

* Cross-platform
* Build on our existing Python [Tableau Server Client](https://github.com/tableau/server-client-python/)


## Contributing

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

## To add a new command
0. choose the single word that will be used as your command. Let's call this one `dream`
1. add parsers/dream_parser.py, and use methods from parent_parser to define the arguments
2. add commands/dreams/dream_command.py. It must have a method run_command.py(args) and the args object must contain all information needed from the user.
3. in map_of_parsers.py, add an entry for your new parser, like "dreams": DreamParser.dream_parser
4. in map_of_commands.py, add an entry for your new command, like "dream": ("dream", DreamCommand, "Think about picnics"),"
5. add tests! 


