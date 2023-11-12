from enum import Enum

from pydantic import BaseModel

__all__ = ('WriteOff', 'WriteOffType')


class WriteOffType(Enum):
    EXPIRE_AT_15_MINUTES = 'EXPIRE_AT_15_MINUTES'
    EXPIRE_AT_10_MINUTES = 'EXPIRE_AT_10_MINUTES'
    EXPIRE_AT_5_MINUTES = 'EXPIRE_AT_5_MINUTES'
    ALREADY_EXPIRED = 'ALREADY_EXPIRED'


class WriteOff(BaseModel):
    unit_name: str
    type: WriteOffType
