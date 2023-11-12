from pydantic import BaseModel

__all__ = ('UnitProductivityBalanceStatistics',)


class UnitProductivityBalanceStatistics(BaseModel):
    unit_name: str
    sales_per_labor_hour: int
    orders_per_labor_hour: float
    stop_sale_duration_in_seconds: int
