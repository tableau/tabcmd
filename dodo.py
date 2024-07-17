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

    

def task_encode_properties():
    """
    For all languages: Read properties files with unicode like "Schlie\u00dfen", save it back as "Schließen"
    requires: pip install ftfy
    help: https://ftfy.readthedocs.io/
    
    Inputs: locales/*_[locale]/LC_MESSAGES/combined.properties files - all in the top level folder for ease of importing them
    Output: (generated clean each run) locales/[locale]/LC_MESSAGES/transcoded.properties file
    This should NOT edit the input files, therefore it should be idempotent.
    """

    def process_locales():
        for current_locale in LOCALES:
            # I'm not sure why we were varying the locale before, but this seems to work fine
            encoding = "utf-8"

            LOCALE_PATH = os.path.join("tabcmd", "locales", current_locale, "LC_MESSAGES")
            INPUT_FILE = os.path.join(LOCALE_PATH, "combined.properties.sorted")
            OUTPUT_FILE = os.path.join(LOCALE_PATH, "transcoded.properties")
            print("Collecting strings for " + current_locale)
            try:
                with open(INPUT_FILE, "r", encoding=encoding, errors='backslashreplace') as infile:
                    data = infile.read()
                # now that we have read in the data properly encoded, fix the \u00fc characters and save as utf-8
                with open(OUTPUT_FILE, "w", encoding="utf-8", errors='backslashreplace') as outfile:
                    outfile.write(ftfy.fixes.decode_escapes(data))
                print("Done!")
            except Exception as e:
                print("!!!!failed to collect strings for {}".format(current_locale))
                print(e)

    return {
        "actions": [process_locales],
        "verbosity": 2,
    }

def task_po():
    """
    For all languages: generate a .po file from each LC_MESSAGES/combined.properties file (these are utf-8)
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

            LOC_PATH = os.path.join("tabcmd", "locales", current_locale, "LC_MESSAGES")
            PROPS_FILE = os.path.join(LOC_PATH, "transcoded.properties")
            PO_FILE = os.path.join(LOC_PATH, "tabcmd.po")
            LOG_FILE = os.path.join(LOC_PATH, "prop2po.out")
            with open(LOG_FILE, "w+", encoding="utf-8") as logfile:
                try:
                    result = subprocess.run(
                        [
                            "python",
                            "bin/i18n/prop2po.py",
                            "--encoding",
                            "utf-8",  # for the .po header
                            "--language",
                            current_locale,  # for the .po header
                            PROPS_FILE,
                            PO_FILE
                        ], 
                        stdout=logfile,
                        stderr=logfile
                    )
                    print("Written from {} to {}".format(PROPS_FILE, PO_FILE))
                except Exception as e:
                    print("run for {} failed with exception".format(current_locale))
                    print("see log file {}".format(LOG_FILE))
        
                if not result.returncode == 0:
                    print("FAILED")
                    print("see log file {}".format(LOG_FILE))

    return {
        "actions": [process_locales],
        "verbosity": 2,
    }


def task_clean_all():
    """For all languages: removes all generated artifacts (.po, .mo) which source from properties files."""

    def process_locales():
        for current_locale in LOCALES:
            LOC_PATH = os.path.join("tabcmd", "locales", current_locale, "LC_MESSAGES", "*")
            for file in glob.glob(LOC_PATH):
                print("deleting {}".format(os.path.basename(file)))
                try:
                    os.remove(file)
                except OSError:
                    pass
    return {
        "actions": [process_locales],
        "verbosity": 2,
    }


def task_merge_properties():
    """
    For all languages: Combines all existing properties files for a language into a single file called 'combined.properties'.
    """

    def process_locales():
        for current_locale in LOCALES:

            LOCALE_PATH = os.path.join("tabcmd", "locales", current_locale)
            INPUT_FILES = os.path.join(LOCALE_PATH, "*.properties")
            OUTPUT_FILE = os.path.join(LOCALE_PATH, "LC_MESSAGES", "combined.properties")

            with open(OUTPUT_FILE, "w+", encoding="utf-8") as outfile:
                for file in glob.glob(INPUT_FILES):
                    with open(file, encoding="utf-8") as infile:
                        outfile.write(infile.read())
                        outfile.write("\n")
            print("Combined strings for {}".format(current_locale))
            sort_and_filter_file(OUTPUT_FILE)

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
            
            
        print("it sure would be nice if there was some automated way to validate that I got a good .mo filedoit ")

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


# local method, not exposed as a task
def sort_and_filter_file(filename):
    uniques = []
    
    with open(filename, "r+", encoding="utf-8") as my_file:
        lines = my_file.readlines()
        # add this back later, for now it's interfering with file diffs lines.sort()
        for line in lines:
            line = line.strip()
            # lines cannot extend over two lines. 
            line = line.replace("\\n", "  ")
            if line == "":
                continue
            elif "=" not in line and "codestrings" not in filename :
                print("prop2po will not like this line. Discarding [{}]".format(line))
            elif not line in uniques:
                uniques.append(line + "\n")
                
    new_file_name = filename + ".sorted"
    with open(new_file_name, "w+", encoding="utf-8") as new_file:
        for line in uniques:
            new_file.write(line)
            
    print("Saved {} sorted unique lines to {}".format(len(uniques), new_file_name))
