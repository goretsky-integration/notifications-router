from models import UnitIngredientStocksBalance

__all__ = ('render_ingredient_stocks_balance',)


def render_ingredient_stocks_balance(
        unit_ingredient_stocks_balance: UnitIngredientStocksBalance,
) -> str:
    lines = [f'<b>[{unit_ingredient_stocks_balance.unit_name}</b>']

    running_out_ingredients = unit_ingredient_stocks_balance.ingredients

    if not running_out_ingredients:
        lines.append('<b>На сегодня всего достаточно</b>')
    else:
        lines.append('❗️ <b>На сегодня не хватит</b> ❗️')

    for ingredient in running_out_ingredients:
        lines.append(
            f'📍 {ingredient.ingredient_name} - остаток'
            f' <b><u>{ingredient.stocks_count}'
            f' {ingredient.stocks_unit}</u></b>'
        )

    return '\n'.join(lines)
