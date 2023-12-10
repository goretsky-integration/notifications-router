from collections.abc import Iterable

from models import UnitAverageCookingTime
from text_utils import humanize_seconds
from views import sort_cooking_time_statistics

__all__ = (
    'render_delivery_cooking_time',
    'render_restaurant_cooking_time',
)


def render_cooking_time(
        units_cooking_time: Iterable[UnitAverageCookingTime],
) -> str:
    lines: list[str] = []

    units_cooking_time = sort_cooking_time_statistics(units_cooking_time)

    for unit_cooking_time in units_cooking_time:
        lines.append(
            f'{unit_cooking_time.unit_name}'
            f' | {humanize_seconds(unit_cooking_time.cooking_time_in_seconds)}'
        )

    return '\n'.join(lines)


def render_restaurant_cooking_time(
        units_cooking_time: Iterable[UnitAverageCookingTime],
) -> str:
    return (
        '<b>Время приготовления в ресторане</b>\n'
        f'{render_cooking_time(units_cooking_time)}'
    )


def render_delivery_cooking_time(
        units_cooking_time: Iterable[UnitAverageCookingTime],
) -> str:
    return (
        '<b>Время приготовления на доставку</b>\n'
        f'{render_cooking_time(units_cooking_time)}'
    )
