from pydantic import BaseModel

__all__ = ('UnitDeliveryProductivity',)


class UnitDeliveryProductivity(BaseModel):
    unit_name: str
    orders_per_courier_labour_hour_today: float
    compared_to_week_before_in_percents: int
