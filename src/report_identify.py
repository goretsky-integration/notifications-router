from dataclasses import dataclass
from enum import Enum
from typing import TypedDict, Type

import exceptions
import models
import text_representations
import utils


class Report(TypedDict):
    type: str
    payload: dict | list


class ReportType(Enum):
    FRAUD_BONUS_SYSTEM_ORDER = 'FRAUD_BONUS_SYSTEM_ORDER'


@dataclass(frozen=True, slots=True)
class ReportRepresentation:
    report_type: ReportType
    payload: dict
    model: Type[models.AllModels]
    text_representation: Type[text_representations.AllTextRepresentations]


class RepresentationKit(TypedDict):
    model: Type[models.AllModels]
    text_representation: Type[text_representations.AllTextRepresentations]


report_type_to_representation_kit: dict[ReportType, RepresentationKit] = {
    ReportType.FRAUD_BONUS_SYSTEM_ORDER: {
        'model': models.BonusSystemFraud,
        'text_representation': text_representations.BonusSystemFraud,
    },
}


def identify_report(report: Report) -> ReportRepresentation:
    """Identify report and get its representation.

    Returns:
        Report representation.

    Raises:
        ReportIsNotIdentified if report is not identified.
        PayloadValidationError if report's payload is invalid.
    """
    for report_type in ReportType:
        if report_type.value != report['type']:
            continue
        representation_kit = report_type_to_representation_kit[report_type]
        utils.validate_payload(representation_kit['model'], report['payload'])
        return ReportRepresentation(
            report_type=report_type,
            payload=report['payload'],
            model=representation_kit['model'],
            text_representation=representation_kit['text_representation'],
        )
    raise exceptions.ReportIsNotIdentified
