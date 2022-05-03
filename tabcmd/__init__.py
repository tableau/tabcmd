
import os
import locale
import gettext
import subprocess

domain = 'create_site_users'
current_locale, encoding = locale.getdefaultlocale()

if current_locale not in ["en_GB", "fr_CA",  "zh_TW"]:
    abbreviated_locale = current_locale.split("_")[0]
    if abbreviated_locale not in ["de", "es", "fr", "ga", "it", "ja", "ko", "pt", "sv", "zh"]:
        current_locale = "en"

current_directory = os.path.dirname(__file__)
# locale_path = current_directory + '/locales/' + current_locale + '/LC_MESSAGES/'
locale_path = "tabcmd/locales/"

# Have this run as a part of setup.py?
# subprocess.run(["tabcmd/i18n/pygettext.py", "-d", "create_site_users", "-o",
#                 "tabcmd/locales/"+current_locale+"/LC_MESSAGES/create_site_users.po",
#                 "tabcmd/commands/user/create_site_users.py"])
subprocess.run(["tabcmd/i18n/msgfmt.py", "-o",
                "tabcmd/locales/"+current_locale+"/LC_MESSAGES/create_site_users.mo",
                "tabcmd/locales/"+current_locale+"/LC_MESSAGES/create_site_users"])


language = gettext.translation(domain, localedir=locale_path, languages=[current_locale], fallback = True)
language.install()
_ = language.gettext  # Greek
