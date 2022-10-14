import atexit
import json
import traceback
from typing import Callable

import pika

import config
from utils import logger

connection = pika.BlockingConnection(pika.URLParameters(config.RABBITMQ_URL))
channel = connection.channel()
channel.queue_declare(queue='telegram-notifications')


def bytes_to_dict(bytes_string: bytes) -> dict:
    return json.loads(bytes_string.decode('utf-8'))


def start_consuming(callback: Callable):
    def wrapper(ch, method, properties, body: bytes):
        logger.debug(f'Received message {method.delivery_tag}')
        try:
            callback(bytes_to_dict(body))
        except Exception:
            logger.error(traceback.format_exc())
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='telegram-notifications', on_message_callback=wrapper)
    channel.start_consuming()


atexit.register(connection.close)
