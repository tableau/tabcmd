import glob
import os
import subprocess
import setuptools_scm

LOCALES = ["en", "de", "es", "fr", "ga", "it", "pt", "sv", "ja", "ko", "zh"]

"""
https://pydoit.org/
Usage:
pip install -e .[prep_work]
doit list # see available tasks

FYI: to read mo and po files use https://poedit.net/download
"""


def task_properties():

    """
    For all languages: a) Combines all existing properties files for a language into a single file called 'combined.properties'
    and b) sorts that into an alphabetical list of unique properties in combined.properties.sorted
    I've also included tasks that find all strings in code so we can skip bundling messages that aren't ever used
    """

    """Searches product code for all localization string keys"""

    def process_code():
        print("\n***** Collect all string keys used in code")

        CODE_PATH = "tabcmd/[ec]*/**/*.py"
        STRINGS_FILE = "tabcmd/locales/codestrings.properties"
        STRING_FLAG = '_("'
        STRING_END = '")'

        lines = set([])
        with open(STRINGS_FILE, "w+", encoding="utf-8") as stringfile:
            for codefile in glob.glob(CODE_PATH):
                with open(codefile, encoding="utf-8") as infile:
                    # find lines that contain a loc string in the form _("string goes here")
                    for line in infile:
                        i = line.find(STRING_FLAG)
                        # include only the string itself and the quote symbols around it
                        if i >= 0:
                            j = line.find(STRING_END)
                            lines.add(line[i + 3 : j] + "\n")

            sorted_lines = sorted(lines)
            stringfile.writelines(sorted_lines)

        print("{} strings collected from code and saved to {}".format(len(lines), STRINGS_FILE))

    def merge():
        print("\n***** Combine our multiple input properties files into one .properties file per locale")
        for current_locale in LOCALES:

            LOCALE_PATH = os.path.join("tabcmd", "locales", current_locale)
            INPUT_FILES = os.path.join(LOCALE_PATH, "*.properties")
            OUTPUT_FILE = os.path.join(LOCALE_PATH, "LC_MESSAGES", "combined.properties")

            with open(OUTPUT_FILE, "w+", encoding="utf-8") as outfile:
                for file in glob.glob(INPUT_FILES):
                    with open(file, encoding="utf-8") as infile:
                        input = infile.read()
                        # remove curly quotes that are not expected in command line text/may not work for some users
                        # U201C, U201D and U201E - opening quotes, German opening quotes, and closing quotes
                        import re

                        changed_input = re.sub("[\u201c\u201d\u201e]", input)
                        # some strings for some reason use two single quotes as a double quote. Reduce to one single quote.
                        re_changed_input = re.sub("''", "'", changed_input)
                        outfile.write(re_changed_input)
                        outfile.write("\n")
            print("Combined strings for {} to {}".format(current_locale, OUTPUT_FILE))
            uniquify_file(OUTPUT_FILE)

    """
    Delete strings that aren't used in the code, to keep size down and not waste time fixing unused strings
    Input: combined.properties.sorted
    Output: filtered.properties
    """

    def filter():
        print("\n***** Remove strings in properties that are never used in code")
        REF_FILE = os.path.join("tabcmd", "locales", "codestrings.properties")
        for current_locale in LOCALES:
            LOCALE_PATH = os.path.join("tabcmd", "locales", current_locale)
            IN_FILE = os.path.join(LOCALE_PATH, "LC_MESSAGES", "combined.properties")
            OUT_FILE = os.path.join(LOCALE_PATH, "LC_MESSAGES", "filtered.properties")

            with open(REF_FILE, "r+", encoding="utf-8") as ref:
                required = ref.read()

                with open(IN_FILE, "r+", encoding="utf-8") as infile, open(OUT_FILE, "w+", encoding="utf-8") as outfile:
                    for line in infile.readlines():
                        key = line.split("=")[0]
                        if key in required:
                            outfile.writelines(line)

            print("Filtered strings for {}".format(current_locale))

    """Remove """

    """Search loc files for each string used in code - print an error if not found.
    Input: codestrings.properties file created by task_collect_strings
    Output: console listing missing keys    
    """

    def enforce_strings_present():

        print("\n***** Verify that all string keys used in code are present in string properties")
        STRINGS_FILE = "tabcmd/locales/codestrings.properties"
        uniquify_file(STRINGS_FILE)
        with open(STRINGS_FILE, "r+", encoding="utf-8") as stringfile:
            codestrings = stringfile.readlines()
            for locale in LOCALES:
                LOC_FILE = os.path.join("tabcmd", "locales", locale, "LC_MESSAGES", "filtered.properties")
                print("checking language {}".format(locale))
                with open(LOC_FILE, "r+", encoding="utf-8") as propsfile:
                    translated_strings = propsfile.read()
                    for message_key in codestrings:
                        message_key = message_key.strip("\n")
                        message_key = message_key.strip('"')
                        if message_key not in translated_strings:
                            print("ERROR: product string not in strings files [{}]".format(message_key))
        print("Done")

    return {
        "actions": [process_code, merge, filter, enforce_strings_present],
        "verbosity": 2,
    }


