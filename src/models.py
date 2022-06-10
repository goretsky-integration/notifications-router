from datetime import datetime

from pydantic import BaseModel


class BonusSystemFraud(BaseModel):
    department: str
    phone_number: str
    datetimes: list[datetime]

    @property
    def amount(self) -> int:
        return len(self.datetimes)


AllModels = BonusSystemFraud
