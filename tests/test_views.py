import datetime
from uuid import UUID
from decimal import Decimal

import pytest

import models
import views


def test_bonus_system_fraud_text_report():
    bonus_system_fraud = models.CheatedOrders(
        unit_name='Москва 4-1',
        phone_number='+7 906 676-76-75',
        orders=[
            models.CheatedOrder(
                created_at='2022-02-22T22:33:44',
                number='32 - 3',
            )
        ]
    )
    expected = (
        '<b>❗️ МОШЕННИЧЕСТВО ❗️️\n'
        'Москва 4-1</b>\n'
        'Номер: +7 906 676-76-75\n'
        '22:33 - <b>заказ №32 - 3</b>'
    )
    assert views.CheatedOrders(bonus_system_fraud).as_text() == expected


def test_canceled_order_view(canceled_order):
    expected = (
        'Заказ <a href="https://shiftmanager.dodopizza.ru/Managment/'
        f'ShiftManagment/Order?orderUUId={canceled_order.id.hex}">'
        f'№{canceled_order.number}</a>'
        f' {canceled_order.price}₽\n'
        f'Тип заказа: {canceled_order.sales_channel_name}'
    )
    assert views.CanceledOrder(canceled_order).as_text() == expected


def test_unit_canceled_orders_view(canceled_order):
    unit_canceled_orders = models.UnitCanceledOrders(
        unit_name='Москва 1-1',
        canceled_orders=(canceled_order, canceled_order),
    )
    expected = (
        f'<b>Отчёт по отменам Москва 1-1:</b>\n'
        '\n'
        'Заказ <a href="https://shiftmanager.dodopizza.ru/Managment/'
        f'ShiftManagment/Order?orderUUId={canceled_order.id.hex}">'
        f'№{canceled_order.number}</a>'
        f' {canceled_order.price}₽\n'
        f'Тип заказа: {canceled_order.sales_channel_name}\n'
        '\n'
        'Заказ <a href="https://shiftmanager.dodopizza.ru/Managment/'
        f'ShiftManagment/Order?orderUUId={canceled_order.id.hex}">'
        f'№{canceled_order.number}</a>'
        f' {canceled_order.price}₽\n'
        f'Тип заказа: {canceled_order.sales_channel_name}\n'
        '\n'
        f'<b>Итого: 41₽</b>'
    )
    assert views.UnitCanceledOrders(unit_canceled_orders).as_text() == expected


def test_stop_sales_by_streets():
    stop_sales = models.StopSaleByStreets(
        unit_name='Москва 4-19',
        street_name='Пушкина 15',
        started_at='2022-06-22T00:00:00',
    )
    expected = (
        '❗️ Москва 4-19 в стопе 35 минут (с 00:00) ❗️\n'
        'Улица: Пушкина 15'
    )
    views.StopSaleByStreets.humanized_order_duration = '35 минут'
    assert views.StopSaleByStreets(stop_sales).as_text() == expected


def test_stop_sales_by_sectors():
    stop_sales = models.StopSaleBySectors(
        unit_name='Москва 4-19',
        sector_name='Пушкина 15',
        started_at='2022-06-22T00:00:00',
    )
    expected = (
        '❗️ Москва 4-19 в стопе 35 минут (с 00:00) ❗️\n'
        'Сектор: Пушкина 15'
    )
    views.StopSaleBySectors.humanized_order_duration = '35 минут'
    assert views.StopSaleBySectors(stop_sales).as_text() == expected


def test_stop_sales_by_ingredients():
    stop_sales = models.StopSaleByIngredients(
        unit_name='Москва 4-19',
        ingredient_name='Тесто 35',
        reason='Отключение электричества',
        started_at='2022-06-22T00:00:00',
    )
    expected = (
        '❗️ Москва 4-19 в стопе 35 минут (с 00:00) ❗️'
        '\nИнгредиент: Тесто 35'
        '\nПричина: Отключение электричества'
    )
    views.StopSaleByIngredients.humanized_order_duration = '35 минут'
    assert views.StopSaleByIngredients(stop_sales).as_text() == expected


def test_stop_sales_by_channels():
    stop_sales = models.StopSaleByChannels(
        unit_name='Москва 4-19',
        sales_channel_name='Самовывоз',
        reason='Отключение электричества',
        started_at='2022-06-22T00:00:00',
    )
    expected = (
        'Москва 4-19 в стопе 15 минут (с 00:00)\n'
        'Тип продажи: Самовывоз\n'
        'Причина: Отключение электричества'
    )
    views.StopSaleByChannels.humanized_order_duration = '15 минут'
    views.StopSaleByChannels.is_urgent = False
    assert views.StopSaleByChannels(stop_sales).as_text() == expected


