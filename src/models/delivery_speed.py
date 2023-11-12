from pydantic import BaseModel

__all__ = ('UnitAverageDeliverySpeedStatistics',)


class UnitAverageDeliverySpeedStatistics(BaseModel):
    unit_name: str
    delivery_order_fulfillment_time_in_seconds: int
    cooking_time_in_seconds: int
    heated_shelf_time_in_seconds: int
    order_trip_time_in_seconds: int
