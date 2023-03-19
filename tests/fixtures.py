import datetime
from uuid import UUID
from decimal import Decimal

import pytest

import models


@pytest.fixture
def canceled_order():
    return models.CanceledOrder(
        id=UUID('6d4a6a5e-52c0-4446-84b2-5931b237339c'),
        sold_at=datetime.datetime(2023, 3, 4, 10, 4),
        canceled_at=datetime.datetime(2023, 3, 4, 12),
        number='21-2',
        sales_channel_name='Доставка',
        price=Decimal('20.5'),
    )
