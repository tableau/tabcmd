import glob
import os
import subprocess
import ftfy
import setuptools_scm

LOCALES = ["en", "de", "es", "fr", "ga", "it", "pt", "sv", "ja", "ko", "zh"]

"""
https://pydoit.org/
Usage:
pip install -e .[prep_work]
doit list # see available tasks

FYI: to read mo and po files use https://poedit.net/download
"""


def task_convert():
    """
    For all languages: Read properties files with unicode like "Schlie\u00dfen", save it back as "Schließen"
    requires: pip install ftfy
    help: https://ftfy.readthedocs.io/
    Run when we copy in updated properties files. NOT IDEMPOTENT: only run on the initial files
    """

    def process_locales():
        for current_locale in LOCALES:
            if current_locale in ["en", "ga"]:  # greek is our pseudo-loc
                continue
            elif current_locale in ["ja", "ko", "zh"]:
                encoding = "utf-8"
            else:
                encoding = "cp1252"

            for file in glob.glob("tabcmd/locales/" + current_locale + "/*.properties"):
                basename = os.path.basename(file).split(".")[0]
                print("transcoding", basename)
                with open(file, encoding=encoding) as infile:
                    data = infile.read()
                # now that we have read in the data properly encoded, fix the \u00fc characters and save as utf-8
                with open(file, "w", encoding="utf-8") as outfile:
                    outfile.write(ftfy.fixes.decode_escapes(data))

    return {
        "actions": [process_locales],
        "verbosity": 2,
    }


def task_po():
    """
    For all languages: generate a .po file from each .properties file
    Run when we copy in updated properties files AFTER task_convert (so all files are utf-8)
    This is idempotent and can be re-run safely
    """

    """
    There are two versions of prop2po:
    - 1.0, available through pip install prop2po, from https://github.com/mivek/prop2po
    it doesn't have any way to control which encoding it uses so I'm patching it
    - 3.x, from pip install translate-toolkit: 
    it copies key->comment, value-> msgid, ""->msgstr which is not at all what we want
    """

    def process_locales():
        for current_locale in LOCALES:
            LOC_PATH = "tabcmd/locales/" + current_locale
            for file in glob.glob(LOC_PATH + "/*.properties"):
                basename = os.path.basename(file).split(".")[0]
                print("processing", basename)
                result = subprocess.run(
                    [
                        "python",
                        "bin/i18n/prop2po.py",
                        "--encoding",
                        "utf-8",  # for the .po header
                        "--language",
                        current_locale,  # for the .po header
                        LOC_PATH + "/" + basename + ".properties",
                        LOC_PATH + "/LC_MESSAGES/" + basename + ".po",
                    ]
                )
                print("\n", result)
                # print("stdout:", result.stdout)
                if not result.returncode == 0:
                    print("stderr:", result.stderr)

    return {
        "actions": [process_locales],
        "verbosity": 2,
    }


def task_clean_all():
    """For all languages: removes all generated artifacts (.po, .mo) which source from properties files."""

    def process_locales():
        for current_locale in LOCALES:
            LOC_PATH = "tabcmd/locales/" + current_locale
            for file in glob.glob(LOC_PATH + "/*.properties"):
                basename = os.path.basename(file).split(".")[0]
                print("deleting", basename + ".*")
                try:
                    os.remove(LOC_PATH + "/LC_MESSAGES/" + basename + ".po")
                except OSError:
                    pass
                try:
                    os.remove(LOC_PATH + "/LC_MESSAGES/" + basename + ".mo")
                except OSError:
                    pass
            try:
                print("deleting", current_locale + ".mo")
                os.remove(LOC_PATH + "/LC_MESSAGES/" + current_locale + ".mo")
            except OSError:
                pass

    return {
        "actions": [process_locales],
        "verbosity": 2,
    }


def task_merge():
    """
    For all languages: Combines all existing po files for a language into a single domain called 'tabcmd'.
    """

    def process_locales():
        for current_locale in LOCALES:
            LOC_PATH = "tabcmd/locales/" + current_locale + "/LC_MESSAGES"

            with open(LOC_PATH + "/tabcmd.po", "w+", encoding="utf-8") as outfile:
                for file in glob.glob(LOC_PATH + "/*.po"):
                    if file.endswith("tabcmd.po"):
                        pass
                    else:
                        print("merging", file)
                        with open(file, encoding="utf-8") as infile:
                            outfile.write(infile.read())
                            outfile.write("\n")

    return {
        "actions": [process_locales],
        "verbosity": 2,
    }


def task_mo():
    """
    For all languages: Processes the tabcmd.po file to produce a final tabcmd.mo file for each language
    Uses msgfmt.py from gettext, which is copied locally into the repo
    """

    def process_locales():
        for current_locale in LOCALES:
            LOC_PATH = "tabcmd/locales/" + current_locale + "/LC_MESSAGES"

            print("writing final tabcmd.mo file")
            # build the single binary file from the .po file
            result = subprocess.run(["python", "bin/i18n/msgfmt.py", LOC_PATH + "/tabcmd"])
            print("\n", result)
            # print("stdout:", result.stdout)
            if not result.returncode == 0:
                print("stderr:", result.stderr)

    return {
        "actions": [process_locales],
        "verbosity": 2,
    }


def task_version():
    """Generates a metadata info file with current version to be bundled by pyinstaller"""

    def write_for_pyinstaller():
        import pyinstaller_versionfile
        import os

        version = setuptools_scm.get_version(local_scheme="no-local-version")
        numeric_version = version.replace("dev", "")
        print("----\n", numeric_version)

        output_file = os.path.join(".", "program_metadata.txt")
        input_file = os.path.join("res", "metadata.yml")
        pyinstaller_versionfile.create_versionfile_from_input_file(
            output_file,
            input_file,
            # optional, can be set to overwrite version information (equivalent to --version when using the CLI)
            version=numeric_version,
        )

    return {
        "actions": [write_for_pyinstaller],
        "verbosity": 2,
    }
