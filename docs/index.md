---
title: tabcmd
layout: docs
permalink: /docs/index.html
---

Tableau provides the tabcmd command-line interface that you can use to automate site administration tasks on your Tableau Online or Tableau Server site. For example, you can use tabcmd to create or delete users, projects, and groups.

<div class="alert alert-info">
<strong>Important</strong>: To ensure availability and avoid disruption with Tableau Online, make sure to upgrade your tabcmd client to a version greater than version 2020.2 before January 2022. The tabcmd versions are API backward compatible and should not require code changes. For more information, see <a href="#install_tabcmd">Install tabcmd</a>.
</div>

* TOC
{:toc}

# Why a new tabcmd? 
The updated tabcmd command-line interface (CLI) allows you to do the following:
* Run tabcmd commands on MacOS (the existing tabcmd does not officially support MacOS)
* Authenticate using personal access tokens (the existing tabcmd does not support personal access token logins)
* Use public endpoints available in the Python-based Tableau Server Client (TSC)
* Add more functionality and extend the tabcmd script for other automation tasks

# Install tabcmd {#install_tabcmd}

You can install Tabcmd version 2 with pip or from the source code
## Install with pip (recommended)
Run the following command to install the latest stable version of tabcmd:

```pip install tabcmd```

## Install from the development branch
You can install from the development branch for a preview of upcoming features. Run the following command to install from the development branch:

```pip install git+https://github.com/tableau/tabcmd.git@development```

<div class="alert alert-info">
<strong>Important</strong>: Do not use the version from the development branch for production code. The methods in the development version are subject to change at any time.</div>

# Examples
The following command demonstrates starting a session:

```tabcmd login -s <https://online.tableau.com> -t mysite -u authority@email.com -p password```

Here’s how to start a session and delete a workbook with one command—note that you do not need login here:

```tabcmd delete "Sales_Workbook" -s <https://online.tableau.com> -t campaign -u admin@email.com -p password```

The options -s, -t, -u, and -p are among the tabcmd global variables, which can be used with any command.

For more information, see [tabcmd Commands](tabcmd_cmd).
