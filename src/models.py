import uuid
from datetime import datetime
from enum import Enum
from typing import TypedDict, TypeAlias

from pydantic import BaseModel, PositiveInt


class EventFromMessageQueueType(str, Enum):
    INGREDIENTS_STOP_SALES = 'INGREDIENTS_STOP_SALES'
    STREET_STOP_SALES = 'STREET_STOP_SALES'
    SECTOR_STOP_SALES = 'SECTOR_STOP_SALES'
    PIZZERIA_STOP_SALES = 'PIZZERIA_STOP_SALES'
    STOPS_AND_RESUMES = 'STOPS_AND_RESUMES'
    CANCELED_ORDERS = 'CANCELED_ORDERS'
    CHEATED_PHONE_NUMBERS = 'CHEATED_PHONE_NUMBERS'
    WRITE_OFFS = 'WRITE_OFFS'
    PROMO_CODES_USAGE = 'PROMO_CODES_USAGE'


class EventFromMessageQueue(BaseModel):
    type: EventFromMessageQueueType
    unit_id: PositiveInt
    payload: dict
    created_at: datetime


class ReportRoute(BaseModel):
    chat_id: int
    unit_ids: tuple[int, ...]


class RawEvent(TypedDict):
    type: str
    unit_id: int
    payload: dict
    created_at: str


class CheatedOrder(BaseModel):
    created_at: datetime
    number: str


class CheatedOrders(BaseModel):
    unit_name: str
    phone_number: str
    orders: list[CheatedOrder]


class StopSale(BaseModel):
    unit_name: str
    started_at: datetime


class IngredientStop(BaseModel):
    started_at: datetime
    reason: str
    name: str


class StopSalesByOtherIngredients(BaseModel):
    unit_name: str
    ingredients: list[IngredientStop]


class StopSaleByIngredients(StopSale):
    reason: str
    ingredient_name: str


class StopSaleByChannels(StopSale):
    reason: str
    sales_channel_name: str


class StopSaleByStreets(StopSale):
    street_name: str


class StopSaleBySectors(StopSale):
    sector_name: str


class ReportFromMongoDB(TypedDict):
    chat_id: int
    unit_ids: list[int]


class OrderByUUID(BaseModel):
    unit_name: str
    created_at: datetime
    canceled_at: datetime
    number: str
    type: str
    price: int
    uuid: uuid.UUID


class StopsAndResumes(BaseModel):
    type: str
    unit_name: str
    product_name: str
    staff_name: str
    datetime: datetime


class StockBalance(BaseModel):
    ingredient_name: str
    days_left: int
    stocks_count: float | int
    stocks_unit: str


class StocksBalance(BaseModel):
    unit_name: str
    stocks_balance: list[StockBalance]


class WriteOffEventType(Enum):
    EXPIRE_AT_15_MINUTES = 'EXPIRE_AT_15_MINUTES'
    EXPIRE_AT_10_MINUTES = 'EXPIRE_AT_10_MINUTES'
    EXPIRE_AT_5_MINUTES = 'EXPIRE_AT_5_MINUTES'
    ALREADY_EXPIRED = 'ALREADY_EXPIRED'


class WriteOff(BaseModel):
    event_type: WriteOffEventType
    unit_name: str


class UsedPromoCode(BaseModel):
    promo_code: str
    order_no: str


class UnitUsedPromoCodes(BaseModel):
    unit_name: str
    promo_codes: list[UsedPromoCode]


EventPayload: TypeAlias = (
        OrderByUUID
        | StopSaleByStreets
        | StopSaleByChannels
        | StopSaleBySectors
        | StopSaleByIngredients
        | CheatedOrders
        | StopsAndResumes
)
