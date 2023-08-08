from ruamel import yaml

from mcdreforged.api.command import *
from mcdreforged.api.types import PluginServerInterface, ConsoleCommandSource


def dump_lang(src: ConsoleCommandSource, ctx: dict):
    language = ctx["language"]
    server = src.get_server()
    translation_manager = server._mcdr_server.translation_manager
    if language not in translation_manager.available_languages:
        server.logger.error("Unknown language: %s", language)
        return
    server.logger.info("Dumping translation data of language %s", language)
    translations = {}
    for key, translation in translation_manager.translations.items():
        if translation:
            translations[key] = translation[language]
    with open(language + "_dump.yml", "w", encoding="utf8") as f:
        yaml.round_trip_dump(translations, f)
    server.logger.info("Dumped %d entries", len(translations))


def register_commands(server: PluginServerInterface):
    server.register_command(
        Literal("!!dumplang")
        .requires(lambda src: src.is_console)
        .then(Text("language").runs(dump_lang))
    )
