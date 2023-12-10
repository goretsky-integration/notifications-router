from datetime import datetime

from pydantic import BaseModel

from enums import SalesChannel

__all__ = ('StopSaleBySalesChannels',)


class StopSaleBySalesChannels(BaseModel):
    unit_name: str
    started_at: datetime
    reason: str
    sales_channel: SalesChannel
