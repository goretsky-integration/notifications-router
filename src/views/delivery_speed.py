from collections.abc import Iterable

from models import UnitAverageDeliverySpeedStatistics
from text_utils import abbreviate_unit_name, humanize_seconds
from views import sort_delivery_speed

__all__ = ('render_delivery_speed',)


def render_delivery_speed(
        units_delivery_speed: Iterable[UnitAverageDeliverySpeedStatistics],
) -> str:
    lines = [
        '<b>Общая скорость доставки - Время приготовления'
        ' - Время на полке - Поездка курьера</b>'
    ]

    units_delivery_speed = sort_delivery_speed(units_delivery_speed)

    for unit_delivery_speed in units_delivery_speed:
        lines.append(
            f'{abbreviate_unit_name(unit_delivery_speed.unit_name)}'
            f' | {humanize_seconds(unit_delivery_speed.delivery_order_fulfillment_time_in_seconds)}'
            f' | {humanize_seconds(unit_delivery_speed.cooking_time_in_seconds)}'
            f' | {humanize_seconds(unit_delivery_speed.heated_shelf_time_in_seconds)}'
            f' | {humanize_seconds(unit_delivery_speed.order_trip_time_in_seconds)}'
        )

    return '\n'.join(lines)
