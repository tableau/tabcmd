
import os
import locale
import gettext
import subprocess

domain = 'remove_users_command'
current_locale, encoding = locale.getdefaultlocale()

if current_locale not in ["en_GB", "fr_CA",  "zh_TW"]:
    abbreviated_locale = current_locale.split("_")[0]
    if abbreviated_locale not in ["de", "es", "fr", "ga", "it", "ja", "ko", "pt", "sv", "zh"]:
        current_locale = "en"

current_directory = os.path.dirname(__file__)
# locale_path = current_directory + '/locales/' + current_locale + '/LC_MESSAGES/'
locale_path = "tabcmd/locales/"

# Have this run as a part of setup.py?
# subprocess.run(["tabcmd/i18n/pygettext.py", "-d", "remove_users_command", "-o",
#                 "tabcmd/locales/"+current_locale+"/LC_MESSAGES/remove_users_command.po",
#                 "tabcmd/commands/user/remove_users_command.py"])
subprocess.run(["tabcmd/i18n/msgfmt.py", "-o",
                "tabcmd/locales/"+current_locale+"/LC_MESSAGES/remove_users_command.mo",
                "tabcmd/locales/"+current_locale+"/LC_MESSAGES/remove_users_command"])


language = gettext.translation(domain, localedir=locale_path, languages=[current_locale], fallback = True)
language.install()
_ = language.gettext  # Greek
