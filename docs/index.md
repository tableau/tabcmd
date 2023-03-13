---
title: tabcmd
layout: docs
permalink: /docs/index.html
---

Tableau provides the tabcmd command-line interface that you can use to automate site administration tasks on your Tableau Cloud or Tableau Server site. For example, you can use tabcmd to create or delete users, projects, and groups.
This new version of tabcmd supports signing in with both Personal Access Tokens and passwords.

* TOC
{:toc}


## Install tabcmd {#install_tabcmd}
You can download and run tabcmd 2.0 as an executable file, or install it on the command line with pip.

### Download and run (recommended)
Packaged apps are available for the latest release at (https://github.com/tableau/tabcmd/releases)
* For Windows, download tabcmd.exe
* For macOS, download tabcmd-mac.zip
* For Linux, download tabcmd

### Install with pip 
To run tabcmd manually as a python module, you can install the latest stable version from pypi:

```shell
pip install tabcmd
```

### Install from the development branch
You can install from the development branch for a preview of upcoming features. Run the following command to install from the development branch:

```shell
pip install git+https://github.com/tableau/tabcmd.git@development
```

<div class="alert alert-info">
<strong>Important</strong>: Don’t use the version from the development branch for production code. The methods in the development version are subject to change at any time.</div>

### Install the older tabcmd client
If you would like to install an older version of tabcmd, you can continue to follow the instructions at https://help.tableau.com/current/server/en-us/tabcmd.htm#tabcmd-install

## Logging in

You can log in to the tabcmd CLI in one of four ways:

  * Log in with `--username` but not `--password`, and tabcmd prompts for the password to be entered 


  * Log in using `--passwordfile` instead of `--password`

  * Log in with a personal access token (PAT) (only available in tabcmd 2.0)

  * Log in with `--password` and the password value listed in the command line. This is the simplest way to log in but it was the least secure.

<div class="alert alert-info">
<strong>Tip</strong>: If your password or PAT has <a href="https://en.wikipedia.org/wiki/Delimiter">delimiters</a> or certain special characters, the command line might not correctly send your password or PAT to the server. These characters must be escaped. 

Special characters can be:

 * comma (,)
 * semicolon (;)
 * equals (=)
 * space ( )
 * tab (    )
 * plus (+)
 * semi-colon (;)
 * ellipsis (...)

The escape character to use depends on your operating system (OS). For example, the caret (^) is an escape character on Windows. To use the caret, you must escape it with itself (^) or by enclosing in double quotes. For example: 

--username "tom^harry"
--username tom^^harry

For more information about escaping characters for your OS, see <a href="https://ss64.com/nt/syntax-esc.html">How-to: Escape Characters, delimiters and Quotes (Windows)</a>, <a href="https://ss64.com/osx/syntax-quoting.html">How-to: Escape Characters, delimiters and Quotes (Mac)</a>, or <a href="https://ss64.com/bash/syntax-quoting.html">How-to: Escape Characters, delimiters and Quotes (Linux)</a>.
</div>


## Examples
The following command demonstrates starting a session:

```shell
tabcmd login -s <https://online.tableau.com> -t mysite -u authority@email.com -p password
```

Here’s how to start a session and delete a workbook with one command. You don’t need login here:

```shell
tabcmd delete "Sales_Workbook" -s <https://online.tableau.com> -t campaign -u admin@email.com -p password
```

The options -s, -t, -u, and -p are among the tabcmd global variables, which can be used with any command.

For more information, see [tabcmd Commands](tabcmd_cmd).

## Log file
Full log information is written to the `tabcmd.log` file. This file is included in the directory where the tabcmd program is running.