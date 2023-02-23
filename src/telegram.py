from typing import Iterable

import httpx
from loguru import logger

import exceptions

__all__ = ('TelegramSender',)


class TelegramSender:
    __slots__ = ('_send_message_url', '_token')

    def __init__(self, token: str):
        self._token = token
        self._send_message_url = f'https://api.telegram.org/bot{self._token}/sendMessage'

    def send_message(self, chat_id: int, text: str) -> None:
        """Send message to telegram.

        Args:
            chat_id: chat id to send (telegram id or username).
            text: message to send.

        Raises:
            TelegramAPIError on error with description.
        """
        response = httpx.post(
            url=self._send_message_url,
            json={
                'text': text,
                'chat_id': chat_id,
                'parse_mode': 'html',
            }
        )
        response_data = response.json()
        if not response_data['ok']:
            error_description = response_data.get('description')
            raise exceptions.TelegramAPIError(error_description)

    def send_messages(self, text: str, chat_ids: Iterable[int]):
        for chat_id in chat_ids:
            try:
                self.send_message(chat_id, text)
            except exceptions.TelegramAPIError as error:
                logger.warning(f'Could not send message to {chat_id}. Error {error.error_description}')
            else:
                logger.info(f'Message sent to {chat_id}')
