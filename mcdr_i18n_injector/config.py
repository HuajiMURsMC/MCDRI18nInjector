from typing import Optional

from mcdreforged.api.utils.serializer import Serializable


class Config(Serializable):
    i18n_files_dir: str = "./i18n"
    language: Optional[str] = None
