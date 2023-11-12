from models import UnitStopSalesBySectors

__all__ = ('render_unit_stop_sale_by_sectors',)


def render_unit_stop_sale_by_sectors(
        unit_stop_sales: UnitStopSalesBySectors,
) -> str:
    lines = [f'<b>{unit_stop_sales.unit_name}</b>']

    for stop_sale in unit_stop_sales.stops:
        lines.append(
            f'Сектор: {stop_sale.sector_name}'
            f' - с {stop_sale.started_at:%H:%M}'
        )

    return '\n'.join(lines)
