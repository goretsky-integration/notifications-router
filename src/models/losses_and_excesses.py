from pydantic import BaseModel

__all__ = ('UnitLossesAndExcesses',)


class LossesAndExcesses(BaseModel):
    percent_of_revenue: float
    amount: float


class UnitLossesAndExcesses(BaseModel):
    unit_name: str
    total_loss: LossesAndExcesses
    unaccounted_losses: LossesAndExcesses
    write_offs: LossesAndExcesses
    total_excess: LossesAndExcesses
