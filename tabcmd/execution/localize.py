
import locale
import gettext


def set_locale(language: str = None):
    current_locale = validate_lang(language) or get_default_locale() or "en"
    locale_path = "tabcmd/locales/"
    domain = 'tabcmd'

    # fallback=True means if loading the translated files fails, strings will be returned
    language = gettext.translation(domain, localedir=locale_path, languages=[current_locale], fallback=True)
    language.install()  # I believe this is the expensive call
    return language


def get_default_locale():
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
