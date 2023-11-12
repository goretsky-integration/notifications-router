from collections.abc import Iterable

from models import UnitHeatedShelfTime
from text_utils import humanize_seconds
from views import sort_heated_shelf_time

__all__ = ('render_heated_shelf_time',)


def render_heated_shelf_time(
        units_heated_shelf_time: Iterable[UnitHeatedShelfTime],
) -> str:
    lines = ['<b>Время ожидания на полке / 1в1</b>']

    units_heated_shelf_time = sort_heated_shelf_time(units_heated_shelf_time)

    for unit_heated_shelf_time in units_heated_shelf_time:
        lines.append(
            f'{unit_heated_shelf_time.unit_name}'
            f' | {humanize_seconds(unit_heated_shelf_time.average_heated_shelf_time_in_seconds)}'
            f' | {unit_heated_shelf_time.trips_with_one_order_percentage:g}%'
        )

    return '\n'.join(lines)
