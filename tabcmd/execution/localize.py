import locale
import gettext
from typing import Any
from typing import Callable
import sys
import os


translate = None


# wrapper around the gettext _ function to load it on demand if required
def _(string_key: str) -> str:
    global translate
    if not translate:
        translate = set_client_locale(None, None)
    return translate(string_key)


def _identity_func(x: Any) -> Any:
    return x


# The client should present text in the OS language, or english if not present.
def set_client_locale(lang: str = None, logger=None) -> Callable:
    logger = logger or _identity_func
    global translate
    try:
        locale_options = [_validate_lang(lang), _get_default_locale(), "en"]
    except Exception as e:
        locale_options = ["en"]

    logger("Language options: {}".format(locale_options))

    locale_path = os.path.join(os.path.dirname(__file__), "..", "..", "tabcmd", "locales")
    domain = "tabcmd"

    for lang in locale_options:
        try:
            if lang:
                translate = _load_language(lang, domain, locale_path)
                break
        except Exception as e:
            print("Failed to load language '", lang, "':", e)

    return translate or _identity_func


# Handling file locations in unbundled (e.g dev) layout and when bundled by pyinstaller
# https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def _load_language(current_locale, domain, locale_path):

    # fallback=True means if loading the translated files fails, strings will be returned
    # ?cant use fallback here because we switch to properties files references
    language: gettext.NullTranslations = gettext.translation(
        domain, localedir=resource_path(locale_path), languages=[current_locale], fallback=False
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
