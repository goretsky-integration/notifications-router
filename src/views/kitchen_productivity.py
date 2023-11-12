from collections.abc import Iterable

from models import UnitKitchenProductivity
from text_utils import intgaps
from views import sort_kitchen_productivity

__all__ = ('render_kitchen_productivity',)


def render_kitchen_productivity(
        units_kitchen_productivity: Iterable[UnitKitchenProductivity],
) -> str:
    lines = ['<b>Выручка на чел. в час</b>']

    units_kitchen_productivity = sort_kitchen_productivity(
        units_kitchen_productivity,
    )

    for unit_kitchen_productivity in units_kitchen_productivity:
        lines.append(
            f'{unit_kitchen_productivity.unit_name}'
            f' | {intgaps(unit_kitchen_productivity.sales_per_labor_hour_today)}'
            f' | {unit_kitchen_productivity.compared_to_week_before_in_percents:+}%'
        )

    return '\n'.join(lines)
