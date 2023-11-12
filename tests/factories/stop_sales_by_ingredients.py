import factory

from models import StopSaleByIngredients

__all__ = ('StopSaleByIngredientsFactory',)


class StopSaleByIngredientsFactory(factory.Factory):

    class Meta:
        model = StopSaleByIngredients

    unit_name = factory.Sequence(lambda n: f'Москва-{n}')
    started_at = factory.Faker('date_time')
    reason = factory.Faker('text')
    ingredient_name = factory.Faker('text')
