import pathlib

import httpx
from pika import URLParameters
from loguru import logger

from config import load_config
from consumer import (
    closing_rabbitmq_connection,
    closing_rabbitmq_channel,
    start_consuming,
)
from db_api import DatabaseAPI
from events import EventHandler, EventExpirationFilter
from telegram import TelegramSender


def main():
    config_file_path = pathlib.Path(__file__).parent.parent / 'config.ini'
    logfile_path = pathlib.Path(__file__).parent.parent / 'logs.log'
    config = load_config(config_file_path)

    loglevel = 'DEBUG' if config.debug else 'INFO'
    logger.add(logfile_path, level=loglevel)

    telegram_sender = TelegramSender(config.telegram_bot_token)
    event_expiration_filter = EventExpirationFilter(
        max_lifetime_in_seconds=config.event_max_lifetime_in_seconds)

    url_parameters = URLParameters(config.rabbitmq_url)

    with (
        httpx.Client(base_url=config.database_api_url) as http_client,
        closing_rabbitmq_connection(url_parameters) as rabbitmq_connection,
        closing_rabbitmq_channel(rabbitmq_connection) as rabbitmq_channel
    ):
        database_api = DatabaseAPI(http_client)
        event_handler = EventHandler(
            telegram_sender,
            database_api,
            event_expiration_filter,
        )
        start_consuming(rabbitmq_channel, on_event=event_handler)


if __name__ == '__main__':
    main()
