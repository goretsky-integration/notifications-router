import text_representations
import models


def test_bonus_system_fraud_text_report():
    bonus_system_fraud = models.BonusSystemFraud(
        department='Москва 4-1',
        phone_number='+7906676767',
        datetimes=[
            '2022-02-22T22:33:44',
            '2022-03-23T03:42:53',
        ],
    )
    expected = (
        '<b>❗️ МОШЕННИЧЕСТВО ❗️️</b>\n'
        'Москва 4-1\n'
        '+7906676767 - 22:33\n'
        '+7906676767 - 03:42'
    )
    assert text_representations.BonusSystemFraud(bonus_system_fraud).as_text() == expected
