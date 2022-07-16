from datetime import datetime, timedelta

from loguru import logger

import config

__all__ = (
    'logger',
)

log_level = 'DEBUG' if config.DEBUG else 'INFO'
logger.add(config.LOGS_FILE_PATH, level=log_level, retention='3 days')


def get_moscow_datetime() -> datetime:
    return datetime.utcnow() - timedelta(hours=3)
