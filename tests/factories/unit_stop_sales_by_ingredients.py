import factory

from models import UnitStopSalesByIngredients, StopSaleByIngredient

__all__ = ('UnitStopSalesByIngredientsFactory', 'StopSaleByIngredientFactory')


class StopSaleByIngredientFactory(factory.Factory):
    class Meta:
        model = StopSaleByIngredient

    started_at = factory.Faker('date_time')
    reason = factory.Faker('sentence')
    ingredient_name = factory.Faker('word')


class UnitStopSalesByIngredientsFactory(factory.Factory):
    class Meta:
        model = UnitStopSalesByIngredients

    unit_name = factory.Sequence(lambda n: f'Москва-{n}')
    stops = factory.List([factory.SubFactory(StopSaleByIngredientFactory)])
