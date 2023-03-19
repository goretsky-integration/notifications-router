import datetime
import traceback
from typing import Callable, TypedDict, Type

from loguru import logger
from pydantic import ValidationError

import models
import views
from db_api import DatabaseAPI
from telegram import TelegramSender
from text_utils import get_text_by_chunks
from units_identify import group_chat_ids_by_unit_id

__all__ = (
    'EventExpirationFilter',
    'EventHandler',
    'EVENTS_STRATEGY',
    'Strategy',
)


class EventExpirationFilter:
    """
    Sometimes events stuck and aren't sending for a long time,
    so some of them might not have relevance if they aren't delivered at time.
    This filter prevents sending not relevant messages.
    """
    __slots__ = ('__max_lifetime_in_seconds', '__get_current_datetime')

    def __init__(
            self,
            max_lifetime_in_seconds: int | float,
            current_datetime_callback: Callable[[], datetime.datetime] = datetime.datetime.utcnow,
    ):
        self.__max_lifetime_in_seconds = max_lifetime_in_seconds
        self.__get_current_datetime = current_datetime_callback
        self.__validate_initial_arguments()

    def __validate_initial_arguments(self):
        if self.__max_lifetime_in_seconds < 1:
            raise ValueError('Max lifetime must be at least 1 second')

    def is_expired(self, event_created_at: datetime.datetime) -> bool:
        event_lifetime = self.__get_current_datetime() - event_created_at
        return event_lifetime.total_seconds() > self.__max_lifetime_in_seconds


class EventHandler:

    def __init__(
            self,
            telegram_sender: TelegramSender,
            database_api: DatabaseAPI,
            event_expiration_filter: EventExpirationFilter,
    ):
        self.__telegram_sender = telegram_sender
        self.__database_api = database_api
        self.__event_expiration_filter = event_expiration_filter

    def __call__(self, event: models.RawEvent):
        try:
            event: models.EventFromMessageQueue = models.EventFromMessageQueue.parse_obj(event)
        except ValidationError:
            logger.error(f'Could not parse event: {traceback.format_exc()}')
            return

        if self.__event_expiration_filter.is_expired(event.created_at):
            logger.info(f'Event {event} was expired')
            return

        strategy = EVENTS_STRATEGY[event.type]

        event_type = strategy.get('alias', event.type.name)
        payload: models.EventPayload = strategy['model'].parse_obj(event.payload)
        view = strategy['view'](payload)
        report_routes = self.__database_api.get_report_routes(event_type)
        unit_id_to_chat_ids = group_chat_ids_by_unit_id(report_routes)
        chat_ids = unit_id_to_chat_ids[event.unit_id]
        logger.info(f'Sending event {event.type.name} by unit {event.unit_id} to chats {chat_ids}')
        for text_chunk in get_text_by_chunks(view.as_text()):
            self.__telegram_sender.send_messages(text_chunk, chat_ids)


class Strategy(TypedDict):
    model: Type[models.EventPayload]
    view: Type[views.MessageView]
    alias: str


EVENTS_STRATEGY = {
    'CANCELED_ORDERS': {
        'model': models.UnitCanceledOrders,
        'view': views.UnitCanceledOrders,
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
        'model': models.StopSalesByOtherIngredients,
        'view': views.StopSalesByOtherIngredients,
    },
    'STOCKS_BALANCE': {
        'model': models.StocksBalance,
        'view': views.StocksBalance,
        'alias': 'STOPS_AND_RESUMES',
    },
    'WRITE_OFFS': {
        'model': models.WriteOff,
        'view': views.WriteOff,
    },
    'PROMO_CODES_USAGE': {
        'model': models.UnitUsedPromoCodes,
        'view': views.UnitUsedPromoCodes,
    },
    'LATE_DELIVERY_VOUCHERS': {
        'model': models.UnitLateDeliveryVouchers,
        'view': views.UnitLateDeliveryVouchers,
    }
}
