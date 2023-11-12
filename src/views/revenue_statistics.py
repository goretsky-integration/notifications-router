from models import UnitsRevenueStatistics
from text_utils import intgaps

__all__ = ('render_revenue_statistics',)


def render_revenue_statistics(
        revenue_statistics: UnitsRevenueStatistics) -> str:
    lines = ['<b>Выручка за сегодня</b>']

    for unit_statistics in revenue_statistics.units_statistics:
        lines.append(
            f'{unit_statistics.unit_name}'
            f' | {intgaps(unit_statistics.revenue_today)}'
            f' | {unit_statistics.compared_to_week_before_in_percents:+}%'
        )

    total_statistics = revenue_statistics.total_statistics
    lines.append(
        f'<b>Итого: {intgaps(total_statistics.revenue_today)}'
        f' | {total_statistics.compared_to_week_before_in_percents:+}%</b>'
    )
    return '\n'.join(lines)
