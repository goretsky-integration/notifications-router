from tests.factories import (
    UnitSuspiciousOrdersByPhoneNumberFactory,
    SuspiciousOrderFactory,
)
from views import render_suspicious_orders_by_phone_number


def test_render_suspicious_orders_by_phone_number() -> None:
    unit_suspicious_orders = UnitSuspiciousOrdersByPhoneNumberFactory(
        orders=[
            SuspiciousOrderFactory(),
        ],
    )

    actual = render_suspicious_orders_by_phone_number(unit_suspicious_orders)
    expected = (
        '<b>❗️ ПОДОЗРИТЕЛЬНО 🤨 ❗️️\n'
        f'{unit_suspicious_orders.unit_name}</b>\n'
        f'Номер: {unit_suspicious_orders.phone_number}\n'
        f'{unit_suspicious_orders.orders[0].created_at:%H:%M}'
        f' - <b>заказ №{unit_suspicious_orders.orders[0].number}</b>'
    )

    assert actual == expected
