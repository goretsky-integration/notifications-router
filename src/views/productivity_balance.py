from collections.abc import Iterable

from models import UnitProductivityBalanceStatistics
from text_utils import intgaps, humanize_seconds
from views import sort_productivity_balance

__all__ = ('render_productivity_balance',)


def render_productivity_balance(
        units_productivity_balance: Iterable[UnitProductivityBalanceStatistics],
) -> str:
    lines = ['<b>Баланс эффективности</b>']

    units_productivity_balance = sort_productivity_balance(
        units_productivity_balance,
    )

    for unit_productivity_balance in units_productivity_balance:
        lines.append(
            f'{unit_productivity_balance.unit_name}'
            f' | {intgaps(unit_productivity_balance.sales_per_labor_hour)}'
            f' | {unit_productivity_balance.orders_per_labor_hour}'
            f' | {humanize_seconds(unit_productivity_balance.stop_sale_duration_in_seconds)}'
        )

    return '\n'.join(lines)
