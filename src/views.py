import collections
from datetime import timedelta, datetime
from typing import Protocol, Generic, TypeVar, Callable, Iterable

import humanize

import models
import utils
from text_utils import abbreviate_time_units

humanize.i18n.activate("ru_RU")

SS = TypeVar('SS', bound=models.StopSale)
C = TypeVar('C', bound=Callable)

HOUR_IN_SECONDS = 3600
DAY_IN_SECONDS = HOUR_IN_SECONDS * 24


class MessageView(Protocol[C]):
    """Report representation to send."""

    def __init__(self, *args, **kwargs): ...

    def as_text(self) -> str:
        """Representation as text."""


class CheatedOrders:

    def __init__(self, cheated_orders: models.CheatedOrders):
        self._cheated_orders = cheated_orders

    def as_text(self) -> str:
        lines = (
            '<b>❗️ МОШЕННИЧЕСТВО ❗️️',
            f'{self._cheated_orders.unit_name}</b>',
            f'Номер: {self._cheated_orders.phone_number}',
            '\n'.join(f'{order.created_at:%H:%M} - <b>заказ №{order.number}</b>'
                      for order in self._cheated_orders.orders)
        )
        return '\n'.join(lines)


class StopSale(Generic[SS]):

    def __init__(self, stop_sale: SS):
        self._stop_sale = stop_sale

    @property
    def stop_duration(self) -> timedelta:
        return utils.get_moscow_datetime() - self._stop_sale.started_at

    @property
    def is_urgent(self) -> bool:
        return self.stop_duration.total_seconds() >= 1800

    @property
    def humanized_order_duration(self) -> str:
        return humanize.precisedelta(self.stop_duration, suppress=['days'], minimum_unit='minutes', format='%0.0f')

    def as_text(self):
        first_line = (f'{self._stop_sale.unit_name} в стопе {self.humanized_order_duration}'
                      f' (с {self._stop_sale.started_at:%H:%M})')
        if self.is_urgent:
            first_line = '❗️ ' + first_line + ' ❗️'
        return first_line


class StopSaleByIngredients(StopSale[models.StopSaleByIngredients]):

    def as_text(self) -> str:
        text = super().as_text()
        text += (f'\nИнгредиент: {self._stop_sale.ingredient_name}'
                 f'\nПричина: {self._stop_sale.reason}')
        return text


class StopSaleByChannels(StopSale[models.StopSaleByChannels]):
    channel_name_map = {
        'Dine-in': 'Ресторан',
        'Takeaway': 'Самовывоз',
        'Delivery': 'Доставка',
    }

    @property
    def humanized_channel_name(self) -> str:
        return self.channel_name_map.get(self._stop_sale.sales_channel_name,
                                         self._stop_sale.sales_channel_name)

    def as_text(self) -> str:
        text = super().as_text()
        text += (f'\nТип продажи: {self.humanized_channel_name}'
                 f'\nПричина: {self._stop_sale.reason}')
        return text


class StopSaleBySectors(StopSale[models.StopSaleBySectors]):

    def as_text(self) -> str:
        text = super().as_text()
        text += f'\nСектор: {self._stop_sale.sector_name}'
        return text


class StopSaleByStreets(StopSale[models.StopSaleByStreets]):

    def as_text(self) -> str:
        text = super().as_text()
        text += f'\nУлица: {self._stop_sale.street_name}'
        return text


class CanceledOrder:

    def __init__(self, canceled_order: models.OrderByUUID):
        self._canceled_order = canceled_order

    @property
    def order_duration(self) -> timedelta:
        return self._canceled_order.receipt_printed_at - self._canceled_order.created_at

    @property
    def humanized_order_duration(self) -> str:
        return humanize.precisedelta(self.order_duration, suppress=['days'], minimum_unit='minutes', format='%0.0f')

    @property
    def order_url(self) -> str:
        return ('https://shiftmanager.dodopizza.ru/Managment/ShiftManagment/Order?'
                f'orderUUId={self._canceled_order.uuid.hex}')

    def as_text(self) -> str:
        return (
            f'{self._canceled_order.unit_name} отменён заказ'
            f' <a href="{self.order_url}">№{self._canceled_order.number}</a> в {self._canceled_order.price}₽\n'
            f'Тип заказа: {self._canceled_order.type}\n'
            f'Заказ сделан в {self._canceled_order.created_at:%H:%M},'
            f' отменён в {self._canceled_order.receipt_printed_at:%H:%M}\n'
            f'Между заказом и отменой прошло {self.humanized_order_duration}'
        )


