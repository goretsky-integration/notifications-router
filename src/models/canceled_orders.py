from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from enums import SalesChannel

__all__ = ('UnitCanceledOrders', 'CanceledOrder')


class CanceledOrder(BaseModel):
    id: UUID
    sold_at: datetime
    canceled_at: datetime
    number: str
    sales_channel: SalesChannel
    price: float


class UnitCanceledOrders(BaseModel):
    unit_name: str
    orders: list[CanceledOrder]
