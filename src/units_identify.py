import collections
from typing import Iterable

import models


def group_chat_ids_by_unit_id(chats_to_retranslate: Iterable[models.ChatToRetranslate]) -> dict[int, set[int]]:
    unit_id_to_chat_ids: dict[int, set[int]] = collections.defaultdict(set)
    for chat_to_retranslate in chats_to_retranslate:
        for unit_id in chat_to_retranslate.unit_ids:
            chat_ids = unit_id_to_chat_ids[unit_id]
            chat_ids.add(chat_to_retranslate.chat_id)
    return unit_id_to_chat_ids
