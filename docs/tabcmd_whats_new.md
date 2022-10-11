---
title: What's New
layout: docs
---

## About tabcmd
tabcmd ships with Tableau Server and, for at least 2022, it will continue being included with new installs of Server. 

Version 2.0 of tabcmd can be updated for users at any time, without waiting for a new release of Server. Significant new features will only be added to this new version.

## Why a new tabcmd? 
The updated tabcmd command-line interface (CLI) allows you to do the following:
* Run tabcmd commands on Windows, macOS, and Linux. The earlier version only supported Windows.
* Authenticate using personal access tokens. The earlier tabcmd didn't support personal access token logins.

Because it is built on public endpoints available in the Python-based Tableau Server Client (TSC), tabcmd also matches behavior through the web client or REST API more closely. This also means faster development time to add functionality and extend the tabcmd script for other automation tasks.

## Which version do you have?
Copies of tabcmd that shipped with Tableau Server are referred to by the version number they shipped in. For example, tabcmd 2020.4, tabcmd 2021.4, etc. The first version built in Python is tabcmd 2.0. To see the version of your current tabcmd, run

`tabcmd -v`

## Will the earlier version go away?
At some point in the future, tabcmd will no longer be included with Tableau Server. We have no intention of breaking Server install flows. If you have specific suggestions or concerns on what that will look like, feel free to open an issue here or a thread on the [Tableau Community Forums](https://community.tableau.com/s/topic/0TO4T000000QT6xWAG/tabcmd).

## Feedback 
The best way to give feedback or ask a question is at the [Tableau Community Forums](https://community.tableau.com/s/topic/0TO4T000000QT6xWAG/tabcmd) or [here on GitHub](https://github.com/tableau/tabcmd/issues)

## Developers
[Looking for code?](https://github.com/tableau/tabcmd)