
### Strings and localization

New text should not be hardcoded into the python, but added to tabcmd/locales/en/extra.properties. This file can be given to the translation team and they will return a copy for each other language. Until then, the english string will be used as a fallback.

To handle localizing text we used the python standard library tool [gettext](https://docs.python.org/3/library/gettext.html). This expects .mo files. I couldn't find a tool that transformed .properties -> .mo directly so we go through .po format. 
(FYI: to read mo files for debugging use https://poedit.net/download)


These steps are separated for easier troubleshooting: each step is idempotent and will overwrite the existing output. More details about implementation are in the script code at dodo.py

1. convert strings from .properties files to .mo for bundling
This step combines the .properties files into a single file, discarding any strings that are not present in code and normalizing curly quotes and unrecognized characters in the strings it keeps. (These files are separate because they are pulled from separate translation sources internally.)
> python -m doit combine_property_files

2. Convert the combined .properties file into a .po file (these are human readable)
> python -m doit po

3. Convert the .po files into .mo files (these are not human readable)
This also checks the .mo files for validity by loading them with gettext
> python -m doit mo