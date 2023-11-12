from pydantic import BaseModel

__all__ = ('UnitAverageCookingTime',)


class UnitAverageCookingTime(BaseModel):
    unit_name: str
    cooking_time_in_seconds: int