def task_po():
    """
    For all languages: generate a .po file from each LC_MESSAGES/filtered.properties file (these are utf-8)
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
        print("\n***** Validate all .po files from filtered.properties")
        subprocess.run(["python", "bin/i18n/prop2po.py", "--help"])
        for current_locale in LOCALES:

            LOC_PATH = os.path.join("tabcmd", "locales", current_locale, "LC_MESSAGES")
            PROPS_FILE = os.path.join(LOC_PATH, "filtered.properties")
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
                            "--project",
                            "Tabcmd 2",
                            "--copyright",
                            "©2024 Salesforce, Inc.",
                            PROPS_FILE,
                            PO_FILE,
                        ],
                        stdout=logfile,
                        stderr=logfile,
                    )
                    print("Written from {} to {}".format(PROPS_FILE, PO_FILE))
                except Exception as e:
                    print("run for {} failed with exception".format(current_locale))
                    print("see log file {}".format(LOG_FILE))
                    exit(1)

                if not result.returncode == 0:
                    print("FAILED")
                    print("see log file {}".format(LOG_FILE))
                    exit(1)
        print("Done")

    return {
        "actions": [process_locales],
        "verbosity": 2,
    }


def task_clean_all():

    """remove all generated files such as .po, .out, and pdf, csv etc that are not in the assets folder"""

    def clean_output_files():
        print("todo - delete pdf, csv, .twbx, .hyper etc that have been produced in tests")

    """For all languages: removes all generated intermediate files (properties, po) from the loc build.
    all we need to keep are the provided translation.properties files from the monolith, at locales/[current_locale]
    and the final tabcmd.mo files in LC_MESSAGES generated by
    >doit properties po mo
    """

    def clean_string_files():
        for current_locale in LOCALES:
            FILESETS = [
                os.path.join("tabcmd", "locales", current_locale, "LC_MESSAGES", "*.properties"),
                os.path.join("tabcmd", "locales", current_locale, "LC_MESSAGES", "*.po"),
                os.path.join("tabcmd", "locales", current_locale, "LC_MESSAGES", "*.out"),
            ]
            for PATH in FILESETS:
                for file in glob.glob(PATH):
                    print("deleting {}".format(os.path.abspath(file)))
                    try:
                        os.remove(file)
                    except OSError:
                        pass

        STRING_FILES = os.path.join("tabcmd", "locales", "codestrings.*")
        for file in glob.glob(STRING_FILES):
            print("deleting {}".format(os.path.abspath(file)))
            try:
                os.remove(file)
            except OSError:
                pass

    return {
        "actions": [clean_string_files, clean_output_files],
        "verbosity": 2,
    }


def task_mo():
    """
    For all languages: Processes the tabcmd.po file to produce a final tabcmd.mo file for each language
    Uses msgfmt.py from gettext, which is copied locally into the repo
    """

    def generate_mo():
        print("\n***** Generate all .mo files from tabcmd.po")
        for current_locale in LOCALES:

            LOC_PATH = "tabcmd/locales/" + current_locale + "/LC_MESSAGES"

            print("\twriting final {}/tabcmd.mo file".format(current_locale))
            # build the single binary file from the .po file
            # a number of keys are failing at the write-to-mo step. We don't use any of them so that's fine for now.
            result = subprocess.run(["python", "bin/i18n/msgfmt.py", LOC_PATH + "/tabcmd"])
            print(result)
        print("\n")

    import gettext

    """
    This calls gettext directly to imitate what we do when the program actually starts up
    It's the most reliable way to actually verify that the .mo file works
    e.g typical error: charset value is not set in .mo header
    BUT it still doesn't guarantee that the packaging is right, so you still have to 
    actually package and then run the app
    """

    def check_mo():
        print("\n****** Validate all generated .mo files")
        for current_locale in LOCALES:
            LANG_DIR = os.path.join("tabcmd", "locales")
            LOC_DIR = os.path.join(LANG_DIR, current_locale, "LC_MESSAGES")
            MO_FILE = os.path.join(LOC_DIR, "tabcmd.mo")
            domain = "tabcmd"
            print("\tloading {} file to validate".format(MO_FILE))
            try:
                with open(MO_FILE, "rb") as fp:
                    print("\topened file - now calling translate {}".format(current_locale))
                    language: gettext.NullTranslations = gettext.translation(
                        domain, LANG_DIR, languages=[current_locale]
                    )
                    language.install()
                    _ = language.gettext
                    print(_("common.output.succeeded"))
            except Exception as e:
                print(e)

    return {
        "actions": [generate_mo, check_mo],
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
def uniquify_file(filename):
    uniques = set([])

    with open(filename, "r", encoding="utf-8") as my_file:
        my_file.seek(0)
        lines = my_file.readlines()
        for line in lines:
            line = line.strip()
            line = line.strip('"')
            # lines cannot extend over two lines.
            line = line.replace("\\n", "  ")
            if line == "":
                continue
            elif "=" not in line and "codestrings" not in filename:
                print("prop2po will not like this line. Discarding [{}]".format(line))
                continue
            else:
                uniques.add(line + "\n")

    with open(filename, "w", encoding="utf-8") as my_file:
        my_file.truncate()
        for line in uniques:
            my_file.write(line)

    print("Saved {} sorted unique lines to {}".format(len(uniques), filename))
