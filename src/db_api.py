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
        url = f'/report-types/names/{report_type}/'
        response = self.__http_client.get(url)
        report_type = response.json()

        url = '/report-routes/telegram-chats/'
        request_query_params = {
            'unit_id': unit_id,
            'report_type_id': report_type['id']
        }
        chat_ids = []
        while True:
            response = self.__http_client.get(url, params=request_query_params)
            response_data = response.json()

            chat_ids += response_data['chat_ids']

            if response_data['is_end_of_list_reached']:
                break
        return chat_ids
