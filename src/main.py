import logging
import pathlib

from redis import Redis

from config import load_config_from_file
from events import start_events_handling
from message_queue import MessageQueueConsumer
from telegram import TelegramSender, is_token_valid

logger = logging.getLogger(__name__)


def main():
    config_file_path = pathlib.Path(__file__).parent.parent / 'config.toml'
    config = load_config_from_file(config_file_path)

    telegram_sender = TelegramSender(config.telegram_bot_token)

    if not is_token_valid(telegram_sender):
        logger.critical('Telegram bot token is invalid')
        exit(1)

    # noinspection PyNoneFunctionAssignment, PyTypeChecker
    redis_client: Redis = Redis.from_url(config.redis_url)

    with MessageQueueConsumer(
            redis_client=redis_client,
            stream_name='reports-sender',
            consumer_group='reports-sender-group',
    ) as message_queue_consumer:

        start_events_handling(
            message_queue_consumer=message_queue_consumer,
            telegram_sender=telegram_sender,
        )


if __name__ == '__main__':
    main()
