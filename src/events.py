import logging
from typing import TypedDict, NoReturn

from pydantic import BaseModel, ValidationError

import models
import views
from message_queue import MessageQueueConsumer
from models import EventType, Event
from telegram import TelegramSender
from text_utils import get_text_by_chunks
from views import RenderFunction

__all__ = (
    'handle_event',
    'EVENT_STRATEGIES',
    'Strategy',
    'start_events_handling',
)

logger = logging.getLogger(__name__)


def handle_event(event: dict, telegram_sender: TelegramSender) -> None:
    try:
        event = Event.model_validate(event)
    except ValidationError:
        logger.exception('Event validation error')
        return

    try:
        strategy = EVENT_STRATEGIES[event.type]
    except KeyError:
        logger.error(f'Unknown event type: {event.type}')
        return

    render = strategy['render']
    model_type = strategy['model']

    try:
        payload = model_type.model_validate(event.payload)
    except ValidationError:
        logger.exception('Payload validation error')
        return

    text = render(payload)

    for text_chunk in get_text_by_chunks(text):
        telegram_sender.send_messages(
            text=text_chunk,
            chat_ids=event.chat_ids,
        )


class Strategy(TypedDict):
    model: type[BaseModel]
    render: RenderFunction


EVENT_STRATEGIES: dict[EventType, Strategy] = {
    EventType.CANCELED_ORDERS: {
        'model': models.UnitCanceledOrders,
        'render': views.render_canceled_orders,
    },
    EventType.INGREDIENT_STOCKS_BALANCE: {
        'model': models.UnitIngredientStocksBalance,
        'render': views.render_ingredient_stocks_balance,
    },
    EventType.LOSSES_AND_EXCESSES: {
        'model': models.UnitLossesAndExcesses,
        'render': views.render_losses_and_excesses,
    },
    EventType.REVENUE_STATISTICS: {
        'model': models.UnitsRevenueStatistics,
        'render': views.render_revenue_statistics,
    },
    EventType.STOP_SALES_BY_INGREDIENTS: {
        'model': models.UnitStopSalesByIngredients,
        'render': views.render_stop_sale_by_ingredients,
    },
    EventType.STOP_SALES_BY_SALES_CHANNELS: {
        'model': models.StopSaleBySalesChannels,
        'render': views.render_stop_sale_by_sales_channels,
    },
    EventType.SUSPICIOUS_ORDERS_BY_PHONE_NUMBER: {
        'model': models.UnitSuspiciousOrdersByPhoneNumber,
        'render': views.render_suspicious_orders_by_phone_number,
    },
    EventType.UNIT_STOP_SALES_BY_INGREDIENTS: {
        'model': models.UnitStopSalesByIngredients,
        'render': views.render_unit_stop_sales_by_ingredients,
    },
    EventType.UNIT_STOP_SALES_BY_SECTORS: {
        'model': models.UnitStopSalesBySectors,
        'render': views.render_unit_stop_sale_by_sectors,
    },
    EventType.WRITE_OFFS: {
        'model': models.WriteOff,
        'render': views.render_write_off,
    }
}


def start_events_handling(
        *,
        message_queue_consumer: MessageQueueConsumer,
        telegram_sender: TelegramSender,
) -> NoReturn:
    consumer_name = 'reports-sender'  # any name
    for event in message_queue_consumer.start_consuming(consumer_name):
        handle_event(
            event=event,
            telegram_sender=telegram_sender,
        )
