from typing import Iterable

import httpx

from loguru import logger

__all__ = ('TelegramSender',)


class TelegramSender:
    __slots__ = ('_send_message_url', '_token')

    def __init__(self, token: str):
        self._token = token
        self._send_message_url = f'https://api.telegram.org/bot{self._token}/sendMessage'

    def send_message(self, chat_id: int, text: str) -> bool:
        """Send message to telegram.

        Args:
            chat_id: chat id to send (telegram id or username).
            text: message to send.

        Returns:
            True if ok.
        """
        response = httpx.post(
            url=self._send_message_url,
            json={
                'text': text,
                'chat_id': chat_id,
                'parse_mode': 'html',
            }
        )
        return response.json()['ok']

    def send_messages(self, text: str, chat_ids: Iterable[int]):
        for chat_id in chat_ids:
            is_message_sent = self.send_message(chat_id, text)
            if is_message_sent:
                logger.debug(f'Message has been sent to {chat_id}')
            else:
                logger.warning(f'Message has not been sent to {chat_id}')
