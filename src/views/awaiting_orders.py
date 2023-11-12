from collections.abc import Iterable

from models import UnitAwaitingOrders
from views import sort_awaiting_orders

__all__ = ('render_awaiting_orders',)


def render_awaiting_orders(
        units_awaiting_orders: Iterable[UnitAwaitingOrders],
) -> str:
    lines = ['<b>Остывают на полке - В очереди (Всего)</b>']

    units_awaiting_orders = sort_awaiting_orders(units_awaiting_orders)

    for unit_awaiting_orders in units_awaiting_orders:
        lines.append(
            f'{unit_awaiting_orders.unit_name}'
            f' | {unit_awaiting_orders.heated_shelf_orders_count}'
            f' - {unit_awaiting_orders.couriers_in_queue_count}'
            f' ({unit_awaiting_orders.couriers_on_shift_count})'
        )

    return '\n'.join(lines)
