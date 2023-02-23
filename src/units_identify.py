import collections
from typing import Iterable

import models


def group_chat_ids_by_unit_id(report_routes: Iterable[models.ReportRoute]) -> dict[int, set[int]]:
    unit_id_to_chat_ids: dict[int, set[int]] = collections.defaultdict(set)
    for report_route in report_routes:
        for unit_id in report_route.unit_ids:
            chat_ids = unit_id_to_chat_ids[unit_id]
            chat_ids.add(report_route.chat_id)
    return unit_id_to_chat_ids
