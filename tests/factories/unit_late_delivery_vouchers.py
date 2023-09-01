import factory

from factories.common import generate_order_number
from factories.common import generate_unit_name
from models import UnitLateDeliveryVouchers

__all__ = ('UnitLateDeliveryVouchersFactory',)


class UnitLateDeliveryVouchersFactory(factory.Factory):

    class Meta:
        model = UnitLateDeliveryVouchers

    unit_name = factory.LazyFunction(generate_unit_name)
    order_numbers = factory.LazyFunction(
        lambda: [generate_order_number() for _ in range(5)]
    )
