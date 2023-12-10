from collections.abc import Iterable

from enums import SalesChannel
from models import UnitCanceledOrders, CanceledOrder
from text_utils import intgaps
from views.common import (
    humanize_sales_channel,
    group_by_sales_channel,
    sort_canceled_orders,
    compute_total_price,
)

__all__ = ('render_canceled_orders',)


def render_canceled_orders_grouped_by_sales_channel(
        sales_channel: SalesChannel,
        canceled_orders: Iterable[CanceledOrder],
) -> str:
    lines = [f'<b>Тип заказа: {humanize_sales_channel(sales_channel)}:</b>']

    for canceled_order in canceled_orders:
        order_url = (
            'https://shiftmanager.dodopizza.ru/Managment/ShiftManagment/Order?'
            f'orderUUId={canceled_order.id.hex}'
        )
        lines.append(
            f'Заказ <a href="{order_url}">'
            f' №{canceled_order.number}</a>'
            f' {canceled_order.price}₽'
        )
    return '\n'.join(lines)


def render_canceled_orders(unit_canceled_orders: UnitCanceledOrders) -> str:
    lines = [f'<b>Отчёт по отменам {unit_canceled_orders.unit_name}:</b>']

    sorted_canceled_orders = sort_canceled_orders(unit_canceled_orders.orders)
    grouped_by_sales_channels = group_by_sales_channel(
        items=sorted_canceled_orders,
    )

    for sales_channel, canceled_orders in grouped_by_sales_channels.items():
        lines.append(
            render_canceled_orders_grouped_by_sales_channel(
                sales_channel=sales_channel,
                canceled_orders=canceled_orders,
            )
        )

    total_price = compute_total_price(sorted_canceled_orders)
    lines.append(f'\n<b>Итого: {intgaps(total_price)}₽</b>')

    return '\n'.join(lines)
