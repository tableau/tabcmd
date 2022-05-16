import locale
import gettext
from typing import Any
from typing import Callable


def _identity_func(x: Any) -> Any:
    x


# The client should present text in the OS language, or english if not present.
def set_client_locale() -> Callable:
    try:
        current_locale = _get_default_locale() or "en"
        locale_path = "tabcmd/locales/"
        domain = "tabcmd"

        # fallback=True means if loading the translated files fails, strings will be returned
        language: gettext.NullTranslations = gettext.translation(
            domain, localedir=locale_path, languages=[current_locale], fallback=True
        )
        language.install()  # I believe this is the expensive call
        _ = language.gettext
    except Exception as e:
        print(e)
        _ = _identity_func
    return _


def _get_default_locale():
    current_locale, encoding = locale.getdefaultlocale()
    current_locale = validate_lang(current_locale)
    return current_locale


def validate_lang(requested_locale):
    if not requested_locale:
        return None
    if requested_locale in ["en_GB", "fr_CA", "zh_TW"]:
        return requested_locale
    else:
        abbreviated_locale = requested_locale.split("_")[0]
        if abbreviated_locale in ["de", "es", "fr", "ga", "it", "ja", "ko", "pt", "sv", "zh"]:
            return abbreviated_locale
    return None


_ = set_client_locale()
