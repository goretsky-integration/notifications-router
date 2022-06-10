from typing import Protocol

import models


class ReportMessage(Protocol):
    """Report representation to send."""

    def as_text(self) -> str:
        """Representation as text."""


class BonusSystemFraud:

    def __init__(self, bonus_system_fraud: models.BonusSystemFraud):
        self._bonus_system_fraud = bonus_system_fraud

    def as_text(self) -> str:
        lines = (
            '<b>❗️ МОШЕННИЧЕСТВО ❗️️</b>',
            self._bonus_system_fraud.department,
            '\n'.join(f'{self._bonus_system_fraud.phone_number} - {datetime:%H:%M}'
                      for datetime in self._bonus_system_fraud.datetimes)
        )
        return '\n'.join(lines)


AllTextRepresentations = BonusSystemFraud
