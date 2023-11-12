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
        f'📍 {unit_stop_sales.stops[0].ingredient_name}'
        f' - <b><u>{humanized_stop_duration}</u></b>'
    )

    assert actual == expected


def test_render_unit_stop_sales_multiple_stops():
    unit_stop_sales = UnitStopSalesByIngredientsFactory(
        stops=[
            StopSaleByIngredientFactory(
                reason='Закончилось',
                started_at='2021-01-01 00:00:00',
            ),
            StopSaleByIngredientFactory(
                reason='Закончилось',
                started_at='2021-01-02 00:00:00',
            ),
            StopSaleByIngredientFactory(
                reason='Просрочено',
                started_at='2021-01-03 00:00:00',
            )
        ],
    )

    actual = render_unit_stop_sales_by_ingredients(unit_stop_sales)

    ingredient_stop_durations = [
        humanize_stop_sale_duration(
            duration=compute_stop_sale_duration(started_at=stop.started_at),
        ) for stop in unit_stop_sales.stops
    ]

    expected = (
        f'<b>{unit_stop_sales.unit_name}</b>\n\n'
        '<b>Просрочено:</b>\n'
        f'📍 {unit_stop_sales.stops[2].ingredient_name}'
        f' - <b><u>{ingredient_stop_durations[2]}</u></b>\n\n'
        '<b>Закончилось:</b>\n'
        f'📍 {unit_stop_sales.stops[1].ingredient_name}'
        f' - <b><u>{ingredient_stop_durations[1]}</u></b>\n'
        f'📍 {unit_stop_sales.stops[0].ingredient_name}'
        f' - <b><u>{ingredient_stop_durations[0]}</u></b>'
    )

    assert actual == expected
