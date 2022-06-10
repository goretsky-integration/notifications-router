import pytest, main

import exceptions
import models
import text_representations
from report_identify import identify_report, ReportType, ReportRepresentation


@pytest.fixture
def fraud_bonus_system_order_report():
    return {
        'department': 'Москва 4-1',
        'phone_number': '+7906676767',
        'datetimes': [
            '2022-02-22T22:33:44',
            '2022-03-23T03:42:53',
        ],
    }


def test_report_is_not_identified():
    report = {
        'type': 'SOME_UNKNOWN_TYPE',
        'payload': [],
    }
    with pytest.raises(exceptions.ReportIsNotIdentified):
        identify_report(report)


def test_report_is_identified(fraud_bonus_system_order_report):
    report = {
        'type': 'FRAUD_BONUS_SYSTEM_ORDER',
        'payload': fraud_bonus_system_order_report,
    }
    expected = ReportRepresentation(
        report_type=ReportType.FRAUD_BONUS_SYSTEM_ORDER,
        text_representation=text_representations.BonusSystemFraud,
        model=models.BonusSystemFraud,
        payload=fraud_bonus_system_order_report
    )
    assert identify_report(report) == expected


def test_report_payload_is_invalid():
    report = {
        'type': 'FRAUD_BONUS_SYSTEM_ORDER',
        'payload': {
            'key': 'value'
        }
    }
    with pytest.raises(exceptions.PayloadValidationError):
        identify_report(report)


if __name__ == '__main__':
    main()
