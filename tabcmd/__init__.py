

import os
import locale
import gettext
import subprocess

domain = 'create_group_command'
current_locale, encoding = locale.getdefaultlocale()
current_directory = os.path.dirname(__file__)
# locale_path = current_directory + '/locales/' + current_locale + '/LC_MESSAGES/'
locale_path = "tabcmd/locales/"

# subprocess.run(["tabcmd/i18n/pygettext.py", "-d", "create_group_command", "-o",
#                 "tabcmd/locales/el_GR/LC_MESSAGES/create_group_command.po",
#                 "tabcmd/commands/group/create_group_command.py"])
# subprocess.run(["tabcmd/i18n/msgfmt.py", "-o",
#                 "tabcmd/locales/el_GR/LC_MESSAGES/create_group_command.mo",
#                 "tabcmd/locales/el_GR/LC_MESSAGES/create_group_command"])


language = gettext.translation(domain, localedir=locale_path, languages=["el_GR"], fallback = True)
language.install()
_ = language.gettext  # Greek
#
# print(_("helloworld"))