# Tabcmd2

![Tableau Supported](https://img.shields.io/badge/Support%20Level-Tableau%20Supported-53bd92.svg)


A Python based app that replicates the functionality of the existing TabCMD command line utility

* [Why Tabcmd2\?]()
* [Demo](#demo)
* [Get started](#get-started)
	* [Prerequisites](#prerequisites)
	* [Installation](#installation)
	* [Configuration](#configuration)
* [Run Tabcmd2]()
* [Support](#support)
* [Contributions](#contributions)

# Why Tabcmd2?

* Run Tabcmd commands on MacOS [Existing Tabcmd does not officially support
 MacOS]
* Authenticate using Personal Access Tokens [Existing Tabcmd does not support
 Personal Access Token Login]
* Easily use public endpoints available in Python based Tableau Server Client 
* Add more functionality and extend script for other automation tasks 

# Demo/Samples

> ....

# Get started

This section describes how to install and configure Tabcmd2.


## Prerequistes

To work with Tabcmd2, you need the following:

* MacOS/ Windows
* Python 3+ installed


## Installation

To install Tabcmd2, follow these steps:

1. Clone the repo
2. Run pip install . 


# Run

To run Tabcmd2, follow these steps:

1. To run a command:
    * tabcmd2 [command_name] [--flags]
    * Examples:
        * tabcmd2 login --username [username] --password [password] --server [server_name] --site [only_if_tableau_online]
        * tabcmd2 createproject --name [project_name]


# Available Commands
1. addusers (to group)
2. creategroup
3. createproject
4. createsite
5. createsiteusers
6. createusers
7. delete workbook-name or datasource-name
8. deletegroup
9. deleteproject
10. deletesite
11. deletesiteusers
12. deleteusers
13. editsite
14. export
15. listsites
16. login
17. logout
18. publish
19. publishsamples
20. removeusers


# Contributions


Code contributions and improvements by the community are welcomed!
See the LICENSE file for current open-source licensing and use information.

Before we can accept pull requests from contributors, we require a signed [Contributor License Agreement (CLA)](http://tableau.github.io/contributing.html),
