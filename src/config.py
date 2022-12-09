import pathlib
from configparser import ConfigParser
from dataclasses import dataclass

__all__ = (
    'ROOT_PATH',
    'LOGS_FILE_PATH',
    'load_config',
    'Config',
)


@dataclass(frozen=True, slots=True)
class Config:
    telegram_bot_token: str
    debug: bool
    rabbitmq_url: str
    database_api_url: str
    event_max_lifetime_in_seconds: int


def load_config(config_file_path: str | pathlib.Path) -> Config:
    config_parser = ConfigParser()
    config_parser.read(config_file_path)

    app_config = config_parser['app']

    return Config(
        telegram_bot_token=app_config.get('telegram_bot_token'),
        debug=app_config.getboolean('debug'),
        rabbitmq_url=app_config.get('rabbitmq_url'),
        database_api_url=app_config.get('database_api_url'),
        event_max_lifetime_in_seconds=app_config.getint('event_max_lifetime_in_seconds'),
    )


ROOT_PATH = pathlib.Path(__file__).parent.parent
LOGS_FILE_PATH = ROOT_PATH / 'logs.log'
