import textwrap

from factories import LossesAndExcessesRevisionFactory
from views import LossesAndExcessesRevisionView


def test_losses_and_excesses_revision_view():
    revision = LossesAndExcessesRevisionFactory()
    view = LossesAndExcessesRevisionView(revision)
    expected = textwrap.dedent(f'''\
    <b>{revision.unit_name}</b>
    Итого потери - {revision.summary.total_loss.percent_of_revenue}% / {revision.summary.total_loss.amount} руб
    Неучтённые потери - {revision.summary.unaccounted_losses.percent_of_revenue}% / {revision.summary.unaccounted_losses.amount} руб
    Списания - {revision.summary.write_offs.percent_of_revenue}% / {revision.summary.write_offs.amount} руб
    Избыток - {revision.summary.total_excess.percent_of_revenue}% / {revision.summary.total_excess.amount} руб''')
    assert view.as_text() == expected
