import datetime
from typing import Callable

__all__ = ('EventExpirationFilter',)


class EventExpirationFilter:
    """
    Sometimes events stuck and aren't sending for a long time,
    so some of them might not have relevance if they aren't delivered at time.
    This filter prevents sending not relevant messages.
    """
    __slots__ = ('__max_lifetime_in_seconds', '__get_current_datetime')

    def __init__(
            self,
            max_lifetime_in_seconds: int | float,
            current_datetime_callback: Callable[[], datetime.datetime] = datetime.datetime.utcnow,
    ):
        self.__max_lifetime_in_seconds = max_lifetime_in_seconds
        self.__get_current_datetime = current_datetime_callback
        self.__validate_initial_arguments()

    def __validate_initial_arguments(self):
        if self.__max_lifetime_in_seconds < 1:
            raise ValueError('Max lifetime must be at least 1 second')

    def is_expired(self, event_created_at: datetime.datetime) -> bool:
        event_lifetime = self.__get_current_datetime() - event_created_at
        return event_lifetime.total_seconds() > self.__max_lifetime_in_seconds
