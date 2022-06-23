---
title: tabcmd Commands
layout: docs
---

You can use the following commands with the tabcmd command-line tool:

<div class="alert alert-info"><strong>Note</strong>: Some commands listed may not apply when using tabcmd with Tableau Online.</div>
<div class="alert alert-info"><strong>Note</strong>: Some commands or options listed may not yet be implemented in this version of tabcmd.</div>

* TOC
{:toc}


## login
Logs in a Tableau Online user. 

<div class="alert alert-info"><strong>Note</strong>: When you use tabcmd you cannot use SAML single sign-on (SSO), even if your site is configured to use SAML. To log in, you must pass the user name and password or token name and token of a user who has been created in your site. You will have the permissions of the Tableau Server user that you're signed in as.</div>

Once you log in, the session will continue until it expires on the server or the logout command is run.

If your session has expired and you want to log in using the same information you've already used, just specify the \-\-password option or the \-\-token option. The server and user name stored in the cookie will be used. (This will not work if \-\-no-cookie was specified)

If you do not provide a password or token or passwordfile you will be prompted for one. The command will fail if username/password is specified AND token name/token is specified.

Instead of calling the login command, all of the options for this command can be used while calling any other command, to create a session and run the command immediately. 
e.g 
tabcmd login --server x --site y --username u --password p
tabmcd listsites
is the same as
tabcmd listsites --server x --site y --username u --password p


### Options

-s, \-\-server

: If you are running the command from a Tableau Server computer that’s on your network, you can use http://localhost. Otherwise, specify the computer's URL, such as http://bigbox.myco.com or http://bigbox.

If the server is using SSL, you will need to specify https:// in the computer's URL. 

If the server is using a port other than 80 (the default), you will need to specify the port, for example http://servername.com:8000

For Tableau Online, specify the URL https://online.tableau.com.

-t, \-\-site

: Include this option if the server has multiple sites, and you are logging in to a site other than the default site. To explicitly specify the default site, use quotes around an empty string: ""

The site ID is used in the URL to uniquely identify the site. For example, a site named West Coast Sales might have a site ID of west-coast-sales.

-u, \-\-username

: The user name of the user logging in. For Tableau Online, the user name is the user's email address.

-p, \-\-password

: Password for the user specified for \-\-username. If you do not provide a password you will be prompted for one.

\-\-password-file

: Allows the password to be stored in the given filename.txt file rather than the command line, for increased security.

-x, \-\-proxy

: Use to specify the HTTP proxy server and port (Host:Port) for the tabcmd request.

\-\-no-prompt

: Do not prompt for a password. If no password is specified, the login command will fail.

\-\-cookie

: Saves the session ID on login. Subsequent commands will not require a login. This value is the default for the command.

\-\-no-cookie

: Do not save the session ID information after a successful login. Subsequent commands will require a login.

\-\-timeout SECONDS

: The number of seconds the server should wait before processing the login command. Default: 30 seconds.

-tn, \-\-token-name

: The token name for user.

-to, \-\-token

: The token specified for --token-name. If you do not provide a token, you will be prompted for one.


### Example

Log in to the Tableau Online site with the specified site ID:

```tabcmd login -s https://online.tableau.com -t siteID -u user@email.com -p password```

