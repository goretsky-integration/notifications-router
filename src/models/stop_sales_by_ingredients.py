from datetime import datetime

from pydantic import BaseModel

__all__ = ('StopSaleByIngredients',)


class StopSaleByIngredients(BaseModel):
    unit_name: str
    started_at: datetime
    reason: str
    ingredient_name: str
