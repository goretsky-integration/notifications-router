from typing import TypedDict, Type

import config
import db
import models
import telegram
import views
from db import consumer
from units_identify import group_chat_ids_by_unit_id
from utils import logger


class Strategy(TypedDict):
    model: Type[models.EventPayload]
    view: Type[views.MessageView]


EVENTS_STRATEGY = {
    'CANCELED_ORDERS': {
        'model': models.OrderByUUID,
        'view': views.CanceledOrder,
    },
    'CHEATED_PHONE_NUMBERS': {
        'model': models.CheatedOrders,
        'view': views.CheatedOrders,
    },
    'INGREDIENTS_STOP_SALES': {
        'model': models.StopSaleByIngredients,
        'view': views.StopSaleByIngredients,
    },
    'STREET_STOP_SALES': {
        'model': models.StopSaleByStreets,
        'view': views.StopSaleByStreets,
    },
    'SECTOR_STOP_SALES': {
        'model': models.StopSaleBySectors,
        'view': views.StopSaleBySectors,
    },
    'PIZZERIA_STOP_SALES': {
        'model': models.StopSaleByChannels,
        'view': views.StopSaleByChannels,
    },
    'STOPS_AND_RESUMES': {
        'model': models.StopsAndResumes,
        'view': views.StopsAndResumes,
    },
}


def run(event: models.Event):
    bot = telegram.TelegramSender(config.TELEGRAM_BOT_TOKEN)
    try:
        strategy: Strategy = EVENTS_STRATEGY[event['type']]
    except KeyError as error:
        logger.warning(f'Event type {str(error)} has not recognized')
        return
    payload: models.EventPayload = strategy['model'].parse_obj(event['payload'])
    view = strategy['view'](payload)
    reports = db.get_reports_by_report_type(event['type'])
    unit_id_to_chat_ids = group_chat_ids_by_unit_id(reports)
    chat_ids = unit_id_to_chat_ids[event['unit_id']]
    telegram.send_messages(bot, view.as_text(), chat_ids)


def main():
    consumer.start_consuming(run)


if __name__ == '__main__':
    main()