def test_stops_and_resumes():
    stops_and_resumes = models.StopsAndResumes(
        type='STOP',
        unit_name='Москва 4-1',
        product_name='Тесто 45',
        staff_name='Sarafan Rustam',
        datetime='2022-07-17T00:00:00'
    )
    expected = (
        '<b>Остановка продаж</b>\n'
        'Точка продаж: Москва 4-1\n'
        'Продукт: Тесто 45\n'
        'Сотрудник: Sarafan Rustam\n'
        'Время: 17.07.2022 00:00'
    )
    assert views.StopsAndResumes(stops_and_resumes).as_text() == expected

    stops_and_resumes = models.StopsAndResumes(
        type='RESUME',
        unit_name='Москва 4-1',
        product_name='Тесто 45',
        staff_name='Sarafan Rustam',
        datetime='2022-07-17T00:00:00'
    )
    expected = (
        '<b>Возобновление продаж</b>\n'
        'Точка продаж: Москва 4-1\n'
        'Продукт: Тесто 45\n'
        'Сотрудник: Sarafan Rustam\n'
        'Время: 17.07.2022 00:00'
    )
    assert views.StopsAndResumes(stops_and_resumes).as_text() == expected


def test_stop_sales_by_sectors():
    stop_sale = models.StopSaleBySectors(
        unit_name='Москва 4-1',
        started_at='2022-06-05T00:00:00',
        sector_name='Rustama',
    )
    expected = (
        '❗️ Москва 4-1 в стопе 15 минут (с 00:00) ❗️\n'
        'Сектор: Rustama'
    )
    views.StopSaleBySectors.humanized_order_duration = '15 минут'
    views.StopSaleBySectors.is_urgent = True
    assert views.StopSaleBySectors(stop_sale).as_text() == expected


def test_stop_sales_by_streets():
    stop_sale = models.StopSaleByStreets(
        unit_name='Москва 4-1',
        started_at='2022-06-05T00:00:00',
        street_name='Rustama',
    )
    expected = (
        '❗️ Москва 4-1 в стопе 15 минут (с 00:00) ❗️\n'
        'Улица: Rustama'
    )
    views.StopSaleByStreets.humanized_order_duration = '15 минут'
    views.StopSaleByStreets.is_urgent = True
    assert views.StopSaleByStreets(stop_sale).as_text() == expected


def test_stop_sales_by_other_ingredients():
    stopped_ingredients = [
        models.IngredientStop(
            started_at='2022-05-05T00:00:00',
            name='Тесто 45',
            reason='Out of stock',
        ),
        models.IngredientStop(
            started_at='2021-05-05T00:00:00',
            name='Тесто 35',
            reason='Out of stock',
        ),
        models.IngredientStop(
            started_at='2024-05-05T00:00:00',
            name='Тесто 55',
            reason='Cooking',
        ),
    ]
    stop_sales_by_other_ingredients = models.StopSalesByOtherIngredients(
        unit_name='Москва 4-1',
        ingredients=stopped_ingredients,
    )
    views.StopSalesByOtherIngredients.get_humanized_stop_duration = lambda \
            *args: '15 минут'
    expected = (
        '<b>Москва 4-1</b>'
        '\n\n'
        '<b>Out of stock:</b>'
        '\n'
        '📍 Тесто 45 - <b><u>15 минут</u></b>'
        '\n'
        '📍 Тесто 35 - <b><u>15 минут</u></b>'
        '\n\n'
        '<b>Cooking:</b>'
        '\n'
        '📍 Тесто 55 - <b><u>15 минут</u></b>'
    )
    assert views.StopSalesByOtherIngredients(
        stop_sales_by_other_ingredients).as_text() == expected


@pytest.mark.parametrize(
    'event_type, humanized_event_type',
    [
        ('EXPIRE_AT_15_MINUTES', 'Списание ингредиентов через 15 минут'),
        ('EXPIRE_AT_10_MINUTES', 'Списание ингредиентов через 10 минут'),
        ('EXPIRE_AT_5_MINUTES', 'Списание ингредиентов через 5 минут'),
        ('ALREADY_EXPIRED', 'В пиццерии просрочка'),
    ]
)
def test_write_offs(event_type, humanized_event_type):
    model = models.WriteOff(event_type=event_type, unit_name='Москва 4-1')
    actual = views.WriteOff(model).as_text()
    expected = '<b>❗️ Москва 4-1 ❗️</b>\n' + humanized_event_type
    assert actual == expected


def test_unit_used_promocode():
    unit_used_promocodes = models.UnitUsedPromoCodes(
        unit_name='Москва 4-1',
        promo_codes=[
            models.UsedPromoCode(
                promo_code='QW3GY4X',
                order_no='32-2',
            ),
            models.UsedPromoCode(
                promo_code='GJ46J2FS',
                order_no='22-3',
            ),
        ],
    )
    view = views.UnitUsedPromoCodes(unit_used_promocodes)
    expected = (
        '<b>Москва 4-1:</b>'
        '\nИспользованы промокоды:'
        '\n'
        '\n📍 <u>QW3GY4X</u> - заказ №32-2'
        '\n📍 <u>GJ46J2FS</u> - заказ №22-3'
    )
    assert view.as_text() == expected
