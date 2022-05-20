import glob
import os
import subprocess

LOCALES = ["en","de", "es", "fr", "ga", "it", "ja", "ko", "pt", "sv", "zh"]

def task_mo():
    """generate a locales .mo file from .po file.   Use task locales_combine to produce final result"""

    def process_locales():
        for current_locale in LOCALES:
            for file in glob.glob("tabcmd/locales/"+current_locale+"/LC_MESSAGES/*.po"):
                basename = os.path.basename(file).split(".")[0]
                print("processing",basename)
                subprocess.run(["bin/i18n/msgfmt.py", "-o",
                                "tabcmd/locales/" + current_locale + "/LC_MESSAGES/"+basename+".mo",
                                "tabcmd/locales/" + current_locale + "/LC_MESSAGES/"+basename])
    return {
        'actions': [process_locales],
        'verbosity': 2,
    }

def task_po():
    """generate a locales .po file from .prooerties file """

    def process_locales():
        for current_locale in LOCALES:
            for file in glob.glob("tabcmd/locales/"+current_locale+"/*.properties"):
                basename = os.path.basename(file).split(".")[0]
                print("processing",basename)
                subprocess.run(["prop2po",
                                "tabcmd/locales/" + current_locale + "/"+basename+".properties",
                                "tabcmd/locales/" + current_locale + "/LC_MESSAGES/"+basename+".po"])
    return {
        'actions': [process_locales],
        'verbosity': 2,
    }

def task_locale_clean():
    """ removes all locale generate artifacts which source from properties files. """

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

def task_locale_combine():
    """ compbines all generated po, mo files inta a single domain called 'tabcmd'.   Produces the final tabcmd.mo file """

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

            with open(LOC_PATH + "/LC_MESSAGES/tabcmd.po", 'w') as outfile:
                for file in glob.glob(LOC_PATH + "/LC_MESSAGES/*.po"):
                    if(file.endswith("tabcmd.po")):
                        pass
                    else:
                        print("processing", file)
                        with open(file) as infile:
                            for line in infile:
                                outfile.write(line)
                            outfile.write("\n")

            print("writing final tabcmd.mo file")
            # build the single binary file from the combined text .po files
            result = subprocess.run(["bin/i18n/msgfmt.py", "-o",
                        "tabcmd/locales/" + current_locale + "/LC_MESSAGES/tabcmd.mo",
                        "tabcmd/locales/" + current_locale + "/LC_MESSAGES/tabcmd"])
            print("stdout:", result.stdout)
            print("stderr:", result.stderr)

    return {
        'actions': [process_locales],
        'verbosity': 2,
    }





