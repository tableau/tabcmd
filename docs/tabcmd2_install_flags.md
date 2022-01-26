---
title: Install Switches and Properties for tabcmd2 (Windows)
layout: docs
---

You can use the following switches when installing the Tableau Server Command Line Utility (tabcmd) version 2019.4.0 or later from the command line on Windows.

<div class="alert alert-info"><strong>Important</strong>: To ensure availability and avoid disruption with Tableau Online, make sure to upgrade your tabcmd2 client to a version greater than version 2020.2 before January 2022. The tabcmd2 versions are API backward compatible and should not require code changes. For more information, see <a href="index.html#install_tabcmd2">Install tabcmd</a>.</div>

<div class="alert alert-info"><strong>Note</strong>: There are no equivalent switches for the Linux version of the tabcmd2 installer.</div>

| Switch  | Description  | Comments  |
|---|---|---|
| `/install \| /repair \| /uninstall \| /layout "<directory>"`  | Run Setup to either install, repair, or uninstall tabcmd, or with /layout, create a complete local copy of the installation bundle in the directory specified.  | Default is to install, displaying UI and all prompts. If no directory is specified on a fresh install, `C:\Program Files\Tableau\Tableau Server\<version>\extras\Command Line Utility` is assumed.  |
| `/passive`  | Run Setup with minimal UI and no prompts.  |   |
| `/quiet \| /silent`  | Run Setup in unattended, fully silent mode. No UI or prompts are displayed.  | >**Note**: Use either /silent or /quiet, not both.  |
| `/norestart` | Run Setup without restarting Windows, even if a restart is necessary. | >**Note**: In certain rare cases, a restart cannot be suppressed, even when this option is used. This is most likely when an earlier system restart was skipped, for example, during installation of other software.  |
| `/log "<log-file>"`  | Log information to the specified file and path. By default log files are created in the user's %TEMP% folder with a naming convention of `Tableau_Server_Command_Line_utility_<version_code>.log`. | If no file location is specified, the log file is written to the user's TEMP folder (`C:\Users\<username>\AppData\Local\Temp`). Check this log file for errors after installation. Example: `<Setup file> /silent /log "C:\Tableau\Logs\tabcmd-Install" ACCEPTEULA=1`  |
 
| Properties	  | Description	  | Comments  |
|---|---|---|
| `ACCEPTEULA=1|0`  | Accept the End User License Agreement (EULA). Required for quiet, silent, and passive install. 1 = accept the EULA, 0 = do not accept the EULA.  | If not included when using /passive, /silent or /quiet, Setup fails silently. If included but set to 0, Setup fails.  |
|`INSTALLDIR="<path\to\installation\directory>"`  | Install tabcmd2 to the specified non-default install location.  |Specifies the location to install tabcmd. If not used, tabcmd2 is installed to `C:\Program Files\Tableau\Tableau Server\<version_code>\extras\Command Line Utility`. Example: `<Setup file> /silent INSTALLDIR="C:\tabcmd"`  |