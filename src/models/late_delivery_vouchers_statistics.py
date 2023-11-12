from pydantic import BaseModel

__all__ = ('UnitLateDeliveryVouchersStatistics',)


class UnitLateDeliveryVouchersStatistics(BaseModel):
    unit_name: str
    certificates_count_today: int
    certificates_count_week_before: int
