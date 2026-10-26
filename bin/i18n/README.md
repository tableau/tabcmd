
### Strings and localization

New text should not be hardcoded into the python, but added to `tabcmd/locales/en/extra.properties` (or directly to `tabcmd/locales/en/tabcmd_messages_en.properties`). The English properties file is given to the translation team, and they return a translated copy for each supported locale. Until translations return, non-English users automatically see the English string via per-key fallback in gettext (see `tabcmd/execution/localize.py`).

To handle localizing text we use the python standard library tool [gettext](https://docs.python.org/3/library/gettext.html). This expects .mo files. There is no direct .properties -> .mo tool so we go through .po format.
(FYI: to read .mo files for debugging use https://poedit.net/download)

Missing string keys are validated on every PR by `.github/workflows/check-strings.yml`, which runs `python bin/i18n/check_strings.py`. Run it locally the same way before pushing.

## Regenerating .mo bundles

Run these when properties files change. Each step is idempotent and will overwrite the existing output. More details about implementation are in the script code at `dodo.py`.

Or run the full pipeline in one command:
> python -m doit localize

Individual steps:

1. Combine .properties files into a single per-locale `combined.tmp`. Discards strings not present in code and normalizes curly quotes.
> python -m doit properties

2. Convert each `combined.tmp` into a human-readable .po file:
> python -m doit po

3. Convert the .po files into binary .mo files. Also validates each .mo by loading it with gettext:
> python -m doit mo

## Optional reorganization task

Move all strings from `extra.properties` to the bottom of `tabcmd_messages_xx.properties`:
> python -m doit move_tabcmd_strings

This consolidates all strings into the main tabcmd_messages files and clears the extra.properties files.