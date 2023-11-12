from pydantic import BaseModel

__all__ = ('UnitBonusSystemUsage',)


class UnitBonusSystemUsage(BaseModel):
    unit_name: str
    percentage_of_all_orders: int
