from typing import Optional
import os

from mcdreforged.api.types import PluginServerInterface
from mcdreforged.translation.translation_manager import TranslationManager

from .translation_manager import MyTranslationManager
from .config import Config
from .command import register_commands


real_translation_manager: Optional[TranslationManager] = None


def on_load(server: PluginServerInterface, old):
    global real_translation_manager
    register_commands(server)
    config = server.load_config_simple("mcdr_i18n_injector.json", in_data_folder=False, target_class=Config)
    os.makedirs(config.i18n_files_dir, exist_ok=True)
    if config.language is None:
        server.logger.warning("Language not set, using language setting in MCDR")
        return
    i18n_file = os.path.join(config.i18n_files_dir, config.language + ".yml")
    if not os.path.isfile(i18n_file):
        server.logger.info("Cannot find language file %s, using language setting in MCDR", i18n_file)
        return
    real_translation_manager = server._mcdr_server.translation_manager
    my_translation_manager = MyTranslationManager.from_translation_manager(real_translation_manager)
    my_translation_manager.load_translation(i18n_file)
    server.logger.info("Patching TranslationManager")
    server._mcdr_server.translation_manager = my_translation_manager
    server.logger.info("Setting language to %s", config.language)
    server._mcdr_server.translation_manager.set_language(config.language)


def on_unload(server: PluginServerInterface):
    if real_translation_manager is not None:
        server.logger.info("Unpatching TranslationManager")
        server._mcdr_server.translation_manager = real_translation_manager
