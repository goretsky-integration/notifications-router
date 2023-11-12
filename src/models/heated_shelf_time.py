from pydantic import BaseModel

__all__ = ('UnitHeatedShelfTime',)


class UnitHeatedShelfTime(BaseModel):
    unit_name: str
    average_heated_shelf_time_in_seconds: int
    trips_with_one_order_percentage: int
