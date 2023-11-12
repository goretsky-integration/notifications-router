from collections.abc import Iterable

from models import UnitDeliveryProductivity
from views import sort_delivery_productivity

__all__ = ('render_delivery_productivity',)


def render_delivery_productivity(
        units_delivery_productivity: Iterable[UnitDeliveryProductivity],
) -> str:
    lines = ['<b>Заказов на курьера в час</b>']

    units_delivery_productivity = sort_delivery_productivity(
        units_delivery_productivity,
    )

    for delivery_productivity in units_delivery_productivity:
        lines.append(
            f'{delivery_productivity.unit_name}'
            f' | {delivery_productivity.orders_per_courier_labour_hour_today}'
            f' | {delivery_productivity.compared_to_week_before_in_percents:+}%'
        )

    return '\n'.join(lines)
