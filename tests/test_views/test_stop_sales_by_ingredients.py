from tests.factories import StopSaleByIngredientsFactory
from views import (
    render_stop_sale_by_ingredients,
    compute_stop_sale_duration,
    humanize_stop_sale_duration,
)


def test_render_stop_sale_by_ingredients() -> None:
    stop_sale = StopSaleByIngredientsFactory()

    actual = render_stop_sale_by_ingredients(stop_sale)

    stop_sale_duration = compute_stop_sale_duration(stop_sale.started_at)
    humanized_stop_sale_duration = humanize_stop_sale_duration(
        duration=stop_sale_duration,
    )
    humanized_stop_sale_started_at = f'{stop_sale.started_at:%H:%M}'

    expected = (
        f'❗️ {stop_sale.unit_name}'
        f' в стопе {humanized_stop_sale_duration}'
        f' (с {humanized_stop_sale_started_at}) ❗️\n'
        f'\nИнгредиент: {stop_sale.ingredient_name}'
        f'\nПричина: {stop_sale.reason}'
    )

    assert actual == expected
