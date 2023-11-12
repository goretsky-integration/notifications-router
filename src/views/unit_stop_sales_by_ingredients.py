from models import UnitStopSalesByIngredients

from views.common import (
    group_by_reason,
    humanize_stop_sale_duration,
    sort_by_started_at,
    compute_stop_sale_duration,
)

__all__ = ('render_unit_stop_sales_by_ingredients',)


def render_unit_stop_sales_by_ingredients(
        unit_stop_sales_by_ingredients: UnitStopSalesByIngredients,
) -> str:
    lines = [f'<b>{unit_stop_sales_by_ingredients.unit_name}</b>']

    unit_stop_sales = sort_by_started_at(unit_stop_sales_by_ingredients.stops)

    if not unit_stop_sales:
        lines.append('<b>Стопов пока нет! Молодцы. Ваши Клиенты довольны</b>')

    for reason, stop_sales in group_by_reason(unit_stop_sales).items():
        lines.append(f'\n<b>{reason}:</b>')

        for stop_sale in stop_sales:
            duration = compute_stop_sale_duration(stop_sale.started_at)
            humanized_stop_duration = humanize_stop_sale_duration(duration)
            lines.append(
                f'📍 {stop_sale.ingredient_name}'
                f' - <b><u>{humanized_stop_duration}</u></b>'
            )

    return '\n'.join(lines)
