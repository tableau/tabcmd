---
title: tabcmd
layout: docs
permalink: /docs/index.html
---

Tableau provides the tabcmd command-line interface that you can use to automate site administration tasks on your Tableau Online or Tableau Server site. For example, you can use tabcmd to create or delete users, projects, and groups.

* TOC
{:toc}


## Install tabcmd {#install_tabcmd}
You can download and run tabcmd 2.0 as an executable file, or install it on the command line with pip.

### Download and run (recommended)
* For [Windows](https://github.com/tableau/tabcmd/releases/download/v1.99.99/tabcmd.exe)
<!--- * For macOS: --->
<!--- * For Linux:  --->

### Install with pip 
For macOS and Linux, run the following command to install the latest stable version of tabcmd:

```shell
pip install tabcmd
```

### Install from the development branch
You can install from the development branch for a preview of upcoming features. Run the following command to install from the development branch:

```shell
pip install git+https://github.com/tableau/tabcmd.git@development
```

<div class="alert alert-info">
<strong>Important</strong>: Do not use the version from the development branch for production code. The methods in the development version are subject to change at any time.</div>

### Install the older tabcmd client
If you would like to install an older version of tabcmd, you can continue to follow the instructions at https://help.tableau.com/current/server/en-us/tabcmd.htm#tabcmd-install

## Logging in

You can log in to the tabcmd CLI in one of four ways:

  * Log in with `--username` but not `--password`, and tabcmd will prompt for the password to be entered 


  * Log in using `--passwordfile` instead of `--password`

  * Log in with a personal access token (PAT) (only available in tabcmd 2.0)

  * Log in with `--password` and the password value listed in the command line. This is the simplest way to log in but it was the least secure.


## Examples
The following command demonstrates starting a session:

```shell
tabcmd login -s <https://online.tableau.com> -t mysite -u authority@email.com -p password
```

Here’s how to start a session and delete a workbook with one command. Note that you do not need login here:

```shell
tabcmd delete "Sales_Workbook" -s <https://online.tableau.com> -t campaign -u admin@email.com -p password
```

The options -s, -t, -u, and -p are among the tabcmd global variables, which can be used with any command.

For more information, see [tabcmd Commands](tabcmd_cmd).
