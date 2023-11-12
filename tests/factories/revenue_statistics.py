import factory

from models import UnitsRevenueStatistics, RevenueStatistics

__all__ = (
    'RevenueStatisticsFactory',
    'UnitsRevenueStatisticsFactory',
)


class RevenueStatisticsFactory(factory.Factory):

    class Meta:
        model = RevenueStatistics

    unit_name = factory.Sequence(lambda n: f'Москва-{n}')
    revenue_today = factory.Faker('pyint')
    revenue_week_before_to_this_time = factory.Faker('pyint')
    compared_to_week_before_in_percents = factory.Faker('pyint')


class UnitsRevenueStatisticsFactory(factory.Factory):

    class Meta:
        model = UnitsRevenueStatistics

    units_statistics = factory.List([
        factory.SubFactory(RevenueStatisticsFactory),
    ])
    total_statistics = factory.SubFactory(RevenueStatisticsFactory)
