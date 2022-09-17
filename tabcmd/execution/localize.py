import gettext
import locale
import logging
import os
import sys
from os import listdir
from typing import Any
from typing import Callable

translate = None


# wrapper around the gettext _ function to load it on demand if required
def _(string_key: str) -> str:
    global translate
    if not translate:
        translate = set_client_locale(None, None)
    if not translate:
        translate = _identity_func
    return translate(string_key)


def _identity_func(x: Any) -> Any:
    return "++" + x + "++"


# The client should present text in the OS language, or english if not present.
def set_client_locale(lang: str = None, logger=None) -> Callable:
    if not logger:
        logger = logging.getLogger()

    global translate
    try:
        locale_options = [_validate_lang(lang), _get_default_locale(), "en"]
    except Exception as e:
        print(e)
        locale_options = ["en"]

    logger.debug("Language options: {}".format(locale_options))

    domain = "tabcmd"
    for lang in locale_options:
        try:
            if lang:
                translate = _load_language(lang, domain, logger)
                break
        except Exception as e:
            print("Failed to load language '", lang, "':", e)

    return translate or _identity_func


"""Get absolute path to resource, works for unbundled (e.g dev) and when bundled by PyInstaller"""
# https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741
def resource_path(relative_path):
    """ for unbundled module, return the tabcmd src dir (parent of this file)"""
    src_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    """sys._MEIPASS will only exist in bundled pyinstaller exe, else fall back to unbundled location"""
    base_path = getattr(sys, "_MEIPASS", src_location)
    return os.path.join(base_path, relative_path)


def _load_language(current_locale, domain, logger):
    locale_path = os.path.join(".", "tabcmd", "locales")
    locale_dir = resource_path(locale_path)
    logger.debug("Checking for language resources at " + locale_dir)
    # to debug pyinstaller file bundling, try something like this example debug line
    # logger.debug(listdir(sys._MEIPASS))
    # logger.debug(listdir(locale_dir))

    language: gettext.NullTranslations = gettext.translation(domain, locale_dir, languages=[current_locale])
    language.install()  # I believe this is the expensive call
    _ = language.gettext
    return _


def _get_default_locale():
    current_locale, encoding = locale.getdefaultlocale()
    current_locale = _validate_lang(current_locale)
    return current_locale


def _validate_lang(requested_locale):
    if not requested_locale:
        return None
    if requested_locale in ["en_GB", "fr_CA", "zh_TW"]:
        return requested_locale
    else:
        abbreviated_locale = requested_locale.split("_")[0]
        if abbreviated_locale in ["de", "es", "fr", "ga", "it", "ja", "ko", "pt", "sv", "zh"]:
            return abbreviated_locale
    return None
