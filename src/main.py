import pathlib

from pika import URLParameters
from loguru import logger

from config import load_config
import consumer
from db_api import DatabaseAPI
from events import EventHandler
from telegram import TelegramSender


def main():
    config_file_path = pathlib.Path(__file__).parent.parent / 'config.ini'
    logfile_path = pathlib.Path(__file__).parent.parent / 'logs.log'
    config = load_config(config_file_path)

    loglevel = 'DEBUG' if config.debug else 'INFO'
    logger.add(logfile_path, level=loglevel)

    database_api = DatabaseAPI(config.database_api_url)

    telegram_sender = TelegramSender(config.telegram_bot_token)
    event_handler = EventHandler(telegram_sender, database_api)

    rabbitmq_connection_parameters = URLParameters(config.rabbitmq_url)
    with consumer.closing_rabbitmq_connection(rabbitmq_connection_parameters) as rabbitmq_connection:
        with consumer.closing_rabbitmq_channel(rabbitmq_connection) as rabbitmq_channel:
            consumer.start_consuming(rabbitmq_channel, on_event=event_handler)


if __name__ == '__main__':
    main()
