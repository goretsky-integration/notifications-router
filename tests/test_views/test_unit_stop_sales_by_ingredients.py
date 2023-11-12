from tests.factories import (
    UnitStopSalesByIngredientsFactory,
    StopSaleByIngredientFactory,
)
from views import (
    render_unit_stop_sales_by_ingredients,
    compute_stop_sale_duration,
    humanize_stop_sale_duration,
)


def test_render_unit_stop_sales_no_stops():
    unit_stop_sales = UnitStopSalesByIngredientsFactory(stops=[])

    actual = render_unit_stop_sales_by_ingredients(unit_stop_sales)

    expected = (
        f'<b>{unit_stop_sales.unit_name}</b>\n'
        '<b>Стопов пока нет! Молодцы. Ваши Клиенты довольны</b>'
    )

    assert actual == expected


def test_render_unit_stop_sales_one_stop():
    unit_stop_sales = UnitStopSalesByIngredientsFactory(
        stops=[
            StopSaleByIngredientFactory(
                ingredient_name='Картошка',
                reason='Закончилось',
                started_at='2021-01-01 00:00:00',
            ),
        ],
    )

    actual = render_unit_stop_sales_by_ingredients(unit_stop_sales)

    duration = compute_stop_sale_duration(unit_stop_sales.stops[0].started_at)
    humanized_stop_duration = humanize_stop_sale_duration(duration)

    expected = (
        f'<b>{unit_stop_sales.unit_name}</b>\n\n'
        '<b>Закончилось:</b>\n'
        f'📍 Картошка - <b><u>{humanized_stop_duration}</u></b>'
    )

    assert actual == expected
