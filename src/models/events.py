from pydantic import BaseModel

from models.event_types import EventType

__all__ = ('Event',)


class Event(BaseModel):
    type: EventType
    chat_ids: set[int]
    payload: dict | list
    errors: list[dict]
