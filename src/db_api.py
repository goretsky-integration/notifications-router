import httpx
from pydantic import parse_obj_as

import models

__all__ = ('DatabaseAPI',)


class DatabaseAPI:
    __slots__ = ('__base_url',)

    def __init__(self, base_url: str):
        self.__base_url = base_url.rstrip('/')

    def get_report_routes(self, report_type: str) -> list[models.ChatToRetranslate]:
        request_query_params = {'report_type': report_type}
        url = f'{self.__base_url}/reports/'
        response = httpx.get(url, params=request_query_params)
        return parse_obj_as(list[models.ChatToRetranslate], response.json())