class StopsAndResumes:
    type_to_title = {
        'STOP': 'Остановка',
        'RESUME': 'Возобновление',
    }

    def __init__(self, stops_and_resumes: models.StopsAndResumes):
        self._stops_and_resumes = stops_and_resumes

    @property
    def title(self) -> str:
        humanized_title = self.type_to_title.get(self._stops_and_resumes.type, self._stops_and_resumes.type)
        return f'<b>{humanized_title} продаж</b>'

    @property
    def humanized_datetime(self) -> str:
        return f'{self._stops_and_resumes.datetime:%d.%m.%Y %H:%M}'

    def as_text(self) -> str:
        return (
            f'{self.title}\n'
            f'Точка продаж: {self._stops_and_resumes.unit_name}\n'
            f'Продукт: {self._stops_and_resumes.product_name}\n'
            f'Сотрудник: {self._stops_and_resumes.staff_name}\n'
            f'Время: {self.humanized_datetime}'
        )


class StopSalesByOtherIngredients:

    def __init__(self, stop_sales_by_other_ingredients: models.StopSalesByOtherIngredients):
        self._stop_sales_by_other_ingredients = stop_sales_by_other_ingredients

    @staticmethod
    def get_stop_duration(stopped_at: datetime) -> int:
        return int((utils.get_moscow_datetime() - stopped_at).total_seconds())

    @staticmethod
    def get_humanized_stop_duration(stopped_at: datetime) -> str:
        stop_duration = StopSalesByOtherIngredients.get_stop_duration(stopped_at)
        if stop_duration >= DAY_IN_SECONDS:
            kwargs = {'format': '%0.0f', 'minimum_unit': 'days', 'suppress': ['months']}
        elif stop_duration >= HOUR_IN_SECONDS:
            kwargs = {'format': '%0.0f', 'minimum_unit': 'hours'}
        else:
            kwargs = {'format': '%0.0f', 'minimum_unit': 'minutes'}
        return abbreviate_time_units(humanize.precisedelta(stop_duration, **kwargs))

    @staticmethod
    def group_by_reason(ingredients: Iterable[models.IngredientStop]) -> dict[str, list[models.IngredientStop]]:
        stop_reason_to_ingredients: dict[str, list[models.IngredientStop]] = collections.defaultdict(list)
        for ingredient in ingredients:
            ingredients_by_stop_reason = stop_reason_to_ingredients[ingredient.reason]
            ingredients_by_stop_reason.append(ingredient)
        return stop_reason_to_ingredients

    def as_text(self) -> str:
        lines = [f'<b>{self._stop_sales_by_other_ingredients.unit_name}</b>']
        for reason, ingredients in self.group_by_reason(self._stop_sales_by_other_ingredients.ingredients).items():
            lines.append(f'\n<b>{reason}:</b>')
            for ingredient in sorted(ingredients, key=lambda ingredient: ingredient.started_at, reverse=True):
                humanized_stop_duration = self.get_humanized_stop_duration(ingredient.started_at)
                lines.append(f'📍 {ingredient.name} - <b><u>{humanized_stop_duration}</u></b>')
        return '\n'.join(lines)


class StocksBalance:

    def __init__(self, stocks_balance: models.StocksBalance):
        self._stocks_balance = stocks_balance

    def as_text(self) -> str:
        lines = [f'<b>{self._stocks_balance.unit_name}</b>', '❗️ <b>На сегодня не хватит</b> ❗️']
        for stock_balance in self._stocks_balance.stocks_balance:
            lines.append(f'📍 {stock_balance.ingredient_name} - остаток'
                         f' <b><u>{stock_balance.stocks_count} {stock_balance.stocks_unit}</u></b>')
        return '\n'.join(lines)
