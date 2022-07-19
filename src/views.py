from datetime import timedelta
from typing import Protocol, Generic, TypeVar, Callable

import humanize

import models
import utils

humanize.i18n.activate("ru_RU")

SS = TypeVar('SS', bound=models.StopSale)
C = TypeVar('C', bound=Callable)


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
