import locale
import gettext
from typing import Any
from typing import Callable
import os


translate = None

# wrapper around the gettext _ function to load it on demand if required
def _(string_key: str) -> str:
    global translate
    if not translate:
        print("Lazy loading a language")
        translate = set_client_locale(None)
    return translate(string_key)


def _identity_func(x: Any) -> Any:
    x


# The client should present text in the OS language, or english if not present.
def set_client_locale(lang: str = None) -> Callable:
    global translate
    try:
        locale_options = [_validate_lang(lang), _get_default_locale(), "en"]
    except Exception as e:
        locale_options = ["en"]
    print("Language options: ", locale_options)

    locale_path = os.path.join(os.path.dirname(__file__), "..", "..", "tabcmd", "locales")
    domain = "tabcmd"

    for lang in locale_options:
        try:
            if lang:
                translate = _load_language(lang, domain, locale_path)
                break
        except Exception as e:
            print("Failed to load language ", lang, ":", e)

    return translate or _identity_func


def _load_language(current_locale, domain, locale_path):
    # fallback=True means if loading the translated files fails, strings will be returned
    # ?cant use fallback here because we switch to properties files references
    language: gettext.NullTranslations = gettext.translation(
        domain, localedir=locale_path, languages=[current_locale], fallback=False
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
