from datetime import datetime

from pydantic import BaseModel

__all__ = ('UnitStopSalesBySectors',)


class StopSaleBySector(BaseModel):
    started_at: datetime
    sector_name: str


class UnitStopSalesBySectors(BaseModel):
    unit_name: str
    stops: list[StopSaleBySector]
