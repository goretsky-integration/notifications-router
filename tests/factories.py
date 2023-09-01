import factory

from models import (
    LossesAndExcessesRevision,
    LossesAndExcessesRevisionRevisionSummaryUnit,
    LossesAndExcessesRevisionSummary,
)

__all__ = (
    'LossesAndExcessesRevisionFactory',
    'LossesAndExcessesRevisionSummaryUnitFactory',
    'LossesAndExcessesRevisionSummaryFactory',
)


class LossesAndExcessesRevisionSummaryUnitFactory(factory.Factory):

    class Meta:
        model = LossesAndExcessesRevisionRevisionSummaryUnit

    percent_of_revenue = factory.Faker(
        'pyfloat',
        min_value=0,
        max_value=100,
        right_digits=2,
    )
    amount = factory.Faker(
        'pyfloat',
        min_value=0,
        max_value=100000,
        right_digits=2,
    )


class LossesAndExcessesRevisionSummaryFactory(factory.Factory):

    class Meta:
        model = LossesAndExcessesRevisionSummary

    total_loss = factory.SubFactory(
        LossesAndExcessesRevisionSummaryUnitFactory,
    )
    unaccounted_losses = factory.SubFactory(
        LossesAndExcessesRevisionSummaryUnitFactory,
    )
    write_offs = factory.SubFactory(
        LossesAndExcessesRevisionSummaryUnitFactory
    )
    total_excess = factory.SubFactory(
        LossesAndExcessesRevisionSummaryUnitFactory,
    )


class LossesAndExcessesRevisionFactory(factory.Factory):

    class Meta:
        model = LossesAndExcessesRevision

    unit_name = factory.Sequence(lambda n: f'Москва 4-{n}')
    summary = factory.SubFactory(
        LossesAndExcessesRevisionSummaryFactory,
    )
