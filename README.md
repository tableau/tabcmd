# Tabcmd

[![Tableau Supported](https://img.shields.io/badge/Support%20Level-Tableau%20Supported-53bd92.svg)](https://www.tableau.com/support-levels-it-and-developer-tools)

![Code Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/<user>/<gist-ID>/raw/coverage-badge.json)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python tests](https://github.com/tableau/tabcmd/actions/workflows/run-tests.yml/badge.svg)](https://github.com/tableau/tabcmd/actions/workflows/run-tests.yml)
[![Pypi smoke tests](https://github.com/tableau/tabcmd/actions/workflows/python-app.yml/badge.svg)](https://github.com/tableau/tabcmd/actions/workflows/python-app.yml)

An open source, cross platform command-line utility which you can use to automate activity on Tableau Cloud or Tableau Server.


## Download the app
* To download the latest release ready to use see https://github.com/tableau/tabcmd/releases
* There is no need to install: open a command line in the same folder as the exe and run


> [!TIP]
> You can also download the current latest release directly on the command line: 
> ```shell
> pip install tabcmd
> ```


### Run tabcmd

These commands can be run from the folder that you downloaded tabcmd. If you add this folder to your PATH, they can be run from any folder.
```shell
tabcmd [command_name] [--flags]
```
e.g 
* `tabcmd login --username [username] --password [password] --server [server_name] --site [site_name]`
* `tabcmd createproject --name [project_name]`
* `tabcmd help`


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

