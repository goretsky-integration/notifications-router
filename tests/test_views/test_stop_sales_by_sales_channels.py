from tests.factories import StopSaleBySalesChannelsFactory
from views import (
    render_stop_sale_by_sales_channels,
    compute_stop_sale_duration,
    humanize_stop_sale_duration,
    humanize_sales_channel,
)


def test_render_stop_sale_by_sales_channels():
    stop_sale = StopSaleBySalesChannelsFactory(
        started_at='2021-01-01 00:00:00',
    )

    actual = render_stop_sale_by_sales_channels(stop_sale)

    stop_sale_duration = compute_stop_sale_duration(stop_sale.started_at)
    humanized_stop_sale_duration = humanize_stop_sale_duration(
        duration=stop_sale_duration,
    )
    humanized_stop_sale_started_at = f'{stop_sale.started_at:%H:%M}'

    expected = (
        f'❗️ {stop_sale.unit_name}'
        f' в стопе {humanized_stop_sale_duration}'
        f' (с {humanized_stop_sale_started_at}) ❗️\n'
        f'Тип продажи: {humanize_sales_channel(stop_sale.sales_channel)}\n'
        f'Причина: {stop_sale.reason}'
    )

    assert actual == expected
