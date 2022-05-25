import glob
import os
import subprocess
import ftfy

LOCALES = ["en", "de", "es", "fr", "ga", "it", "pt", "sv", "ja", "ko",  "zh"]

"""
https://pydoit.org/
Usage:
pip install doit
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
        'actions': [process_locales],
        'verbosity': 2,
    }


def task_po():
    """
    For all languages: generate a .po file from each .properties file
    requires: pip install translate-toolkit -- NOT prop2po, it has fewer options (it lacks personality)
    help: http://docs.translatehouse.org/projects/translate-toolkit/en/latest/commands/prop2po.html
    Run when we copy in updated properties files AFTER task_convert - so all files are utf-8
    """
    def process_locales():
        for current_locale in LOCALES:
            for file in glob.glob("tabcmd/locales/"+current_locale+"/*.properties"):
                basename = os.path.basename(file).split(".")[0]
                print("processing", basename)
                result = subprocess.run(["prop2po",
                                         "--personality=java-utf8",
                                         "tabcmd/locales/" + current_locale + "/"+basename+".properties",
                                         "tabcmd/locales/" + current_locale + "/LC_MESSAGES/"+basename+".po"])
                print(result)
                print("stdout:", result.stdout)
                print("stderr:", result.stderr)
    return {
        'actions': [process_locales],
        'verbosity': 2,
    }


def task_clean_all():
    """For all languages: removes all generated artifacts (.po, .mo) which source from properties files. """

    def process_locales():
        for current_locale in LOCALES:
            for file in glob.glob("tabcmd/locales/"+current_locale+"/*.properties"):
                basename = os.path.basename(file).split(".")[0]
                print("deleting",basename + ".*")
                try:
                    os.remove("tabcmd/locales/" + current_locale + "/LC_MESSAGES/"+basename+".po")
                except OSError:
                    pass
                try:
                    os.remove("tabcmd/locales/" + current_locale + "/LC_MESSAGES/" + basename + ".mo")
                except OSError:
                    pass
            try:
                print("deleting", current_locale + ".mo")
                os.remove("tabcmd/locales/" + current_locale + "/LC_MESSAGES/" + current_locale + ".mo")
            except OSError:
                pass


    return {
        'actions': [process_locales],
        'verbosity': 2,
    }


def task_mo():
    """For all languages: Combines all existing po files for a language into a single domain called 'tabcmd'.
        Processes these files to produce a final tabcmd.mo file for each language """

    def process_locales():
        for current_locale in LOCALES:

            try:
                os.remove("tabcmd/locales/" + current_locale + "/LC_MESSAGES/tabcmd.po")
            except OSError:
                pass
            try:
                os.remove("tabcmd/locales/" + current_locale + "/LC_MESSAGES/tabcmd.mo")
            except OSError:
                pass

            LOC_PATH = "tabcmd/locales/" + current_locale

            with open(LOC_PATH + "/LC_MESSAGES/tabcmd.po", 'w', encoding="utf-8") as outfile:
                for file in glob.glob(LOC_PATH + "/LC_MESSAGES/*.po"):
                    if file.endswith("tabcmd.po"):
                        pass
                    else:
                        print("merging", file)
                        with open(file) as infile:
                            for line in infile:
                                outfile.write(line)
                            outfile.write("\n")

            print("writing final tabcmd.mo file")
            # build the single binary file from the combined text .po files
            result = subprocess.run(["bin/i18n/msgfmt.py",
                                     "tabcmd/locales/" + current_locale + "/LC_MESSAGES/tabcmd"])
            print(result)
            print("stdout:", result.stdout)
            print("stderr:", result.stderr)

    return {
        'actions': [process_locales],
        'verbosity': 2,
    }





