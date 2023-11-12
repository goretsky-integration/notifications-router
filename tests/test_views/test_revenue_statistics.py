from tests.factories import (
    UnitsRevenueStatisticsFactory,
    RevenueStatisticsFactory
)
from text_utils import intgaps
from views import render_revenue_statistics


def test_render_revenue_statistics() -> None:
    units_revenue_statistics = UnitsRevenueStatisticsFactory(
        units_statistics=[
            RevenueStatisticsFactory(),
            RevenueStatisticsFactory(),
        ],
        total_revenue=RevenueStatisticsFactory(),
    )

    first_unit_statistics = units_revenue_statistics.units_statistics[0]
    second_unit_statistics = units_revenue_statistics.units_statistics[1]
    total_statistics = units_revenue_statistics.total_statistics

    actual = render_revenue_statistics(units_revenue_statistics)
    expected = (
        '<b>Выручка за сегодня</b>\n'
        f'{first_unit_statistics.unit_name}'
        f' | {intgaps(first_unit_statistics.revenue_today)}'
        f' | {first_unit_statistics.compared_to_week_before_in_percents:+}%\n'
        f'{second_unit_statistics.unit_name}'
        f' | {intgaps(second_unit_statistics.revenue_today)}'
        f' | {second_unit_statistics.compared_to_week_before_in_percents:+}%\n'
        f'<b>Итого:'
        f' {intgaps(total_statistics.revenue_today)}'
        f' | {total_statistics.compared_to_week_before_in_percents:+}%</b>'
    )

    assert actual == expected
