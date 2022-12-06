import contextlib
import json
import traceback
from typing import Callable

from pika import ConnectionParameters, URLParameters, BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel

from loguru import logger


__all__ = (
    'closing_rabbitmq_connection',
    'closing_rabbitmq_channel',
)


@contextlib.contextmanager
def closing_rabbitmq_connection(
        connection_parameters: ConnectionParameters | URLParameters,
) -> BlockingConnection:
    with BlockingConnection(connection_parameters) as connection:
        yield connection


@contextlib.contextmanager
def closing_rabbitmq_channel(
        connection: BlockingConnection,
) -> BlockingChannel:
    with connection.channel() as channel:
        channel.queue_declare(queue='telegram-notifications')
        yield channel


def bytes_to_dict(bytes_string: bytes) -> dict:
    return json.loads(bytes_string.decode('utf-8'))


def start_consuming(channel: BlockingChannel, on_event: Callable):
    def wrapper(ch, method, properties, body: bytes):
        logger.debug(f'Received message {method.delivery_tag}')
        try:
            on_event(bytes_to_dict(body))
        except Exception:
            logger.error(traceback.format_exc())
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='telegram-notifications', on_message_callback=wrapper)
    channel.start_consuming()
