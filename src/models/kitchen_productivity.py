from pydantic import BaseModel

__all__ = ('UnitKitchenProductivity',)


class UnitKitchenProductivity(BaseModel):
    unit_name: str
    sales_per_labor_hour_today: int
    compared_to_week_before_in_percents: int
