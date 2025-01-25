import json
import os
from app.models.settings import Settings

# Create an instance of Settings or use an existing one
settings_instance = Settings()
settings_instance.load()
# Cache for storing loaded translations
_translation_cache = {}

# Path to the locales directory
_locales_dir = os.path.join(os.path.dirname(__file__), 'locales')

def set_language(language_code):
    """Sets the current language for translations and caches the translations."""
    global settings_instance
    settings_instance.current_language = language_code
    load_locale(language_code)  # Load and cache the translations

def get_language():
    """Gets the current language from settings."""
    return settings_instance.current_language

def load_locale(language_code):
    """Loads the translations for the specified language code into the cache."""
    if language_code in _translation_cache:
        return _translation_cache[language_code]
    
    locale_path = os.path.join(_locales_dir, f"{language_code}.json")
    try:
        with open(locale_path, 'r', encoding='utf-8') as file:
            translations = json.load(file)
        _translation_cache[language_code] = translations
        print(f"Loaded and cached translations for {language_code}.")
        return translations
    except FileNotFoundError:
        print(f"Localization file for {language_code} not found.")
        return {}

def translate(key):
    """Returns the localized string for the given key based on the current language.
       Falls back to English if the key is not found."""
    language_code = get_language()
    translations = load_locale(language_code)
    translation = translations.get(key)
    
    if translation:
        return translation
    else:
        print(f"Key '{key}' not found in {language_code}. Falling back to English.")
        english_translations = load_locale('en')
        return english_translations.get(key, key)

def invalidate_cache(language_code=None):
    """Invalidates the translation cache, either for a specific language or all."""
    if language_code:
        _translation_cache.pop(language_code, None)
    else:
        _translation_cache.clear()
