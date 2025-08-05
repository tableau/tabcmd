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


def task_combine_property_files():

    """
    For all languages: a) Combines all existing properties files for a language into a single file called 'combined.tmp'
    and b) removes duplicates while preserving the original order of properties
    Also extracts string keys from code and validates all locales have required strings
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
        STRINGS_FILE = "tabcmd/locales/codestrings.tmp"

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

        # Write to codestrings.properties (preserve original order)
        with open(STRINGS_FILE, "w+", encoding="utf-8") as stringfile:
            # Don't sort - preserve order strings were found in code
            for key in all_string_keys:
                stringfile.write(key + "\n")

        print("{} strings collected from code and saved to {}".format(len(all_string_keys), STRINGS_FILE))

    def merge():
        print("\n***** Combine our multiple input properties files into one .properties file per locale")
        # Process English last for cleaner output
        locales_ordered = [loc for loc in LOCALES if loc != "en"] + ["en"]
        for current_locale in locales_ordered:

            LOCALE_PATH = os.path.join("tabcmd", "locales", current_locale)
            INPUT_FILES = os.path.join(LOCALE_PATH, "*.properties")
            OUTPUT_FILE = os.path.join(LOCALE_PATH, "LC_MESSAGES", "combined.tmp")

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

    

    """Search loc files for each string used in code - print an error if not found.
    Uses enhanced check_strings.py script for validation.
    """

    def enforce_strings_present():
        print("\n***** Verify that all string keys are present using check_strings validator")

        # English must be processed FIRST for validation baseline, others can be in any order
        locales_ordered = ["en"] + [loc for loc in LOCALES if loc != "en"]
        result = subprocess.run(
            ["python", "bin/i18n/check_strings.py", "--mode", "build", "--locales"] + locales_ordered,
            capture_output=True,
            text=True,
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



    return {
        "actions": [process_code, merge, enforce_strings_present],
        "verbosity": 2,
    }


def task_po():
    """
    For all languages: generate a .po file from each LC_MESSAGES/combined.tmp file (these are utf-8)
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
        print("\n***** Generate all .po files from combined.tmp")
        subprocess.run(["python", "bin/i18n/prop2po.py", "--help"])
        for current_locale in LOCALES:

            LOC_PATH = os.path.join("tabcmd", "locales", current_locale, "LC_MESSAGES")
            PROPS_FILE = os.path.join(LOC_PATH, "combined.tmp")
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


