import factory.fuzzy

from models import StopSaleBySalesChannels, SalesChannel

__all__ = ('StopSaleBySalesChannelsFactory',)


class StopSaleBySalesChannelsFactory(factory.Factory):

    class Meta:
        model = StopSaleBySalesChannels

    unit_name = factory.Sequence(lambda n: f'Москва-{n}')
    started_at = factory.Faker('date_time')
    reason = factory.Faker('text')
    sales_channel = factory.fuzzy.FuzzyChoice(SalesChannel)
