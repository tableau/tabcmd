---
title: Install Switches and Properties for tabcmd2 (Windows)
layout: docs
---

You can use the following switches when installing the Tableau Server Command Line Utility (tabcmd) version 2019.4.0 or later from the command line on Windows.

<div class="alert alert-info"><strong>Important</strong>: To ensure availability and avoid disruption with Tableau Online, make sure to upgrade your tabcmd2 client to a version greater than version 2020.2 before January 2022. The tabcmd2 versions are API backward compatible and should not require code changes. For more information, see <a href="index.html#install_tabcmd2">Install tabcmd</a>.</div>

<div class="alert alert-info"><strong>Note</strong>: There are no equivalent switches for the Linux version of the tabcmd2 installer.</div>

<table>
    <thead>
        <tr>
            <th>Switch</th>
            <th>Description</th>
            <th>Comments</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>/install</code> | <code>/repair</code> | <code>/uninstall</code> | <code>/layout "&lt;directory&gt;"</code></td>
            <td>Run Setup to either install, repair, or uninstall tabcmd, or with /layout, create a complete local copy of the installation bundle in the directory specified.</td>
            <td>Default is to install, displaying UI and all prompts. If no directory is specified on a fresh install, `C:\Program Files\Tableau\Tableau Server\&lt;version&gt;\extras\Command Line Utility` is assumed.</td>
        </tr>
        <tr>
            <td><code>/passive</code></td>
            <td>Run Setup with minimal UI and no prompts.</td>
            <td></td>
        </tr>
        <tr>
            <td><code>/quiet</code> | <code>/silent</code></td>
            <td>Run Setup in unattended, fully silent mode. No UI or prompts are displayed.</td>
            <td><div class="alert alert-info"><strong>Note</strong>: Use either /silent or /quiet, not both.</div></td>
        </tr>
        <tr>
            <td><code>/norestart</code></td>
            <td>Run Setup without restarting Windows, even if a restart is necessary.</td>
            <td><div class="alert alert-info"><strong>Note</strong>: In certain rare cases, a restart cannot be suppressed, even when this option is used. This is most likely when an earlier system restart was skipped, for example, during installation of other software.</div></td>
        </tr>
        <tr>
            <td><code>/log "&lt;log-file&gt;"</code></td>
            <td>Log information to the specified file and path. By default log files are created in the user's %TEMP% folder with a naming convention of `Tableau_Server_Command_Line_utility_&lt;version_code&gt;.log`.</td>
            <td>If no file location is specified, the log file is written to the user's TEMP folder (<code>C:\Users\&lt;username&gt;\AppData\Local\Temp</code>). Check this log file for errors after installation. Example: <code>&lt;Setup file&gt; /silent /log "C:\Tableau\Logs	abcmd-Install" ACCEPTEULA=1</code></td>
        </tr>
    </tbody>
</table>
        
<table>
    <thead>
        <tr>
            <th>Properties</th>
            <th>Description</th>
            <th>Comments</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>ACCEPTEULA=1|0</code></td>
            <td>Accept the End User License Agreement (EULA). Required for quiet, silent, and passive install. 1 = accept the EULA, 0 = do not accept the EULA.</td>
            <td>If not included when using <code>/passive</code>, <code>/silent</code> or <code>/quiet</code>, Setup fails silently. If included but set to 0, Setup fails.</td>
        </tr>
        <tr>
            <td><code>INSTALLDIR="
&lt;path\to\installation\directory&gt;"</code></td>
            <td>Install tabcmd2 to the specified non-default install location.</td>
            <td>Specifies the location to install tabcmd. If not used, tabcmd2 is installed to <code>C:\Program Files\Tableau\Tableau Server\&lt;version_code&gt;\extras\Command Line Utility</code>. 
            
Example: <code>&lt;Setup file&gt; /silent INSTALLDIR="C:\tabcmd"</code></td>
        </tr>
    </tbody>
</table>

