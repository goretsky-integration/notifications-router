from collections.abc import Iterable

from models import (
    UnitLateDeliveryVouchersStatistics as UnitLateDeliveryVouchers,
)
from views import sort_late_delivery_vouchers

__all__ = ('render_late_delivery_vouchers',)


def render_late_delivery_vouchers(
        units_late_delivery_vouchers: Iterable[UnitLateDeliveryVouchers],
):
    lines = ['<b>Сертификаты за опоздание (сегодня) | (неделю назад)</b>']

    units_late_delivery_vouchers = sort_late_delivery_vouchers(
        units_late_delivery_vouchers,
    )

    for unit_late_delivery_vouchers in units_late_delivery_vouchers:
        lines.append(
            f'{unit_late_delivery_vouchers.unit_name}'
            f' | {unit_late_delivery_vouchers.certificates_count_today} шт'
            f' | {unit_late_delivery_vouchers.certificates_count_week_before} шт'
        )

    return '\n'.join(lines)
