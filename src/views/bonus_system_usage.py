from collections.abc import Iterable

from models import UnitBonusSystemUsage
from views import sort_bonus_system_usage_statistics


def render_bonus_system_usage(
        units_bonus_system_usage: Iterable[UnitBonusSystemUsage],
) -> str:
    lines = ['<b>Бонусная система</b>']

    units_bonus_system_usage = sort_bonus_system_usage_statistics(
        units_bonus_system_usage,
    )

    for unit_bonus_system_usage in units_bonus_system_usage:
        lines.append(
            f'{unit_bonus_system_usage.unit_name}'
            f' | {unit_bonus_system_usage.orders_with_phone_numbers_percent}%'
            f' из 100'
        )

    return '\n'.join(lines)
