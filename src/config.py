import pathlib
import tomllib
from dataclasses import dataclass

__all__ = (
    'load_config_from_file',
    'Config',
)


@dataclass(frozen=True, slots=True)
class Config:
    telegram_bot_token: str
    redis_url: str


def load_config_from_file(file_path: pathlib.Path) -> Config:
    config_text = file_path.read_text(encoding='utf-8')
    config = tomllib.loads(config_text)
    return Config(
        telegram_bot_token=config['telegram']['bot_token'],
        redis_url=config['redis']['url'],
    )
