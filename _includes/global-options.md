The following options are used by all tabcmd commands. The `--server`, `--user`, and `--password` options are required at least once to begin a session. An authentication token is stored so subsequent commands can be run without including these options. This token remains valid for five minutes after the last command that used it.

-h, \-\-help

: Displays the help for the command.

<div class="alert alert-info"><strong>Note</strong>: Some commands listed may not apply when using tabcmd with Tableau Online.</div>

-s, \-\-server

: The Tableau Online URL, which is required at least once to begin session.

-u, \-\-user

: The Tableau Online username, which is required at least once to begin session.

-p, \-\-password

: The Tableau Online password, which is required at least once to begin session.

\-\-password-file

: Allows the password to be stored in the given .txt file rather than the command line for increased security.

-t, \-\-site

: Indicates that the command applies to the site specified by the Tableau Online site ID, surrounded by single quotes or double quotes. Use this option if the user specified is associated with more than one site. Site ID is case-sensitive when using a cached authentication token. If you do not match case you may be prompted for a password even if the token is still valid.

\-\-no-prompt

: When specified, the command will not prompt for a password. If no valid password is provided the command will fail.

\-\-[no-]cookie

: When specified, the session ID is saved on login so subsequent commands will not need to log in. Use the no- prefix to not save the session ID. By default, the session is saved.

\-\-timeout

: Waits the specified number of seconds for the server to complete processing the command. By default, the process will wait until the server responds.

\-\-

: Specifies the end of options on the command line. You can use \-\- to indicate to tabcmd that anything that follows \-\- should not be interpreted as an option setting and can instead be interpreted as a value for the command. This is useful if you need to specify a value in the command that includes a hyphen. The following example shows how you might use \-\- in a tabcmd command, where -430105/Sheet1 is a required value for the export command.

```tabcmd export --csv -f "D:\export10.csv" -- -430105/Sheet1```
