import httpx
from pydantic import parse_obj_as

import config
import models

__all__ = (
    'get_chats_to_retranslate',
)


def get_chats_to_retranslate(report_type: str) -> list[models.ChatToRetranslate]:
    url = f'{config.DATABASE_API_URL.rstrip("/")}/reports/retranslate/{report_type}/'
    response = httpx.get(url)
    return parse_obj_as(list[models.ChatToRetranslate], response.json())
