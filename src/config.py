import pathlib

from environs import Env

__all__ = (
    'ROOT_PATH',
    'LOGS_FILE_PATH',
    'TELEGRAM_BOT_TOKEN',
    'IS_DEBUG',
    'RABBITMQ_HOST',
    'RABBITMQ_PORT',
    'RABBITMQ_EXCHANGE',
)

env = Env()
env.read_env()

ROOT_PATH = pathlib.Path(__file__).parent.parent
LOGS_FILE_PATH = ROOT_PATH / 'logs.log'

TELEGRAM_BOT_TOKEN: str = env.str('TELEGRAM_BOT_TOKEN')
IS_DEBUG: bool = env.bool('IS_DEBUG')
RABBITMQ_HOST: str = env.str('RABBITMQ_HOST')
RABBITMQ_PORT: int = env.int('RABBITMQ_PORT')
RABBITMQ_EXCHANGE: str = env.str('RABBITMQ_EXCHANGE')
