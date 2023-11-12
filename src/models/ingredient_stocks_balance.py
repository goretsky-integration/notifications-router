from pydantic import BaseModel

__all__ = ('UnitIngredientStocksBalance',)


class IngredientStocksBalance(BaseModel):
    ingredient_name: str
    stocks_unit: str
    stocks_count: float
    enough_for_days: int


class UnitIngredientStocksBalance(BaseModel):
    unit_name: str
    ingredients: list[IngredientStocksBalance]
