from datetime import datetime

from pydantic import BaseModel

__all__ = ('UnitStopSalesByIngredients',)


class StopSaleByIngredient(BaseModel):
    started_at: datetime
    reason: str
    ingredient_name: str


class UnitStopSalesByIngredients(BaseModel):
    unit_name: str
    stops: list[StopSaleByIngredient]
