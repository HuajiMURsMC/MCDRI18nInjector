from typing import Optional
import os

from mcdreforged.translation.translation_manager import TranslationManager
from mcdreforged.utils import translation_util
from ruamel.yaml import YAML


class MyTranslationManager(TranslationManager):
    @classmethod
    def from_translation_manager(cls, translation_manager: TranslationManager):
        instance = cls(translation_manager.logger)
        instance.language = translation_manager.language
        instance.translations = translation_manager.translations
        instance.available_languages = translation_manager.available_languages
        return instance

    def load_translation(self, file_path: str, fallback: Optional[str] = None):
        self.logger.info("Loading translation file %s", file_path)
        language, _ = os.path.basename(file_path).rsplit('.', 1)
        try:
            with open(os.path.join(file_path), encoding='utf8') as file_handler:
                translations = dict(YAML().load(file_handler))
            for key, text in translation_util.unpack_nest_translation(translations).items():
                self.translations[key][language] = text
            self.available_languages.add(language)
            self.logger.debug('Loaded translation for %s with %d entries', language, len(translations))
            if fallback is not None:
                for key, translation in self.translations.items():
                    if translation.get(language) is None:
                        translation[language] = translation[fallback]
        except Exception:
            self.logger.exception('Failed to load language %s from "%s"', language, file_path)
