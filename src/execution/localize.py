import gettext
import locale
import logging
import os
import sys
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
    return x


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
                translate = _load_language(lang, domain)
                break
        except Exception as e:
            print("Failed to load language '", lang, "':", e)

    return translate or _identity_func


# Handling file locations in unbundled (e.g dev) layout and when bundled by pyinstaller
# https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    print("2:", base_path, relative_path)
    return os.path.join(base_path, relative_path)


def _load_language(current_locale, domain):
    locale_path = os.path.join("..", "locales")
    print("1:", locale_path)

    # fallback=True means if loading the translated files fails, strings will be returned
    # we use the identity function above instead
    locale_dir = resource_path(locale_path)
    print("3:", locale_dir)
    language: gettext.NullTranslations = gettext.translation(
        domain, locale_dir, languages=[current_locale], fallback=False
    )
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
