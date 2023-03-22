import httpx

__all__ = ('DatabaseAPI',)


class DatabaseAPI:
    __slots__ = ('__http_client',)

    def __init__(self, http_client: httpx.Client):
        self.__http_client = http_client

    def get_telegram_chats(
            self,
            *,
            unit_id: int,
            report_type: str,
    ) -> list[int]:
        request_query_params = {'unit_id': unit_id, 'report_type': report_type}
        url = '/reports/telegram-chats/'
        response = self.__http_client.get(url, params=request_query_params)
        return response.json()
