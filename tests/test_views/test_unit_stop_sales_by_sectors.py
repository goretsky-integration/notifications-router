from tests.factories import UnitStopSalesBySectorFactory
from views import render_unit_stop_sale_by_sectors


def test_render_unit_stop_sale_by_sectors():
    unit_stop_sales_by_sectors = UnitStopSalesBySectorFactory()

    actual = render_unit_stop_sale_by_sectors(unit_stop_sales_by_sectors)
    expected = (
        f"<b>{unit_stop_sales_by_sectors.unit_name}</b>\n"
        f"Сектор: {unit_stop_sales_by_sectors.stops[0].sector_name}"
        f" - с {unit_stop_sales_by_sectors.stops[0].started_at:%H:%M}"
    )

    assert actual == expected
