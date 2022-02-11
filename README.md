# Tabcmd

[![Tableau Supported](https://img.shields.io/badge/Support%20Level-Tableau%20Supported-53bd92.svg)](https://www.tableau.com/support-levels-it-and-developer-tools)

A Python based app that replicates the functionality of the existing [Tabcmd command line utility](https://help.tableau.com/current/server/en-us/tabcmd.htm).

**Important Note:** tabcmd is a work in progress ("beta") which may be useful for test and development purposes, but is not yet recommended for production environments.

* [Why a Python based tabcmd\?](#whytabcmd)
* [Demo](#demo)
* [Get started](#get-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Run](#run)
  * [Available Commands](#available-commands)
* [Contributions](#contributions)

## Why a Python based Tabcmd?

* Run Tabcmd commands on MacOS (existing Tabcmd does not officially support MacOS)
* Authenticate using Personal Access Tokens (existing Tabcmd does not support Personal Access Token login)
* Easily use public endpoints available in Python based [Tableau Server Client](https://github.com/tableau/server-client-python/)
* Add more functionality and extend script for other automation tasks

## Demo/Samples

_coming soon_

## Get started

This section describes how to install and configure tabcmd.

### Prerequisites

To work with tabcmd, you need the following:

* MacOS / Windows
* Python 3.7+ installed

### Installation

To install tabcmd, follow these steps:

1. Clone the repo
2. Run `pip install .`

## Run

To run tabcmd, follow these steps:

1. To run a command:
    * `tabcmd [command_name] [--flags]`
    * Examples:
        * `tabcmd login --username [username] --password [password] --server
         [server_name] --site [site_name]`
        * `tabcmd createproject --name [project_name]`

### Available Commands

This table lists the development status of all commands, listed in the same order as the tabcmd help.

These are the column definitions:

* TSC: API support is available in [TSC](https://github.com/tableau/server-client-python/)
* Completed: Code implemented, manually tested, unit tests for parsing added
* Done: Error handling, all unit tests, logging, code review, can produce docs, merged into master

| Command | TSC | Completed | Done | Notes |
|-|-|-|-|-|
| addusers (to group) | Yes (single user) | :heavy_check_mark: |  |  |
| createextracts | Yes |  |  |  |
| creategroup | Yes | :heavy_check_mark:  |  |  |
| createproject | Yes | :heavy_check_mark:  |  |  |
| createsite | Yes | :heavy_check_mark:  |  |  |
| createsiteusers | Yes | :heavy_check_mark:  |  |  |
| createusers | Yes (single user) | :heavy_check_mark:  |  |  |
| decryptextracts | Yes |  |  |  |
| delete workbook-name or datasource-name | Yes | :heavy_check_mark:  |  |  |
| deleteextracts | Yes |  |  |  |
| deletegroup | Yes | :heavy_check_mark:  |  |  |
| deleteproject | Yes | :heavy_check_mark:  |  |  |
| deletesite | Yes | :heavy_check_mark:  |  |  |
| deletesiteusers | Yes | :heavy_check_mark:  |  |  |
| deleteusers | No |  |  |  |
| editdomain | No |  |  |  |
| editsite | Yes | :heavy_check_mark:  |  |  |
| encryptextracts | Yes |  |  |  |
| export | Yes | :heavy_check_mark:  |  |  |
| get url | Yes |  |  |  |
| initialuser | No |  |  |  |
| listdomains | No |  |  |  |
| listsites | Yes | :heavy_check_mark:  |  |  |
| login | Yes | :heavy_check_mark:  |  |  |
| logout | Yes | :heavy_check_mark:  |  |  |
| publish | Yes | :heavy_check_mark:  |  |  |
| publishsamples | No |  |  |  |
| reencryptextracts | Yes |  |  |  |
| refreshextracts | No |  |  |  |
| removeusers | Yes | :heavy_check_mark:  |  |  |
| reset_openid_sub | No |  |  |  |
| runschedule | No |  |  |  |
| set | No |  |  |  |
| syncgroup | No |  |  |  |
| version | N/A |  |  |  |

## Contributions

Code contributions and improvements by the community are welcomed!

See the LICENSE file for current open-source licensing and use information. See dev information at [contributing.md](./contributing.md)

Before we can accept pull requests from contributors, we require a signed [Contributor License Agreement (CLA)](http://tableau.github.io/contributing.html).
