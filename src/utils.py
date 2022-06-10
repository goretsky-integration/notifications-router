from typing import Iterable, Type

from loguru import logger
from pydantic import ValidationError

import config

__all__ = (
    'logger',
)

import exceptions

import models

log_level = 'DEBUG' if config.IS_DEBUG else 'INFO'
logger.add(config.LOGS_FILE_PATH, level=log_level, retention='3 days')


def validate_payload(model: Type[models.AllModels] | models.AllModels, payload: dict):
    try:
        model.parse_obj(payload)
    except ValidationError:
        raise exceptions.PayloadValidationError
