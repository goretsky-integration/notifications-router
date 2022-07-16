import time
from typing import TypedDict, Type

import db
import models
import views
import telegram
from db import consumer
from utils import logger
from units_identify import group_chat_ids_by_unit_id


class Strategy(TypedDict):
    model: Type[models.EventPayload]
    view: Type[views.MessageView]


EVENTS_STRATEGY = {
    'CANCELED_ORDERS': {
        'model': models.OrderByUUID,
        'view': views.CanceledOrder,
    },
}


def run(event: models.Event):
    try:
        strategy: Strategy = EVENTS_STRATEGY[event['type']]
    except KeyError:
        return
    payload: models.EventPayload = strategy['model'].parse_obj(event['payload'])
    view = strategy['view'](payload)
    reports = db.get_reports_by_report_type(event['type'])
    unit_id_to_chat_ids = group_chat_ids_by_unit_id(reports)
    chat_ids = unit_id_to_chat_ids[event['unit_id']]
    for chat_id in chat_ids:
        is_message_sent = telegram.send_message(chat_id, view)
        if is_message_sent:
            logger.debug(f'Message has been sent')
        else:
            logger.warning(f'Message has not been sent')
        time.sleep(0.3)


def main():
    consumer.start_consuming(run)


if __name__ == '__main__':
    main()
