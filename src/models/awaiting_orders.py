from pydantic import BaseModel

__all__ = ('UnitAwaitingOrders',)


class UnitAwaitingOrders(BaseModel):
    unit_name: str
    heated_shelf_orders_count: int
    couriers_in_queue_count: int
    couriers_on_shift_count: int
