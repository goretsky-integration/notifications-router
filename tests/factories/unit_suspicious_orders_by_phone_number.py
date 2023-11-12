import random

import factory

from models import UnitSuspiciousOrdersByPhoneNumber, SuspiciousOrder

__all__ = (
    'UnitSuspiciousOrdersByPhoneNumberFactory',
    'SuspiciousOrderFactory',
)


class SuspiciousOrderFactory(factory.Factory):
    class Meta:
        model = SuspiciousOrder

    number = factory.LazyFunction(
        lambda: f'{random.randint(1, 100)}-{random.randint(1, 5)}',
    )
    created_at = factory.Faker('date_time')


class UnitSuspiciousOrdersByPhoneNumberFactory(factory.Factory):
    class Meta:
        model = UnitSuspiciousOrdersByPhoneNumber

    unit_name = factory.Sequence(lambda n: f'Москва-{n}')
    phone_number = factory.Faker('phone_number')
    orders = factory.List([factory.SubFactory(SuspiciousOrderFactory)])