### Log in using personal access tokens
Create a personal access token (PAT) as described in [create tokens](https://help.tableau.com/current/server/en-us/security_personal_access_tokens.htm#create-tokens).
For example:

```tabcmd login --server “http://exampleserver.com" --site "examplesite" --token-name "tokenname" --token "exampletoken"```

where:
* `-tn, --token-name` is the token name for user.
* `-to, --token` is the token specified for `--token-name`


## logout
Logs out of the server.

### Example

```tabcmd logout```


## addusers *group-name* 
Adds users to the specified group.

### Options
\-\-users
: Add the users in the given .csv file to the specified group. The file should be a simple list with one user name per line. User names are not case-sensitive. The users should already be created on Tableau Online.

: For more information, see [CSV Import File Guidelines](https://help.tableau.com/current/online/en-us/csvguidelines.htm).

### Example

`tabcmd addusers "Development" --users "users.csv"`


## createextracts
Creates extracts for a published workbook or data source.

### Options

-d, \-\-datasource
: The name of the target data source for extract creation.

\-\-embedded-datasources

: A space-separated list of embedded data source names within the target workbook. Enclose data source names with double quotes if they contain spaces. Only available when creating extracts for a workbook.

\-\-encrypt

: Create encrypted extract.

\-\-include-all

: Include all embedded data sources within target workbook. Only available when creating extracts for workbook.

\-\-parent-project-path

: Path of the project that is the parent of the project that contains the target resource. Must specify the project name with `--project`.

\-\-project

: The name of the project that contains the target resource. Only necessary if \-\-workbook or \-\-datasource is specified. If unspecified, the default project 'Default' is used.

-u, -url

: The canonical name for the resource as it appears in the URL.

-w, -workbook

: The name of the target workbook for extract creation.


## creategroup *group-name*
Creates a group. Use addusers to add users after the group has been created.

### Example

```tabcmd creategroup "Development"```

## createproject *project-name*
Creates a project.

### Options

-n, \-\-name

: Specifies the name of the project that you want to create.

\-\-parent-project-path

: Specifies the name of the parent project for the nested project as specified with the -n option. For example, to specify a project called "Nested" that exists in a "Main" project, use the following syntax: ```--parent-project-path "Main" -n "Nested".```

-d, \-\-description

: Specifies a description for the project.

### Example

```tabcmd createproject -n "Quarterly_Reports" -d "Workbooks showing quarterly sales reports."```

## createsite *site-name* <div class="alert alert-info"><strong>Note</strong>: Tableau Server only.</div>

Creates a site.

### Options

\-r, \-\-url

: Used in URLs to specify the site. Different from the site name.

\-\-user-quota

: Maximum number of users that can be added to the site.

\-\-[no-]site-mode

: Allows or denies site administrators the ability to add users to or remove users from the site.

\-\-storage-quota

: In MB, the amount of workbooks, extracts, and data sources that can be stored on the site.

\-\-extract-encryption-mode

: The extract encryption mode for the site can be enforced, enabled or disabled. For more information, see [Extract Encryption at Rest](https://help.tableau.com/current/server/en-us/security_ear.htm).

\-\-run-now-enabled

: Allow or deny users from running extract refreshes, flows, or schedules manually. true to allow users to run tasks manually or false to prevent users from running tasks manually. For more information, see [Server Settings (General and Customization)](https://help.tableau.com/current/server/en-us/maintenance_set.htm).

### Examples

Create a site named West Coast Sales. A site ID of WestCoastSales will be automatically created, the site will have no storage quota limit, and site administrators will be able to add and remove users:

```tabcmd createsite "West Coast Sales"```

Create a site named West Coast Saleswith a site ID of wsales:

```tabcmd createsite "West Coast Sales" -r "wsales"```

Prevent site administrators from adding users to the site:

```tabcmd createsite "West Coast Sales" --no-site-mode```

Set a storage quota, in MB:

```tabcmd createsite "West Coast Sales" --storage-quota 100```


## createsiteusers *filename.csv*

Adds users to a site, based on information supplied in a comma-separated values (CSV) file. If the user is not already created on the server, the command creates the user before adding that user to the site.

The CSV file must contain one or more user names and can also include (for each user) a password, full name, license type, administrator level, publisher (yes/no), and email address. For information about the format of the CSV file, see [CSV Import File Guidelines](https://help.tableau.com/current/online/en-us/csvguidelines.htm).

As an alternative to including administrator level and publisher permissions in the CSV file, you can pass access level information by including the \-\-role option and specifying the site role you want to assign users listed in the CSV file.

By default, users are added to the site that you are logged in to. To add users to a different site, include the global \-\-site option and specify that site. (You must have permissions to create users on the site you specify.)

### Options

\-\-auth-type

: Sets the authentication type (TableauID or SAML) for all users in the .csv file. If unspecified, the default is TableauID.

<div class="alert alert-info"><strong>Note</strong>: To use SAML authentication, the site itself must be SAML-enabled as well. For information, see <a href="https://help.tableau.com/current/online/en-us/saml_config_site.htm">Enable SAML Authentication on a Site</a>.</div>

\-\-nowait

: Do not wait for asynchronous jobs to complete.

\-\-role

: Specifies a site role for all users in the .csv file. When you want to assign site roles using the \-\-role option, create a separate CSV file for each site role.

Valid values are: ServerAdministrator, SiteAdministratorCreator, SiteAdministratorExplorer, SiteAdministrator, Creator, ExplorerCanPublish, Publisher, Explorer, Interactor, Viewer, and Unlicensed.

The default is Unlicensed for new users and unchanged for existing users. Users are added as unlicensed also if you have a user-based server installation, and if the createsiteusers command creates a new user, but you have already reached the limit on the number of licenses for your users.

<div class="alert alert-info"><strong>Note</strong>: On a multi-site Tableau Server, if you want to assign the ServerAdministrator site role using the <code>--role</code> option, use the createusers command instead of createsiteusers.</div>

\-\-silent-progress

: Do not display progress messages for the command.

### Example

```tabcmd createsiteusers "users.csv" --role "Explorer"```


## decryptextracts <div class="alert alert-info"><strong>Note</strong>: Tableau Server only.</div>

Decrypts all extracts on a site. If no site is specified, extracts on the default site will be decrypted. For more information, see [Extract Encryption at Rest](https://help.tableau.com/current/server/en-us/security_ear.htm).

Depending on the number and size of extracts, this operation may consume significant server resources. Consider running this command outside of normal business hours.


## delete workbook-name or datasource-name
Deletes the specified workbook or data source from the server.

This command takes the name of the workbook or data source as it is on the server, not the file name when it was published.

### Example

`tabcmd delete "Sales_Analysis"`

### Options

-r, \-\-project

: The name of the project containing the workbook or data source you want to delete. If not specified, the “Default” project is assumed.

\-\-parent-project-path

: Specifies the name of the parent project for the nested project as specified with the -r option. For example, to specify a project called "Nested" that exists in a "Main" project, use the following syntax: \-\-parent-project-path "Main" -r "Nested".

\-\-workbook

: The name of the workbook you want to delete.

\-\-datasource

: The name of the data source you want to delete.

## deleteextracts

Deletes extracts for a published workbook or data source.

### Options

-d, \-\-datasource
: The name of the target data source for extract deletion.
\-\-embedded-datasources
: A space-separated list of embedded data source names within the target workbook. Enclose data source names with double quotes if they contain spaces. Only available when deleting extracts for a workbook.
\-\-encrypt
: Create encrypted extract.

\-\-include-all

: Include all embedded data sources within target workbook.

\-\-parent-project-path

: Path of the project that is the parent of the project that contains the target resource. Must specify the project name with \-\-project.

\-\-project

: The name of the project that contains the target resource. Only necessary if \-\-workbook or \-\-datasource is specified. If unspecified, the default project 'Default' is used.

-u, -url

: The canonical name for the resource as it appears in the URL.

-w, -workbook

: The name of the target workbook for extract deletion.

### Example

```tabcmd decryptextracts "West Coast Sales"```



## deletegroup *group-name*
Deletes the specified group from the server.

### Example

`tabcmd deletegroup "Development"`


## deleteproject *project-name*
Deletes the specified project from the server.


### Option

\-\-parent-project-path

: Specifies the name of the parent project for the nested project as specified with the command. 

### Example

to specify a project called "Designs" that exists in a "Main" project:
`tabcmd deleteproject "Designs"` --parent-path "Main"

## deletesite *site-name* <div class="alert alert-info"><strong>Note</strong>: Tableau Server only.</div>

Deletes the specified site from the server.

### Example

```tabcmd deletesite "Development"```

## deletesiteusers *filename.csv*
Removes users from from the site that you are logged in to. The users to be removed are specified in a file that contains a simple list of one user name per line. (No additional information is required beyond the user name.)

By default, if the server has only one site, or if the user belongs to only one site, the user is also removed from the server. On a Tableau Server Enterprise installation, if the server contains multiple sites, users who are assigned the site role of **Server Administrator** are removed from the site but are not removed from the server.

If the user owns content, the user's role is change to **Unlicensed**, but the user is not removed from the server or the site. The content is still owned by that user. To remove the user completely, you must change the owner of the content and then try removing the user again.

### Example

`tabcmd deletesiteusers "users.csv"`

## editsite *site-name* <div class="alert alert-info"><strong>Note</strong>: Tableau Server only.</div>

Changes the name of a site or its web folder name. You can also use this command to allow or deny site administrators the ability to add and remove users, or prevent users from running certain tasks manually. If site administrators have user management rights, you can specify how many users they can add to a site.

### Options

\-\-site-name

: The name of the site that's displayed.

\-\-site-id

: Used in the URL to uniquely identify the site.

\-\-user-quota

: Maximum number of users who can be members of the site.

\-\-[no-]site-mode

: Allow or prevent site administrators from adding users to the site.

\-\-status

: Set to ACTIVE to activate a site, or to SUSPENDED to suspend a site.

\-\-storage-quota

: In MB, the amount of workbooks, extracts, and data sources that can be stored on the site.

\-\-extract-encryption-mode

: The extract encryption mode for the site can be enforced, enabled or disabled. For more information, see [Extract Encryption at Rest](https://help.tableau.com/current/server-linux/en-us/security_ear.htm). Depending on the number and size of extracts, this operation may consume significant server resources.

\-\-run-now-enabled

: Allow or deny users from running extract refreshes, flows, or schedules manually. true to allow users to run tasks manually or false to prevent users from running tasks manually. For more information, see [Server Settings (General and Customization)](https://help.tableau.com/current/server-linux/en-us/maintenance_set.htm).

### Examples

```tabcmd editsite wc_sales --site-name "West Coast Sales"```

```tabcmd editsite wc_sales --site-id "wsales"```

```tabcmd editsite wsales --status ACTIVE```

```tabcmd editsite wsales --user-quota 50```

## encryptextracts *site-name* <div class="alert alert-info"><strong>Note</strong>: Tableau Server only.</div>

Encrypt all extracts on a site. For more information, see [Extract Encryption at Rest](https://help.tableau.com/current/server/en-us/security_ear.htm).

Depending on the number and size of extracts, this operation may consume significant server resources. Consider running this command outside of normal business hours.

### Example

```tabcmd encryptextracts "West Coast Sales"```


## export
Exports a view or workbook from Tableau Online and saves it to a file. This command can also export just the data used for a view. View data is exported at the summary level. To export detail-level data, you must use the Tableau Server UI. For details, see [Download Views and Workbooks](https://help.tableau.com/current/pro/desktop/en-us/export.htm).

<! --- Syntax 
tabcmd get url[?data-parameters] [format-option] [options] [Global options] --->



### Options
-f, \-\-filename

Saves the file with the given filename and extension.  
If you don't provide a name, it will be derived from the view or workbook name. If you don't provide a location, the file will be saved to your current working directory. Otherwise, you can specify a full path or one that's relative to your current working directory.
<div class="alert alert-info"><strong>Note</strong>: You must include a file name extension such as .csv or .pdf. The command does not automatically add an extension to the file name that you provide.</div>

\-\-csv | \-\-pdf | \-\-png | \-\-fullpdf [required]

**format-option** Your format options depend on what's being exported. A workbook can only be exported as a PDF using the `--fullpdf` argument. A view can be exported as a PDF (\-\-pdf) or a PNG (\-\-png) or a csv showing summary data only (\-\-csv).

\-\-pagelayout

Sets the page orientation (landscape or portrait) of the exported PDF. If not specified, its Tableau Desktop setting will be used.

\-\-pagesize

Sets the page size of the exported PDF as one of the following: unspecified, letter, legal, note folio, tabloid, ledger, statement, executive, a3, a4, a5, b4, b5, or quarto. Default is letter.

\-\-width

Sets the width in pixels. Default is 800 px.

\-\-height

Sets the height in pixels. Default is 600 px.

?filter-name

* To filter the data you download, add a parameter to the view or workbook url using this format:
        
        ```?<filter_name>=value```
        
        or, if filtering on a parameter and that parameter has a display name that matches the name of a measure or dimension:

        `?Parameters.<filter_name>=value`

?refresh=yes

* To force a fresh data query instead of pulling the results from the cache, add this parameter to the view or workbook url:
        ```?:refresh=yes` 
        
<div class="alert alert-info"><strong>Notes:</strong>
If you are using tabcmd with your own scripting and the refresh URL parameter is being used a great deal, this can have a negative impact on performance. It's recommended that you use refresh only when real-time data is required—for example, on a single dashboard instead of on an entire workbook.
</div>


Note the following when you use this command:

* **Permissions**: To export, you must have the **Export Image** permission. By default, this permission is Allowed or Inherited for all roles, although permissions can be set per workbook or view.

* **Constraints**: 

* To export a workbook, it must have been published with **Show Sheets as Tabs** selected in the Tableau Desktop Publish dialog box.

* The Tableau workbook that contains the [admin views](https://help.tableau.com/current/online/en-us/adminview.htm) cannot be exported.

* A dashboard can optionally include a web page object. If you are performing an export to PDF of a dashboard that includes a web page object, the web page object won't be included in the PDF.

* **Specifying the view or workbook to export**:

* Use part of the URL to identify what to export, specifically the "workbook/view" string as it appears in the URL for the workbook or view. Do not use the “friendly name,” and exclude the `:iid=<n>` session ID at the end of the URL.

    For example, the Tableau sample view Global Temperatures in the Regionalworkbook has a URL similar to this: <server_name>/#/views/Regional/GlobalTemperatures?:iid=3

    To export the Global Temperatures view, use the string Regional/GlobalTemperatures. 
    *Do not use Regional/Global Temperatures, or Regional/GlobalTemperatures?:iid=3*

* To export a workbook, get the URL string by opening a view in the workbook, and include the view in the string you use.

    In the above example, to export the Regional workbook, use the string `Regional/GlobalTemperatures`.

### Examples

#### Views

```tabcmd export "Q1Sales/Sales_Report" --csv -f "Weekly-Report.csv"```

```tabcmd export -t Sales "Sales/Sales_Analysis" --pdf -f "C:\Tableau_Workbooks\Weekly-Reports.pdf"```

```tabcmd export "Finance/InvestmentGrowth" --png```

```tabcmd export "Finance/InvestmentGrowth?:refresh=yes" --png```

#### Workbooks

```tabcmd export "Q1Sales/Sales_Report" --fullpdf```

```tabcmd export "Sales/Sales_Analysis" --fullpdf --pagesize tabloid -f "C:\Tableau_Workbooks\Weekly-Reports.pdf"```


* **Non-ASCII and non-standard ASCII characters**: If you are exporting a view or workbook with a name that includes a character outside the ASCII character set, or a non-standard ASCII character set, you need to URL encode (percent-encode) the character.

    For example if your command includes the city Zürich, you need to URL encode it as Z%C3%BCrich:

    ```tabcmd export "/Cities/Sheet1?locationCity=Z%C3%BCrich" -fullpdf```


## get *url*
Gets the resource from Tableau Online that's represented by the specified (partial) URL. The result is returned as a file.

<div class="alert alert-info"><strong>Notes:</strong>
    This command is very similar to export, but not identical. Be careful you are using the options and url formatted for the correct command
    </div>
    
<! --- Syntax 
tabcmd get url[?data-parameters] [format-type] [Global options] --->

url: Identifies the view or workbook to be exported. The URL must include a file extension, which determines the type of file returned. A view can be returned in PDF, PNG, or CSV (summary data only) format. A Tableau workbook is returned as a TWB if it connects to a published data source or uses a live connection, or a TWBX if it connects to a data extract.

You specify the url for a view to get using the "/views/<workbookname>/<viewname>.<extension>" string, and specify the url for a workbook to get using the "/workbooks/<workbookname>.<extension>" string. Replace <workbookname> and <viewname> with the names of the workbook and view as they appear in the URL when you open the view in a browser and replace <extension> with the type of file you want to save. Do not use the session ID at the end of the URL (?:iid=<n>) or the "friendly" name of the workbook or view.

    <div class="alert alert-info"><strong>Exception</strong>: If you are downloading a view to a PDF or PNG file, and if you include a <code>--filename</code> parameter that includes the .pdf or .png extension, you do not have to include a .pdf or .png extension in the URL.</div>

\-\-filename (optional): 
The name and extension to save the downloaded content under. If you don't provide a name and file extension, both will be derived from the URL string. If you don't provide a location, the file is saved to your current working directory. Otherwise, you can specify a full path or one that's relative to your current working directory.

?size=??? (optional)
    
If the saved file is a PNG, you can specify the size, in pixels, in the URL.

?refresh=yes (optional)
    
You can optionally add the URL parameter ?:refresh=yes to force a fresh data query instead of pulling the results from the cache. If you are using tabcmd with your own scripting, using the refresh parameter a great deal can have a negative impact on performance. It's recommended that you use refresh only when real-time data is required—for example, on a single dashboard instead of on an entire workbook.

Note the following when you use this command:

* **Permissions**: To get a file, you must have the **Download/Web Save As** permission. By default, this permission is allowed or inherited for all roles, although permissions can be set per workbook or view.

* **Specifying a view or workbook to get**: You specify a view to get using the "/views/<workbookname>/<viewname>.<extension>" string, and specify a workbook to get using the "/workbooks/<workbookname>.<extension>" string. Replace <workbookname> and <viewname> with the names of the workbook and view as they appear in the URL when you open the view in a browser and replace <extension> with the type of file you want to save. Do not use the session ID at the end of the URL (?:iid=<n>) or the "friendly" name of the workbook or view.

    For example, when you open a view Regional Totals in a workbook named Metrics Summary, the URL will look similar to this:

    ```/views/MetricsSummary_1/RegionalTotals?:iid=1```

    Use the string /views/MetricsSummary_1/RegionalTotals.<extension> to get the view.

    Use the string /workbooks/MetricsSummary_1.<extension> to get the workbook.


    
### Examples

#### Views

```tabcmd get "/views/Sales_Analysis/Sales_Report.png" --filename "Weekly-Report.png"```

```tabcmd get "/views/Finance/InvestmentGrowth.pdf" -f "Q1Growth.pdf"```

```tabcmd get "/views/Finance/InvestmentGrowth" -f "Q1Growth.pdf"```

```tabcmd get "/views/Finance/InvestmentGrowth.csv"```

```tabcmd get "/views/Finance/InvestmentGrowth.png?:size=640,480" -f growth.png```

```tabcmd get "/views/Finance/InvestmentGrowth.png?:refresh=yes" -f growth.png```

#### Workbooks

```tabcmd get "/workbooks/Sales_Analysis.twb" -f "C:\Tableau_Workbooks\Weekly-Reports.twb"```

## listsites

<div class="alert alert-info"><strong>Note</strong>: Tableau Server only.</div>

Returns a list of sites to which the logged in user belongs.

### Example

```tabcmd listsites --username adam --password mypassword```

### Options
```--get-extract-encryption-mode```

The extract encryption mode for the site can be enforced, enabled or disabled. For more information, see [Extract Encryption at Rest](https://help.tableau.com/current/server/en-us/security_ear.htm).


## publish *filename.twb(x)*, *filename.tds(x)*, or *filename.hyper*
Publishes the specified workbook (.twb(x)), data source (.tds(x)), or extract (.hyper) to Tableau Online.

    
<! --- Syntax 
tabcmd publish [filename] [options] [Global options] --->
    
If you are publishing a workbook, by default, all sheets in the workbook are published without database user names or passwords.

The permissions initially assigned to the workbook or data source are copied from the project that the file is published to. Permissions for the published resource can be changed after the file has been published.

If the workbook contains user filters, one of the thumbnail options must be specified.

### Options

-n, \-\-name

: Name of the workbook or data source on the server. If omitted, the workbook, data source, or data extract will be named after filename.

-o, \-\-overwrite

: Overwrites the workbook, data source, or data extract if it already exists on the server.

-r, \-\-project

: Publishes the workbook, data source, or data extract into the specified project. Publishes to the “Default” project if not specified.

\-\-parent-project-path

: Specifies the name of the parent project for the nested project as specified with the -r option. For example, to specify a project called "Nested" that exists in a "Main" project, use the following syntax: \-\-parent-project-path "Main" -r "Nested".

<div class="alert alert-info"><strong>Additional arguments not yet implemented:</strong>
\-\-db-username

: Use this option to publish a database user name with the workbook, data source, or data extract.

If you connect to the data through a protected OAuth connection and access token, us the \-\-oauth-username option instead.

\-\-db-password

: Use this option to publish a database password with the workbook, data source, or extract.

\-\-save-db-password

: Stores the provided database password on the server.

\-\-oauth-username

: The email address of the user account. Connects the user through a preconfigured OAuth connection, if the user already has a saved access token for the cloud data source specified in \-\-name. Access tokens are managed in user preferences.

For existing OAuth connections to the data source, use this option instead of \-\-db-username and \-\-db-password.

\-\-save-oauth

: Saves the credential specified by \-\-oauth-username as an embedded credential with the published workbook or data source.

Subsequently, when the publisher or server administrator signs in to the server and edits the connection for that workbook or data source, the connection settings will show this OAuth credential as embedded in the content.

If you want to schedule extract refreshes after publishing, you must include this option with \-\-oauth-username. This is analogous to using \-\-save-db-password with a traditional database connection.

\-\-thumbnail-username

: If the workbook contains user filters, the thumbnails will be generated based on what the specified user can see. Cannot be specified when \-\-thumbnail-group option is set.

\-\-thumbnail-group

: If the workbook contains user filters, the thumbnails will be generated based on what the specified group can see. Cannot be specified when \-\-thumbnail-usernameoption is set.

\-\-tabbed

: When a workbook with tabbed views is published, each sheet becomes a tab that viewers can use to navigate through the workbook. Note that this setting will override any sheet-level security.

\-\-append

: Append the extract file to the existing data source.

\-\-replace

: Use the extract file to replace the existing data source.

</div>

### Examples

`tabcmd publish "analysis_sfdc.hyper" -n "Sales Analysis"
--oauth-username "user-name" --save-oauth`

If the file is not in the same directory as tabcmd, include the full path to the file.

`tabcmd publish "\\computer\volume\Tableau Workbooks\analysis_sfdc.hyper" -n "Sales Analysis" --oauth-username "username" -e-save-oauth`


## publishsamples

Publishes Tableau sample workbooks to the specified project. Any existing samples will be overwritten.

<! --- Syntax 
tabcmd publishsamples -n [project name] [Global options] --->


### Options
-n, \-\-name

Required. Publishes the Tableau samples into the specified project. If the project name includes spaces, enclose the entire name in quotes.

\-\-parent-project-path

Specifies the name of the parent project for the nested project as specified with the -n option. For example, to specify a project called "Nested" that exists in a "Main" project, use the following syntax: ```--parent-project-path "Main" -n "Nested"```.

### Example

Publish samples to the Inside Sales project on the Default site, as user jsmith.

```tabcmd publishsamples -n "Inside Sales" -t "" -s localhost --username "jsmith" --password "secret-password"```
    
## reencryptextracts 

<div class="alert alert-info"><strong>Note</strong>: Tableau Server only.</div>

<! --- Syntax 
tabcmd reencryptextracts [site name] [Global options] --->

Reencrypt all extracts on a site with new encryption keys. This command will regenerate the key encryption key and data encryption key. You must specify a site. For more information, see [Extract Encryption at Rest](https://help.tableau.com/current/server/en-us/security_ear.htm).

Depending on the number and size of extracts, this operation may consume significant server resources. Consider running this command outside of normal business hours.

### Examples

```tabcmd reencryptextracts "Default"```

```tabcmd reencryptextracts "West Coast Sales"```


## refreshextracts *workbook-name* or *datasource-name*

<! --- Syntax 
tabcmd publishsamples [name] [Global options] --->
    
Performs a full or incremental refresh of extracts belonging to the specified workbook or data source.

This command takes the name of the workbook or data source as it appears on the server, not the file name when it was published. Only an administrator or the owner of the workbook or data source is allowed to perform this operation.

<div class="alert alert-info"><strong>Notes:</strong>
<ul>
<li>This method will fail and result in an error if your Server Administrator has disabled the **RunNow** setting for the site. For more information, see [Tableau Server Settings](https://help.tableau.com/current/server/en-us/maintenance_set.htm).</li>
<li>You can use tabcmd to refresh supported data sources that are hosted in the cloud. For example, SQL Server, MySQL, PostgreSQL on a cloud platform; Google Analytics; and so on.</li>
<li>To refresh on-premises data with tabcmd, the data source must be a type that can be configured for Tableau Bridge [Recommended schedules](https://help.tableau.com/current/online/en-us/to_sync_schedule.htm). For all other data sources that connect to on-premises data, you can use Bridge or the command-line data extract utility. Learn more at [Use Bridge to Keep Data Fresh](https://help.tableau.com/current/online/en-us/qs_refresh_local_data.htm) and [Automate Extract Refresh Tasks from the Command Line](https://help.tableau.com/current/online/en-us/to_refresh_extract_commandline.htm).</li>
</ul></div>
    
### Options

\-\-incremental       <div class="alert alert-info">Not yet implemented.</div>

: Run an incremental refresh instead of a full refresh

\-\-synchronous      <div class="alert alert-info">Not yet implemented.</div>

: Adds the full refresh operation to the queue used by the Backgrounder process, to be run as soon as a Backgrounder process is available. If a Backgrounder process is available, the operation is run immediately. The refresh operation appears on the Background Tasks report.

During a synchronous refresh, tabcmd maintains a live connection to the server while the refresh operation is underway, polling every second until the background job is done.

\-\-workbook

: The name of the workbook containing extracts to refresh. If the workbook has spaces in its name, enclose it in quotes.

\-\-datasource

: The name of the data source containing extracts to refresh.: 

\-\-project

: Use with \-\-workbook or \-\-datasource to identify a workbook or data source in a project other than Default. If not specified, the Default project is assumed.

\-\-parent-project-path

: Specifies the name of the parent project for the nested project as specified with the \-\-project option.

For example:

* To specify a project called "Nested" that exists in a "Main" project, use the following syntax:
`--parent-project-path "Main" --project "Nested"`
* To specify a project called "Nested2" that is nested within the "Nested" project:
`--parent-project-path "Main/Nested" --project "Nested2"`

\-\-url

: The name of the workbook as it appears in the URL. A workbook published as “Sales Analysis” has a URL name of “SalesAnalysis”.
    

### Examples

`tabcmd refreshextracts --datasource sales_ds`

`tabcmd refreshextracts --project "Sales External" --datasource sales_ds`

`tabcmd refreshextracts --project "Sales External" --parent-project-path "Main" --project "Sales External" --datasource sales_ds`

`tabcmd refreshextracts --workbook "My Workbook"`

`tabcmd refreshextracts --url SalesAnalysis`

## removeusers *group-name*
    
<! --- Syntax 
tabcmd publishsamples -n [project name] [Global options] --->
    
Removes users from the specified group.

### Options

\-\-users

: Remove the users in the given `.csv` file from the specified group. The file should be a simple list with one user name per line.

\-\-[no-]complete

: Requires that all rows be valid for any change to succeed. If not specified `--complete` is used.

### Example

`tabcmd removeusers "Development" --users "users.csv"`


## runschedule *schedule-name* <div class="alert alert-info"><strong>Note</strong>: Tableau Server only. Not Yet Implemented</div>

<! --- Syntax 
tabcmd runschedule [schedule name] [Global options] --->
    
Runs the specified schedule.

<div class="alert alert-info"><strong>Important</strong>: This command will fail and result in an error if your Server Administrator has disabled the RunNow setting for the site. For more information, see <a href="https://help.tableau.com/current/server/en-us/maintenance_set.htm">Tableau Server Settings</a>.</div>

### Example

```tabcmd runschedule "5AM Sales Refresh"```

## version
Displays the version information for the current installation of the tabcmd utility.

### Example

```tabcmd version```
