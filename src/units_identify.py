import collections
from typing import Iterable

import models


def group_chat_ids_by_unit_id(reports: Iterable[models.ReportFromMongoDB]) -> dict[int, set[int]]:
    unit_id_to_chat_ids = collections.defaultdict(set)
    for report in reports:
        for unit_id in report['unit_ids']:
            chat_ids = unit_id_to_chat_ids[unit_id]
            chat_ids.add(report['chat_id'])
            unit_id_to_chat_ids[unit_id] = chat_ids
    return unit_id_to_chat_ids
