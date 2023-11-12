import factory

from models import UnitLossesAndExcesses, LossesAndExcesses

__all__ = (
    'LossesAndExcessesFactory',
    'UnitLossesAndExcessesFactory',
)


class LossesAndExcessesFactory(factory.Factory):

    class Meta:
        model = LossesAndExcesses

    percent_of_revenue = factory.Faker('pyfloat', positive=True)
    amount = factory.Faker('pyfloat', positive=True)


class UnitLossesAndExcessesFactory(factory.Factory):

    class Meta:
        model = UnitLossesAndExcesses

    unit_name = factory.Sequence(lambda n: f'Москва-{n}')
    total_loss = factory.SubFactory(LossesAndExcessesFactory)
    unaccounted_losses = factory.SubFactory(LossesAndExcessesFactory)
    write_offs = factory.SubFactory(LossesAndExcessesFactory)
    total_excess = factory.SubFactory(LossesAndExcessesFactory)
