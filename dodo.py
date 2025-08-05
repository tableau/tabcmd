import glob
import os
import subprocess
import sys
import setuptools_scm

LOCALES = ["en", "de", "es", "fr", "ga", "it", "pt", "sv", "ja", "ko", "zh"]

"""
https://pydoit.org/
Usage:
pip install -e .[localize]
doit list # see available tasks

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

        # Import string extraction logic from check_strings module
        import sys
        from pathlib import Path
        
        # Add bin directory to Python path for imports
        bin_path = str(Path(__file__).parent / "bin")
        if bin_path not in sys.path:
            sys.path.insert(0, bin_path)
            
        from i18n.check_strings import find_python_files, extract_string_keys_from_file

        tabcmd_dir = "tabcmd"
        STRINGS_FILE = "tabcmd/locales/codestrings.properties"

        # Use enhanced string extraction logic
        python_files = find_python_files(tabcmd_dir)
        all_string_keys = set()
        
        # Log files being processed to localize.log
        with open("localize.log", "a", encoding="utf-8") as log_file:
            log_file.write("# Code files processed for string extraction:\n")
            for codefile in python_files:
                log_file.write("\t{}\n".format(codefile))
            log_file.write("\n")
        
        for codefile in python_files:
            file_keys = extract_string_keys_from_file(codefile)
            all_string_keys.update(file_keys)

        # Write to codestrings.properties (same format as before)
        with open(STRINGS_FILE, "w+", encoding="utf-8") as stringfile:
            sorted_keys = sorted(all_string_keys)
            for key in sorted_keys:
                stringfile.write(key + "\n")

        print("{} strings collected from code and saved to {}".format(len(all_string_keys), STRINGS_FILE))

    def merge():
        print("\n***** Combine our multiple input properties files into one .properties file per locale")
        # Process English last for cleaner output
        locales_ordered = [loc for loc in LOCALES if loc != "en"] + ["en"]
        for current_locale in locales_ordered:

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

                        changed_input = re.sub("[\u201c\u201d\u201e]", "'", input)
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
        UNUSED_ENGLISH_FILE = "unused_english_strings.txt"
        
        # Track unused English strings for separate output file
        unused_english_strings = []
        
        # Process English last for cleaner output
        locales_ordered = [loc for loc in LOCALES if loc != "en"] + ["en"]
        for current_locale in locales_ordered:
            LOCALE_PATH = os.path.join("tabcmd", "locales", current_locale)
            IN_FILE = os.path.join(LOCALE_PATH, "LC_MESSAGES", "combined.properties")
            OUT_FILE = os.path.join(LOCALE_PATH, "LC_MESSAGES", "filtered.properties")

            excluded_count = 0
            with open(REF_FILE, "r+", encoding="utf-8") as ref:
                required = ref.read()

                with open(IN_FILE, "r+", encoding="utf-8") as infile, open(OUT_FILE, "w+", encoding="utf-8") as outfile:
                    for line in infile.readlines():
                        key = line.split("=")[0]
                        if key in required:
                            outfile.writelines(line)
                        else:
                            excluded_count += 1
                            # Track unused English strings for output file
                            if current_locale == "en":
                                unused_english_strings.append(line.strip())

            # Show summary for all languages 
            if excluded_count > 0:
                print("Filtered strings for {} (excluded {} unused strings)".format(current_locale, excluded_count))
            else:
                print("Filtered strings for {} (no unused strings)".format(current_locale))
        
        # Write unused English strings to separate file (silently)
        if unused_english_strings:
            with open(UNUSED_ENGLISH_FILE, "w+", encoding="utf-8") as unused_file:
                unused_file.write("# Unused English strings (present in properties but not referenced in code)\n")
                unused_file.write("# Generated by doit properties filter step\n")
                unused_file.write(f"# Found {len(unused_english_strings)} unused strings\n\n")
                
                for unused_string in sorted(unused_english_strings):
                    unused_file.write(unused_string + "\n")
            
            # Store count for final summary (will be printed at end of validation step)
            with open("unused_count.tmp", "w") as count_file:
                count_file.write(str(len(unused_english_strings)))

    """Remove """

    """Search loc files for each string used in code - print an error if not found.
    Uses enhanced check_strings.py script for validation.
    """

    def enforce_strings_present():
        print("\n***** Verify that all string keys are present using check_strings validator")
        
        # English must be processed FIRST for validation baseline, others can be in any order
        locales_ordered = ["en"] + [loc for loc in LOCALES if loc != "en"]
        result = subprocess.run([
            "python", "bin/i18n/check_strings.py", 
            "--mode", "build",
            "--locales"] + locales_ordered,
            capture_output=True, text=True
        )
        
        # Print the output from the validation script
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        if result.returncode != 0:
            print("VALIDATION FAILED: Missing localization strings found")
            exit(1)
        else:
            print("All string validations passed")
        
        # Print unused English strings summary at the end
        if os.path.exists("unused_count.tmp"):
            with open("unused_count.tmp", "r") as count_file:
                unused_count = int(count_file.read().strip())
            print(f"\n{unused_count} unused English strings saved to unused_english_strings.txt")
            os.remove("unused_count.tmp")  # Clean up temp file
        else:
            print("\nNo unused English strings found")

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
    it doesn't have any way to control which encoding it uses so I'm patching it at bin/i18n/prop2po.py
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
    Uses msgfmt.py from gettext, which is copied locally into the repo at bin/i18n/msgfmt.py
    """

    def generate_mo():
        print("\n***** Generate all .mo files from tabcmd.po")
        for current_locale in LOCALES:

            LOC_PATH = "tabcmd/locales/" + current_locale + "/LC_MESSAGES"

            print("\nBegin writing final {}/tabcmd.mo file".format(current_locale))
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
            print("Loading {} file to validate".format(MO_FILE))
            try:
                with open(MO_FILE, "rb") as fp:
                    print("File open - now calling translate ({})".format(current_locale))
                    language: gettext.NullTranslations = gettext.translation(
                        domain, LANG_DIR, languages=[current_locale]
                    )
                    language.install()
                    _ = language.gettext
                    print("\t" + _("common.output.succeeded"))
                    print("\t" + _("session.options.server"))
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
    discarded_lines = []

    with open(filename, "r", encoding="utf-8") as my_file:
        my_file.seek(0)
        lines = my_file.readlines()
        for line in lines:
            line = line.strip()
            # lines cannot extend over two lines.
            line = line.replace("\\n", "  ")
            if line == "":
                continue
            elif "=" not in line and "codestrings" not in filename:
                discarded_lines.append(line)
                continue
            else:
                uniques.add(line + "\n")

    with open(filename, "w", encoding="utf-8") as my_file:
        my_file.truncate()
        for line in uniques:
            my_file.write(line)

    # Write discarded lines to log file
    if discarded_lines:
        log_filename = "localize.log"
        with open(log_filename, "a", encoding="utf-8") as log_file:
            log_file.write("# Lines discarded from {} because prop2po will not like them\n".format(filename))
            log_file.write("# These lines don't contain '=' and are not codestrings\n\n")
            for line in discarded_lines:
                log_file.write(line + "\n")
            log_file.write("\n")  # Add separator between different files
        print("Saved {} sorted unique lines to {} ({} discarded lines logged to {})".format(len(uniques), filename, len(discarded_lines), log_filename))
    else:
        print("Saved {} sorted unique lines to {}".format(len(uniques), filename))
