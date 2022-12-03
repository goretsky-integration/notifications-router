import datetime

import pytest

from events import EventExpirationFilter


def get_current_datetime_mock() -> datetime.datetime:
    return datetime.datetime(year=2022, month=12, day=1, hour=12)


@pytest.mark.parametrize(
    'created_at, expected',
    [
        (datetime.datetime(year=2022, month=12, day=1, hour=11, minute=49, second=59), True),
        (datetime.datetime(year=2022, month=12, day=1, hour=11, minute=50), False),
        (datetime.datetime(year=2022, month=12, day=1, hour=12), False),
        (datetime.datetime(year=2022, month=12, day=2), False),
    ]
)
def test_events_expiration(created_at, expected):
    max_lifetime_in_seconds = 600
    event_expiration_filter = EventExpirationFilter(
        max_lifetime_in_seconds=max_lifetime_in_seconds,
        current_datetime_callback=get_current_datetime_mock,
    )
    assert event_expiration_filter.is_expired(created_at) == expected


def test_invalid_max_lifetime():
    for max_lifetime_in_seconds in (0, -1, 0.9, -99999):
        with pytest.raises(ValueError) as error:
            EventExpirationFilter(max_lifetime_in_seconds, get_current_datetime_mock)
        assert error.value.args[0] == 'Max lifetime must be at least 1 second'
