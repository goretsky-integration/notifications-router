import pathlib

from pika import URLParameters
from loguru import logger

from config import load_config
from db import consumer
from events import EventHandler
from telegram import TelegramSender


def main():
    config_file_path = pathlib.Path(__file__).parent.parent / 'config.ini'
    logfile_path = pathlib.Path(__file__).parent.parent / 'logs.log'
    config = load_config(config_file_path)

    loglevel = 'DEBUG' if config.debug else 'INFO'
    logger.add(logfile_path, level=loglevel)

    telegram_sender = TelegramSender(config.telegram_bot_token)
    event_handler = EventHandler(telegram_sender)

    rabbitmq_connection_parameters = URLParameters(config.rabbitmq_url)
    with consumer.closing_rabbitmq_connection(rabbitmq_connection_parameters) as rabbitmq_connection:
        with consumer.closing_rabbitmq_channel(rabbitmq_connection) as rabbitmq_channel:
            consumer.start_consuming(rabbitmq_channel, on_event=event_handler)


if __name__ == '__main__':
    main()
