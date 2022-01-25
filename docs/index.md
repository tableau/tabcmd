---
title: tabcmd
layout: docs
---

Tableau provides the tabcmd command-line utility which you can use to automate site administration tasks on your Tableau Online site. For example, creating or deleting users, projects, and groups.

<div class="alert alert-info">
<strong>Important</strong>: To ensure availability and avoid disruption with Tableau Online, make sure to upgrade your tabcmd client to a version greater than version 2020.2 before January 2022. The tabcmd versions are API backward compatible and should not require code changes. For more information, see [Install tabcmd](#install_tabcmd).
</div>

# Install tabcmd {#install_tabcmd}

When Tableau Server or Tableau Online is upgraded to a new version, if an updated version of tabcmd is required, you can download it from the Tableau Server Releases page on the Tableau website.

For Tableau Server, we recommend you download the version that matches your server version. For Tableau Online, we recommend you always download the latest version to avoid issues caused by version incompatibilities. In either case, using an out of date version of tabcmd can cause errors and unpredictable results.

1. Open a web browser and go to the [Tableau Server Releases](https://www.tableau.com/support/releases/server?_ga=2.51032878.601314143.1643046979-174841.1636564315) page. Go to this page even if you use Tableau Online.

2. If you're using:

* Tableau Online, select the latest Tableau Server release.
* Tableau Server (Windows or Linux): select the release that matches your server version.

    In either case, if the expanded information shows maintenance releases, select the latest maintenance release or the one that matches your server version.


Select the server version you use (latest release for Tableau Online)

This takes you to the release notes page, called Resolved Issues, where you can read about security improvements and resolved issues.

3. Scroll to the Download Files section under the resolved issues, select the tabcmd download link that is compatible with the computer on which you’ll run the tabcmd commands.

Select the tabcmd installer for the computer you'll use it on (32- or 64-bit)

The remaining steps refer to this computer as “the tabcmd computer.”

4. Save the installer to the tabcmd computer, or a location accessible from that computer .

5. Complete the installation steps as appropriate for the operating system of the tabcmd computer:

    **Windows**
By default tabcmd is installed to ```C:\Program Files\Tableau\Tableau Server\<version>\extras\Command Line Utility```. You can change this during installation and recommend that you install tabcmd to a folder named tabcmd at the root of the C:\ drive (`C:\tabcmd)`. This can make it easier to locate and run, and will accommodate some limitations with the Windows operating system if you add the tabcmd directory to the Windows PATH.


        <div class="alert alert-info"><strong>Note</strong>: The tabcmd Setup program does not add the tabcmd directory to the Windows PATH variable. You can add it manually, or you can include the full path to tabcmd each time you call it.</div>

        You can install tabcmd in two ways on Windows:

        a. Double-click the installer to follow the steps in the UI:

       * Accept the license agreement.

       * If you want to install to a non-default location, click Customize and type or browse to the location you want to install tabcmd to.

       * Click Install.
         If you are prompted by Windows Defender Firewall or User Account Control, click Allow access.

        b. Run the installer from a command prompt:

        * Open a command prompt as administrator on the tabcmd computer.

        * Navigate to the directory where you copied the tabcmd installer.

        * Install tabcmd:

            ```
            tableau-setup-tabcmd-tableau-<version_code>-x64.exe /quiet ACCEPTEULA=1
            ```
        To install to a non-default location:

            ```
            tableau-setup-tabcmd-tableau-<version_code>-x64.exe /quiet ACCEPTEULA=1 INSTALLDIR="<path\to\install\directory>"
            ```
        For example:

            ```
            tableau-setup-tabcmd-tableau-<version_code>-x64.exe /quiet ACCEPTEULA=1 INSTALLDIR="C:\tabcmd"
            ```
            For a complete list of command line options you can use with the tabcmd installer, run the installer with a /?. For more information on tabcmd installer command line options, see Install Switches and Properties for tabcmd (Windows).

        The tabcmd Setup program creates logs in C:\Users\<user>\AppData\Local\Temp you can use if you have problems installing tabcmd. The logs use the naming convention Tableau_Server_Command_Line_Utility_(<version_code>)_##############.log.


    * **Linux**
        <div class="alert alert-info"><b>Note</b>: To run tabcmd on a Linux computer, you must have Java 8 (also called Java 1.8) installed. On RHEL-like systems this will be installed as a dependency when you install tabcmd. On Debian-like systems, you need to install Java 8 (1.8) separately if it is not already installed.

        a. Log on as a user with sudo access to the tabcmd computer.

        b. Navigate to the directory where you copied the .rpm or .deb package that you downloaded.

        * On RHEL-like distributions, including CentOS, run the following command:

        ```sudo yum install tableau-tabcmd-<version>.noarch.rpm```

        * On Ubuntu and Debian, run the following command:

        ```sudo apt-get install ./tableau-tabcmd-<version>_all.deb```

        To uninstall tabcmd from a Linux computer, see the documentation for the Linux variety you are running.

6. (Optional) Add the fully qualified location where tabcmd is installed to your system path to allow you to run tabcmd commands without changing to that location, or specifying the location with each command. Steps to do this depend on the type and version of your operating system. For more information, see [PATH_(variable)](https://en.wikipedia.org/wiki/PATH_(variable)).

# How to use tabcmd
The basic steps for using tabcmd are as follows:

1. Open the Command Prompt as an administrator.

2. On a Windows computer, if you installed tabcmd on a computer other than the initial node, change to the directory where you installed tabcmd.
On a Linux computer, you do not need to change to the install directory.

3. Run the tabcmd command.

When you use tabcmd, you must establish an authenticated server session. The session identifies the server or Tableau Online site and the user running the session. You can start a session first, and then specify your command next, or you can start a session and execute a command all at once.

>**Important**: If you are using tabcmd to perform more than one task, you must run tasks one after another (serially), rather than at the same time (in parallel).

Commands (such as login) and the options (such as -s, -u, etc.) are not case sensitive, but the values you provide (such as User@Example.com) are case sensitive.

# Examples
The following command demonstrates starting a session:

```tabcmd login -s <https://online.tableau.com> -t mysite -u authority@email.com -p password```

Here’s how to start a session and delete a workbook with one command—note that you do not need login here:

```tabcmd delete "Sales_Workbook" -s <https://online.tableau.com> -t campaign -u admin@email.com -p password```

The options -s, -t, -u, and -p are among the tabcmd global variables, which can be used with any command.

For more information, see [tabcmd Commands](tabcmd_cmd.md).