def task_remove_unused_strings():
    """
    Edit original properties files to remove unused strings that are not referenced in code.
    This permanently modifies the source .properties files, removing bloat.
    """

    def cleanup_properties():
        print("\n***** Clean up properties files by removing unused strings")
        REF_FILE = os.path.join("tabcmd", "locales", "codestrings.tmp")
        CLEANUP_LOG = "cleanup_removed_strings.log"
        
        # Check if codestrings.tmp exists
        if not os.path.exists(REF_FILE):
            print(f"ERROR: {REF_FILE} not found")
            print("Please run 'python -m doit combine_property_files' first to generate the code strings reference file")
            print("This file is needed to identify which strings are actually used in the code")
            exit(1)
        
        # Load required strings from code
        with open(REF_FILE, "r+", encoding="utf-8") as ref:
            required = ref.read()
        
        total_removed = 0
        with open(CLEANUP_LOG, "w", encoding="utf-8") as cleanup_log:
            cleanup_log.write("# Strings removed from properties files during cleanup\n")
            cleanup_log.write("# These strings were present in properties but not used in code\n\n")
            
            # Process English last for cleaner output
            locales_ordered = [loc for loc in LOCALES if loc != "en"] + ["en"]
            for current_locale in locales_ordered:
                LOCALE_PATH = os.path.join("tabcmd", "locales", current_locale)
                
                # Find all .properties files in this locale directory
                properties_files = glob.glob(os.path.join(LOCALE_PATH, "*.properties"))
                
                locale_removed = 0
                for props_file in properties_files:
                    removed_from_file = []
                    kept_lines = []
                    
                    # Read and process the file
                    header_lines = []  # Comments and empty lines at the top
                    string_lines = []  # Key=value entries to keep
                    found_first_entry = False
                    
                    with open(props_file, "r", encoding="utf-8") as infile:
                        for line in infile.readlines():
                            line_stripped = line.strip()
                            if line_stripped == "" or line_stripped.startswith("#"):
                                if not found_first_entry:
                                    # Keep header comments and empty lines at top
                                    header_lines.append(line)
                                # Skip comments/empty lines mixed with entries (will be cleaned up)
                            else:
                                found_first_entry = True
                                key = line_stripped.split("=")[0]
                                if key in required:
                                    # Keep used strings
                                    string_lines.append(line)
                                else:
                                    # Mark unused strings for removal
                                    removed_from_file.append(line.strip())
                                    locale_removed += 1
                    
                    # Write back the cleaned file
                    if removed_from_file or string_lines:  # Write if we removed anything or have content
                        with open(props_file, "w", encoding="utf-8") as outfile:
                            # Write header comments first
                            outfile.writelines(header_lines)
                            
                            # Add separator if we have both header and content
                            if header_lines and string_lines and not header_lines[-1].endswith('\n\n'):
                                if not header_lines[-1].endswith('\n'):
                                    outfile.write('\n')
                                outfile.write('\n')
                            
                            # Write string entries (alphabetizing commented out)
                            # for line in sorted(string_lines, key=lambda x: x.split('=')[0].lower()):
                            for line in string_lines:
                                outfile.write(line)
                        
                        # Log what was removed (only if something was actually removed)
                        if removed_from_file:
                            cleanup_log.write(f"# Removed from {props_file}:\n")
                            for removed_line in removed_from_file:
                                cleanup_log.write(f"{removed_line}\n")
                            cleanup_log.write("\n")
                
                total_removed += locale_removed
                if locale_removed > 0:
                    print(f"Cleaned {current_locale}: removed {locale_removed} unused strings")
                else:
                    print(f"Cleaned {current_locale}: no unused strings found")
        
        if total_removed > 0:
            print(f"\nTotal: {total_removed} unused strings removed from properties files")
            print(f"Removed strings logged to {CLEANUP_LOG}")
        else:
            print("\nNo unused strings found to remove")

    return {
        "actions": [cleanup_properties],
        "verbosity": 2,
    }


def task_clean_temp():

    """remove all generated files such as .po, .out, and pdf, csv etc that are not in the assets folder"""

    def clean_output_files():
        print("todo - delete pdf, csv, .twbx, .hyper etc that have been produced in tests")

    """For all languages: removes all generated intermediate files (properties, po) from the loc build.
    all we need to keep are the provided translation.properties files from the monolith, at locales/[current_locale]
    and the final tabcmd.mo files in LC_MESSAGES generated by
    >doit combine_property_files po mo
    """

    def clean_string_files():
        for current_locale in LOCALES:
            FILESETS = [
                os.path.join("tabcmd", "locales", current_locale, "LC_MESSAGES", "*.out"),
                os.path.join("tabcmd", "locales", current_locale, "LC_MESSAGES", "*.tmp"),
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
    seen = set()  # Track what we've seen
    unique_lines = []  # Preserve order
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
                line_with_newline = line + "\n"
                if line not in seen:  # Only add if we haven't seen it before
                    seen.add(line)
                    unique_lines.append(line_with_newline)

    with open(filename, "w", encoding="utf-8") as my_file:
        my_file.truncate()
        for line in unique_lines:  # Write in original order
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
        print(
            "Saved {} unique lines to {} ({} discarded lines logged to {})".format(
                len(unique_lines), filename, len(discarded_lines), log_filename
            )
        )
    else:
        print("Saved {} unique lines to {}".format(len(unique_lines), filename))
