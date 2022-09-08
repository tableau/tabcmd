---
title: About Tabcmd
layout: docs
---


## About Tabcmd
Tabcmd ships with Tableau Server and, for at least 2022, it will continue being included with new installs of Server. 

This new version of tabcmd can be updated for users at any time, without waiting for a new release of Server. Significant new features will only be added to this new version.

### Why a new tabcmd? 
The updated tabcmd command-line interface (CLI) allows you to do the following:
* Run tabcmd commands on MacOS (the existing tabcmd doesn’t officially support MacOS)
* Authenticate using personal access tokens (the existing tabcmd doesn’t support personal access token logins)

Because it is built on public endpoints available in the Python-based Tableau Server Client (TSC), tabcmd also matches behavior through the web client or REST API more closely. This also means faster development time to add functionality and extend the tabcmd script for other automation tasks.

### Which one do I have?
Copies of tabcmd that shipped with Tableau Server are referred to by the version number they shipped in: for example, tabcmd 2020.4, tabcmd 2021.4, etc. The first version built in Python is tabcmd 2.0. To see the version of your current tabcmd, run

`tabcmd -v`

### Will one of them go away?
At some point in the future, tabcmd will no longer be included with Tableau Server. We have no intention of breaking Server install flows. If you have specific suggestions or concerns on what that will look like, feel free to open an issue here or a thread on the Community Forums.

## About this help

### Feedback 
The best way to give feedback or ask a question is at the [Tableau Community Forums](https://community.tableau.com/s/topic/0TO4T000000QT6xWAG/tabcmd) or [here on GitHub](https://github.com/tableau/tabcmd/issues)

### Developers
[Looking for code?](https://github.com/tableau/tabcmd)

### Addressing implicit bias in technical language
In an effort to align with one of our core company values, equality, we have changed terminology to be more inclusive where possible. Because changing terms in code can break current implementations, we maintain the current terminology in the following places:

- Tableau APIs: methods, parameters, and variables
- Tableau CLIs: commands and options
- Installers, installation directories, and terms in configuration files
- Tableau Resource Monitoring Tool (we plan to make changes to non-inclusive terminology in the web interface, error messages, and related documentation soon.)
- Third-party systems documentation

For more information about our ongoing effort to address implicit bias, see [Salesforce Updates Technical Language in Ongoing Effort to Address Implicit Bias](https://www.salesforce.com/news/stories/salesforce-updates-technical-language-in-ongoing-effort-to-address-implicit-bias) on the Salesforce website.
