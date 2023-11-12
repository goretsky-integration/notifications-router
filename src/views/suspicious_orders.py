from models import UnitSuspiciousOrdersByPhoneNumber

__all__ = ('render_suspicious_orders_by_phone_number',)


def render_suspicious_orders_by_phone_number(
        unit_suspicious_orders: UnitSuspiciousOrdersByPhoneNumber,
) -> str:
    lines = [
        '<b>❗️ ПОДОЗРИТЕЛЬНО 🤨 ❗️️',
        f'{unit_suspicious_orders.unit_name}</b>',
        f'Номер: {unit_suspicious_orders.phone_number}',
    ]

    for suspicious_order in unit_suspicious_orders.orders:
        lines.append(
            f'{suspicious_order.created_at:%H:%M} - '
            f'<b>заказ №{suspicious_order.number}</b>'
        )

    return '\n'.join(lines)
