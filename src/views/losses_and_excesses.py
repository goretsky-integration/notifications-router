from models import UnitLossesAndExcesses

__all__ = ('render_losses_and_excesses',)


def render_losses_and_excesses(
        unit_losses_and_excesses: UnitLossesAndExcesses,
) -> str:
    return (
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
