from models import StopSaleByIngredients
from views.common import render_stop_sale_header

__all__ = ('render_stop_sale_by_ingredients',)


def render_stop_sale_by_ingredients(
        stop_sale: StopSaleByIngredients,
) -> str:
    header = render_stop_sale_header(stop_sale)
    return (
        f'{header}\n'
        f'\nИнгредиент: {stop_sale.ingredient_name}'
        f'\nПричина: {stop_sale.reason}'
    )
