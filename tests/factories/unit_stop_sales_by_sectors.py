import factory

from models import StopSaleBySector, UnitStopSalesBySectors

__all__ = ('StopSaleBySectorFactory', 'UnitStopSalesBySectorFactory')


class StopSaleBySectorFactory(factory.Factory):
    class Meta:
        model = StopSaleBySector

    started_at = factory.Faker('date_time')
    sector_name = factory.Faker('address')


class UnitStopSalesBySectorFactory(factory.Factory):
    class Meta:
        model = UnitStopSalesBySectors

    unit_name = factory.Sequence(lambda n: f'Москва-{n}')
    stops = factory.List([factory.SubFactory(StopSaleBySectorFactory)])
