from tests.factories import UnitLossesAndExcessesFactory
from views import render_losses_and_excesses


def test_render_losses_and_excesses() -> None:
    unit_losses_and_excesses = UnitLossesAndExcessesFactory()

    actual = render_losses_and_excesses(unit_losses_and_excesses)
    expected = (
        f'<b>{unit_losses_and_excesses.unit_name}</b>\n'
        f'Итого потери -'
        f' {unit_losses_and_excesses.total_loss.percent_of_revenue}%'
        f' / {unit_losses_and_excesses.total_loss.amount} руб\n'
        f'Неучтённые потери -'
        f' {unit_losses_and_excesses.unaccounted_losses.percent_of_revenue}%'
        f' / {unit_losses_and_excesses.unaccounted_losses.amount} руб\n'
        f'Списания - {unit_losses_and_excesses.write_offs.percent_of_revenue}'
        f'% / {unit_losses_and_excesses.write_offs.amount} руб\n'
        f'Избыток - {unit_losses_and_excesses.total_excess.percent_of_revenue}'
        f'% / {unit_losses_and_excesses.total_excess.amount} руб'
    )

    assert actual == expected
