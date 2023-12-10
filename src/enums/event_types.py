from enum import StrEnum, auto

__all__ = ('EventType',)


class EventType(StrEnum):
    CANCELED_ORDERS = auto()
    INGREDIENT_STOCKS_BALANCE = auto()
    LATE_DELIVERY_VOUCHERS_STATISTICS = auto()
    LOSSES_AND_EXCESSES = auto()
    REVENUE_STATISTICS = auto()
    STOP_SALES_BY_INGREDIENTS = auto()
    STOP_SALES_BY_SALES_CHANNELS = auto()
    SUSPICIOUS_ORDERS_BY_PHONE_NUMBER = auto()
    UNIT_STOP_SALES_BY_INGREDIENTS = auto()
    UNIT_STOP_SALES_BY_SECTORS = auto()
    WRITE_OFFS = auto()
