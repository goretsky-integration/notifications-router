from collections import defaultdict
from collections.abc import Callable, Iterable
from datetime import timedelta, datetime
from typing import Protocol, TypeVar

import humanize

from models import SalesChannel, CanceledOrder

__all__ = (
    'RenderFunction',
    'render_stop_sale_header',
    'humanize_sales_channel',
    'group_by_sales_channel',
    'humanize_stop_sale_duration',
    'sort_canceled_orders',
    'compute_total_price',
    'group_by_reason',
    'sort_by_started_at',
    'compute_stop_sale_duration',
)

from text_utils import abbreviate_time_units

RenderFunction = Callable[[...], str]

humanize.i18n.activate('ru_RU')

DAY_IN_SECONDS = 86400
HOUR_IN_SECONDS = 3600


class HasUnitNameAndStartedAt(Protocol):
    unit_name: str
    started_at: datetime


class HasSalesChannel(Protocol):
    sales_channel: SalesChannel


class HasPrice(Protocol):
    price: int | float


class HasReason(Protocol):
    reason: str


class HasStartedAt(Protocol):
    started_at: datetime


HasSalesChannelT = TypeVar('HasSalesChannelT', bound=HasSalesChannel)
HasPriceT = TypeVar('HasPriceT', bound=HasPrice)
HasReasonT = TypeVar('HasReasonT', bound=HasReason)
HasStartedAtT = TypeVar('HasStartedAtT', bound=HasStartedAt)


def is_urgent(duration: timedelta) -> bool:
    return duration.total_seconds() >= 1800


def compute_stop_sale_duration(started_at: datetime) -> timedelta:
    return datetime.utcnow() + timedelta(hours=3) - started_at


def render_stop_sale_header(stop_sale: HasUnitNameAndStartedAt):
    stop_sale_duration = compute_stop_sale_duration(stop_sale.started_at)
    humanized_stop_sale_duration = humanize_stop_sale_duration(
        duration=stop_sale_duration,
    )
    humanized_stop_sale_started_at = f'{stop_sale.started_at:%H:%M}'

    header = (
        f'{stop_sale.unit_name}'
        f' в стопе {humanized_stop_sale_duration}'
        f' (с {humanized_stop_sale_started_at})')

    if is_urgent(stop_sale_duration):
        header = '❗️ ' + header + ' ❗️'

    return header


def humanize_sales_channel(sales_channel: SalesChannel) -> str:
    channel_name_map = {
        SalesChannel.DINE_IN: 'Ресторан',
        SalesChannel.TAKEAWAY: 'Самовывоз',
        SalesChannel.DELIVERY: 'Доставка',
    }
    return channel_name_map[sales_channel]


def group_by_sales_channel(
        items: Iterable[HasSalesChannelT],
) -> dict[SalesChannel, list[HasSalesChannelT]]:
    sales_channel_to_items = defaultdict(list)
    for item in items:
        sales_channel_to_items[item.sales_channel].append(item)
    return dict(sales_channel_to_items)


def sort_canceled_orders(
        canceled_orders: Iterable[CanceledOrder],
) -> list[CanceledOrder]:
    return sorted(
        canceled_orders,
        key=lambda canceled_order: (
            canceled_order.sold_at,
            canceled_order.canceled_at,
        )
    )


def compute_total_price(items: Iterable[HasPriceT]) -> int | float:
    return sum(item.price for item in items)


def group_by_reason(items: Iterable[HasReasonT]) -> dict[str, list[HasReasonT]]:
    reason_to_items: dict[str, list[HasReasonT]] = defaultdict(list)
    for item in items:
        reason_to_items[item.reason].append(item)
    return reason_to_items


def sort_by_started_at(items: Iterable[HasStartedAtT]) -> list[HasStartedAtT]:
    return sorted(items, key=lambda item: item.started_at, reverse=True)


def humanize_stop_sale_duration(duration: timedelta) -> str:
    stop_duration_in_seconds = duration.total_seconds()

    if stop_duration_in_seconds >= DAY_IN_SECONDS:
        kwargs = {
            'format': '%0.0f',
            'minimum_unit': 'days',
            'suppress': ['months'],
        }
    elif stop_duration_in_seconds >= HOUR_IN_SECONDS:
        kwargs = {'format': '%0.0f', 'minimum_unit': 'hours'}
    else:
        kwargs = {'format': '%0.0f', 'minimum_unit': 'minutes'}

    return abbreviate_time_units(
        humanize.precisedelta(duration, **kwargs)
    )
