import pytest
from pydantic import parse_obj_as

from models import ChatToRetranslate
from units_identify import group_chat_ids_by_unit_id


def test_group_chat_ids_by_unit_ids():
    data = [
        {
            'chat_id': 434234,
            'unit_ids': [641],
        },
        {
            'chat_id': 5435436,
            'unit_ids': [865, 465],
        },
        {
            'chat_id': 645645,
            'unit_ids': [865],
        },
        {
            'chat_id': 645645,
            'unit_ids': [641],
        },
    ]
    expected = {
        465: {5435436},
        641: {645645, 434234},
        865: {645645, 5435436}
    }
    assert group_chat_ids_by_unit_id(parse_obj_as(list[ChatToRetranslate], data)) == expected
