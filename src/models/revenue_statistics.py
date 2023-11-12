from pydantic import BaseModel

__all__ = ('UnitsRevenueStatistics',)


class RevenueStatistics(BaseModel):
    unit_name: str
    revenue_today: int
    revenue_week_before_to_this_time: int
    compared_to_week_before_in_percents: float


class UnitsRevenueStatistics(BaseModel):
    units_statistics: list[RevenueStatistics]
    total_statistics: RevenueStatistics
