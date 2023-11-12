import logging
import time
from collections.abc import Iterable

import requests

import exceptions

__all__ = ('TelegramSender', 'is_token_valid')

logger = logging.getLogger(__name__)


class TelegramSender:
    __slots__ = ('_token',)

    def __init__(self, token: str):
        self._token = token

    def get_me(self) -> dict:
        """Get information about bot.

        Returns:
            dict with information about bot.
        """
        url = f'https://api.telegram.org/bot{self._token}/getMe'
        response = requests.get(url)
        return response.json()

    def send_message(self, chat_id: int, text: str) -> None:

        """Send message to telegram.

        Args:
            chat_id: chat id to send (telegram id or username).
            text: message to send.

        Raises:
            TelegramAPIError on error with description.
        """

        url = f'https://api.telegram.org/bot{self._token}/sendMessage'
        for _ in range(3):
            try:
                response = requests.post(
                    url=url,
                    json={
                        'text': text,
                        'chat_id': chat_id,
                        'parse_mode': 'html',
                    }
                )
            except requests.ConnectionError:
                logger.error('HTTP Connect Error. Trying again')
            else:
                break
        else:
            raise exceptions.TelegramAPIError(
                'Could not connect to Telegram API'
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
                logger.error(
                    f'Could not send message to {chat_id}.'
                    f' Error {error.error_description}'
                )
            else:
                logger.info(f'Message sent to {chat_id}')
            finally:
                time.sleep(0.5)


def is_token_valid(telegram_sender: TelegramSender) -> bool:
    """Check bot token.

    Returns:
        True if token is valid, False otherwise.
    """
    response = telegram_sender.get_me()
    return response['ok']
