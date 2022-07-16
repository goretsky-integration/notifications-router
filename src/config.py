import pathlib

from environs import Env

__all__ = (
    'ROOT_PATH',
    'LOGS_FILE_PATH',
    'TELEGRAM_BOT_TOKEN',
    'DEBUG',
    'RABBITMQ_URL',
    'MONGODB_URL',
)

env = Env()
env.read_env()

ROOT_PATH = pathlib.Path(__file__).parent.parent
LOGS_FILE_PATH = ROOT_PATH / 'logs.log'

TELEGRAM_BOT_TOKEN: str = env.str('TELEGRAM_BOT_TOKEN')
MONGODB_URL: str = env.str('MONGODB_URL')
DEBUG: bool = env.bool('DEBUG')
RABBITMQ_URL: str = env.str('RABBITMQ_URL')
