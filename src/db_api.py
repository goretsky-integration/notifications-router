import httpx
from pydantic import parse_obj_as

import models

__all__ = ('DatabaseAPI',)


class DatabaseAPI:
    __slots__ = ('__base_url',)

    def __init__(self, base_url: str):
        self.__base_url = base_url

    def get_chats_to_retranslate(self, report_type: str) -> list[models.ChatToRetranslate]:
        url = f'{self.__base_url.rstrip("/")}/reports/retranslate/{report_type}/'
        response = httpx.get(url)
        return parse_obj_as(list[models.ChatToRetranslate], response.json())
