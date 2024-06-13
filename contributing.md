
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


## Install Tabcmd
> [!NOTE]
> These instructions are for people who want to work with the python code behind tabcmd. If you are interested in tabcmd but not the code, see [here](Readme.md).

####To work with tabcmd, you need to have **Python 3.8+** installed. To propose changes, you must have a Github account.

### To make changes to tabcmd code

Fork the tabcmd repo and create a branch off the **development** branch, not the default branch (named main) [(See Github Docs)](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)


### As a library that you can use in another application:

To install the current release:
```shell
pip install tabcmd
```

Or install the current work-in-progress version from Git\
*Only do this if you know you want the development version, no guarantee that we won't break APIs during development*

```shell
pip install git+https://github.com/tableau/tabcmd.git@development
```

> [!TIP]
> If you want to switch back to the non-development version, you need to run the following command before installing the stable version:
>
>```shell
>pip uninstall tabcmd
>```

## Software design

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

#### To add a new command
0. choose the single word that will be used as your command. Let's call this one `dream`
1. add parsers/dream_parser.py, and use methods from parent_parser to define the arguments
2. add commands/dreams/dream_command.py. It must have a method run_command.py(args) and the args object must contain all information needed from the user.
3. in map_of_parsers.py, add an entry for your new parser, like "dreams": DreamParser.dream_parser
4. in map_of_commands.py, add an entry for your new command, like "dream": ("dream", DreamCommand, "Think about picnics"),"
5. add tests!

## Contributing

Code contributions and improvements by the community are welcomed!

See the LICENSE file for current open-source licensing and use information. 

Before we can accept pull requests from contributors, we require a signed [Contributor License Agreement (CLA)](http://tableau.github.io/contributing.html).
 

## Developing
To work on the tabcmd code, use these scripts.
_(note that running mypy and black with no errors is required before code will be merged into the repo)_

- build and run
> pip install build
> python setup.py build
> python -m tabcmd.py [command_name] [--flags]

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


### Packaging 
- build an executable package with [pyinstaller](https://github.com/pyinstaller/pyinstaller). 
> [!NOTE]
> You can only build an executable for the platform you are running pyinstaller on. The spec for each platform is stored in tabcmd-*platform*.spec and the exact build commands for each platform can be checked in [our packaging script](.github/workflows//package.yml).

e.g for Windows
> pyinstaller tabcmd-windows.spec --clean --noconfirm --distpath ./dist/windows

produces dist/tabcmd.exe
To run the newly created executable, from a console window in the same directory as the file tabcmd.py:

> dist/tabcmd/tabcmd.exe --help



### Localization

Strings are stored in /tabcmd/locales/[language]/*.properties by id and referred to in code as 
> string = _("string.id")

For runtime execution these files must be converted from .properties -> .po -> .mo files. These .mo files will be bundled in the the package by pyinstaller. The entire conversion action is done by a .doit script:
> doit mo

### Versioning

Versioning is done with setuptools_scm and based on git tags. The version number will be x.y.dev0.dirty except for commits with a new version tag.
 This is pulled from the git state, and to get a clean version like "v2.1.0", you must be on a commit with the tag "v2.1.0" (Creating a Github release also creates a tag on the selected branch.) 
The version reflected in the executable (tabcmd -v) is stored in a metadata file created by a .doit script:
> doit version

## Release process

1. Create a new Github project release manually: https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
    - include a useful list of changes since the last release
    - include a clear list of remaining non-server-admin functional gaps

1. This will trigger our github packaging action to run on 3 different OSs.
    - write an updated metadata file with the correct version number.
    - build the python wheel
    - run pyinstaller to create executables
    - save the executable as an artifact on that job.

1. Find the artifacts created by this job and manually copy them to the new release. (Beware! of what the file type is, github does something weird with zipping it if you download with curl etc. TODO: automate workflow with a github action)

1. To trigger publishing to pypi run the manual workflow on main with 'pypi'. (TODO: automate trigger)

1. When the packages are available on pypi, you can run the 'Pypi smoke test action'. This action will also be run every 24 hours to validate doing pip install. (TODO: automate the after-release trigger)


