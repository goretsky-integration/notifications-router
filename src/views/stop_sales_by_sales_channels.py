from models import StopSaleBySalesChannels
from views.common import render_stop_sale_header, humanize_sales_channel

__all__ = ('render_stop_sale_by_sales_channels',)


def render_stop_sale_by_sales_channels(
        stop_sale: StopSaleBySalesChannels,
) -> str:
    header = render_stop_sale_header(stop_sale)
    channel_name = humanize_sales_channel(stop_sale.sales_channel)
    return (
        f'{header}\n'
        f'Тип продажи: {channel_name}\n'
        f'Причина: {stop_sale.reason}'
    )
