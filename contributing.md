
# For developers
* [Install tabcmd](#install-tabcmd)
* [Contributing](#contributing)
* [Development](#development)
  * [Dev scripts](#dev-scripts) 
  * [Why Python\?](#why-python)
  * [Project structure](#project-structure)
  * [To add a new command](#to-add-a-new-command)
  * [Localization](#localization)
* [Releases](#releases)
  * [Versioning](#versioning)
  * [Packaging](#packaging)


These instructions are for people who want to download the code and edit it directly. If you are interested in tabcmd but not the code, see [here](Readme.md).
####To work with tabcmd, you need to have **Python 3.7+** installed.


## Contributing

Code contributions and improvements by the community are welcomed!

See the LICENSE file for current open-source licensing and use information. 

Before we can accept pull requests from contributors, we require a signed [Contributor License Agreement (CLA)](http://tableau.github.io/contributing.html).
 

## Development

### Dev scripts
To work on the tabcmd code, use these scripts.
_(note that running mypy and black is required for code being submitted to the repo)_


Recommended: create and activate a venv for development
> python -m venv my-dev
> my-dev/Scripts/activate  # or OS-specific call https://docs.python.org/3/library/venv.html
- build
> pip install build
> python -m build
- run tests
> pytest
- run tests against a live server
> python -m tabcmd login {your server info here}
> pytest -q tests\e2e\online_tests.py -r pfE
- autoformat your code with black (https://pypi.org/project/black/)
> black .
- check types 
> mypy tabcmd tests
- do test coverage calculation (https://coverage.readthedocs.io/en/6.3.2)
> bin/coverage.sh


### Why Python?

* Cross-platform
* Build on our existing Python [Tableau Server Client](https://github.com/tableau/server-client-python/)


### Project structure
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

### Localization

Strings are stored in /tabcmd/locales/[language]/*.properties by id and referred to in code as 
> string = _("string.id")

For runtime execution these files must be converted to .mo via .po
> doit mo


## Releases
To trigger publishing to pypi tag a commit on main with 'pypi'.
When pypi-release is done, begin the app smoke test action. 

### Versioning
Versioning is done with setuptools_scm and based on git tags. 
It will be a x.y.dev0 pre-release version except for commits with a new version tag. e.g
> git tag v2.0.4 && git push --tags

A new tag is created with the name of each release on github. 

### Packaging
First build the module
> python -m build
Before packaging, we produce a current metadata file to include in the bundle
> doit version 

Packaging is done with pyinstaller, which will build an executable for the platform it runs on. 
A github action runs on Mac, Windows and Linux to generate each executable: check package.yml for the OS-specific command line
> pyinstaller tabcmd-windows.spec .... 
 
Packaging produces executables in the dist folder. To run:
> dist/tabcmd/tabcmd.exe --help

