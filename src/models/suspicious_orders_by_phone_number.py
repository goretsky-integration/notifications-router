from datetime import datetime

from pydantic import BaseModel

__all__ = ('UnitSuspiciousOrdersByPhoneNumber', 'SuspiciousOrder')


class SuspiciousOrder(BaseModel):
    number: str
    created_at: datetime


class UnitSuspiciousOrdersByPhoneNumber(BaseModel):
    unit_name: str
    phone_number: str
    orders: list[SuspiciousOrder]
