import collections
from datetime import timedelta, datetime
from decimal import Decimal
from typing import Protocol, Generic, TypeVar, Callable, Iterable

import humanize

import models
import utils
from text_utils import abbreviate_time_units, intgaps

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
            '<b>❗️ ПОДОЗРИТЕЛЬНО 🤨 ❗️️',
            f'{self._cheated_orders.unit_name}</b>',
            f'Номер: {self._cheated_orders.phone_number.removesuffix(".0")}',
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
        return humanize.precisedelta(self.stop_duration, suppress=['days'],
                                     minimum_unit='minutes', format='%0.0f')

    def as_text(self):
        first_line = (
            f'{self._stop_sale.unit_name} в стопе {self.humanized_order_duration}'
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

    def __init__(self, canceled_order: models.CanceledOrder):
        self.__canceled_order = canceled_order

    @property
    def order_url(self) -> str:
        return (
            'https://shiftmanager.dodopizza.ru/Managment/ShiftManagment/Order?'
            f'orderUUId={self.__canceled_order.id.hex}'
        )

    def as_text(self) -> str:
        return (
            f'Заказ <a href="{self.order_url}">'
            f'№{self.__canceled_order.number}</a>'
            f' {self.__canceled_order.price}₽\n'
            f'Тип заказа: {self.__canceled_order.sales_channel_name}'
        )


class UnitCanceledOrders:

    def __init__(self, unit_canceled_orders: models.UnitCanceledOrders):
        self.__unit_canceled_orders = unit_canceled_orders

    def calculate_total_price(self) -> Decimal:
        return sum(canceled_order.price for canceled_order
                   in self.__unit_canceled_orders.canceled_orders)

    def as_text(self) -> str:
        lines = [
            f'<b>Отчёт по отменам {self.__unit_canceled_orders.unit_name}:</b>',
        ]
        sorted_canceled_orders = sorted(
            self.__unit_canceled_orders.canceled_orders,
            key=lambda canceled_order: (
                canceled_order.sold_at,
                canceled_order.canceled_at,
            )
        )
        for canceled_order in sorted_canceled_orders:
            canceled_order_text = CanceledOrder(canceled_order).as_text()
            lines.append(f'\n{canceled_order_text}')

        total_price = int(self.calculate_total_price())

        lines.append(f'\n<b>Итого: {intgaps(total_price)}₽</b>')
        return '\n'.join(lines)


class StopsAndResumes:
    type_to_title = {
        'STOP': 'Остановка',
        'RESUME': 'Возобновление',
    }

    def __init__(self, stops_and_resumes: models.StopsAndResumes):
        self._stops_and_resumes = stops_and_resumes

    @property
    def title(self) -> str:
        humanized_title = self.type_to_title.get(self._stops_and_resumes.type,
                                                 self._stops_and_resumes.type)
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

    def __init__(self,
                 stop_sales_by_other_ingredients: models.StopSalesByOtherIngredients):
        self._stop_sales_by_other_ingredients = stop_sales_by_other_ingredients

    @staticmethod
    def get_stop_duration(stopped_at: datetime) -> int:
        return int((utils.get_moscow_datetime() - stopped_at).total_seconds())

    @staticmethod
    def get_humanized_stop_duration(stopped_at: datetime) -> str:
        stop_duration = StopSalesByOtherIngredients.get_stop_duration(
            stopped_at)
        if stop_duration >= DAY_IN_SECONDS:
            kwargs = {
                'format': '%0.0f', 'minimum_unit': 'days',
                'suppress': ['months']
            }
        elif stop_duration >= HOUR_IN_SECONDS:
            kwargs = {'format': '%0.0f', 'minimum_unit': 'hours'}
        else:
            kwargs = {'format': '%0.0f', 'minimum_unit': 'minutes'}
        return abbreviate_time_units(
            humanize.precisedelta(stop_duration, **kwargs))

    @staticmethod
    def group_by_reason(ingredients: Iterable[models.IngredientStop]) -> dict[
        str, list[models.IngredientStop]]:
        stop_reason_to_ingredients: dict[
            str, list[models.IngredientStop]] = collections.defaultdict(list)
        for ingredient in ingredients:
            ingredients_by_stop_reason = stop_reason_to_ingredients[
                ingredient.reason]
            ingredients_by_stop_reason.append(ingredient)
        return stop_reason_to_ingredients

    def as_text(self) -> str:
        lines = [f'<b>{self._stop_sales_by_other_ingredients.unit_name}</b>']
        if not self._stop_sales_by_other_ingredients.ingredients:
            lines.append(
                '<b>Стопов пока нет! Молодцы. Ваши Клиенты довольны</b>')
        for reason, ingredients in self.group_by_reason(
                self._stop_sales_by_other_ingredients.ingredients).items():
            lines.append(f'\n<b>{reason}:</b>')
            for ingredient in sorted(ingredients, key=lambda
                    ingredient: ingredient.started_at, reverse=True):
                humanized_stop_duration = self.get_humanized_stop_duration(
                    ingredient.started_at)
                lines.append(
                    f'📍 {ingredient.name} - <b><u>{humanized_stop_duration}</u></b>')
        return '\n'.join(lines)


class StocksBalance:

    def __init__(self, stocks_balance: models.StocksBalance):
        self._stocks_balance = stocks_balance

    def as_text(self) -> str:
        lines = [f'<b>{self._stocks_balance.unit_name}</b>']
        lines.append(
            '❗️ <b>На сегодня не хватит</b> ❗️' if self._stocks_balance.stocks_balance
            else '<b>На сегодня всего достаточно</b>')
        for stock_balance in self._stocks_balance.stocks_balance:
            lines.append(f'📍 {stock_balance.ingredient_name} - остаток'
                         f' <b><u>{stock_balance.stocks_count} {stock_balance.stocks_unit}</u></b>')
        return '\n'.join(lines)


class WriteOff:
    write_off_event_types_map = {
        models.WriteOffEventType.EXPIRE_AT_15_MINUTES: 'Списание ингредиентов через 15 минут',
        models.WriteOffEventType.EXPIRE_AT_10_MINUTES: 'Списание ингредиентов через 10 минут',
        models.WriteOffEventType.EXPIRE_AT_5_MINUTES: 'Списание ингредиентов через 5 минут',
        models.WriteOffEventType.ALREADY_EXPIRED: 'В пиццерии просрочка',
    }

    def __init__(self, write_off: models.WriteOff):
        self._write_off = write_off

    def as_text(self) -> str:
        return f'<b>❗️ {self._write_off.unit_name} ❗️</b>\n' + \
            self.write_off_event_types_map[
                self._write_off.event_type]


class UnitUsedPromoCodes:

    def __init__(self, unit_used_promo_codes: models.UnitUsedPromoCodes):
        self.__unit_used_promo_codes = unit_used_promo_codes

    def as_text(self) -> str:
        lines = [
            f'<b>{self.__unit_used_promo_codes.unit_name}:</b>',
            'Использованы промокоды:\n',
        ]
        for promo_code in self.__unit_used_promo_codes.promo_codes:
            lines.append(
                f'📍 <u>{promo_code.promo_code}</u> - заказ №{promo_code.order_no}')
        return '\n'.join(lines)


class UnitLateDeliveryVouchers:

    def __init__(
            self,
            unit_late_delivery_vouchers: models.UnitLateDeliveryVouchers,
    ):
        self.__unit_late_delivery_vouchers = unit_late_delivery_vouchers

    def as_text(self) -> str:
        lines: list[str] = [
            f'<b>{self.__unit_late_delivery_vouchers.unit_name}:</b>',
            'Выданы сертификаты за опоздание:\n',
        ]
        for order_number in self.__unit_late_delivery_vouchers.order_numbers:
            lines.append(f'📍 Заказ <b>№{order_number}</b>')
        return '\n'.join(lines)


class LossesAndExcessesRevisionView:

    def __init__(self, revision: models.LossesAndExcessesRevision):
        self.__revision = revision

    def as_text(self) -> str:
        return (
            f'<b>{self.__revision.unit_name}</b>\n'
            f'Итого потери -'
            f' {self.__revision.summary.total_loss.percent_of_revenue}%'
            f' / {self.__revision.summary.total_loss.amount} руб\n'
            f'Неучтённые потери -'
            f' {self.__revision.summary.unaccounted_losses.percent_of_revenue}%'
            f' / {self.__revision.summary.unaccounted_losses.amount} руб\n'
            f'Списания - {self.__revision.summary.write_offs.percent_of_revenue}'
            f'% / {self.__revision.summary.write_offs.amount} руб\n'
            f'Избыток - {self.__revision.summary.total_excess.percent_of_revenue}'
            f'% / {self.__revision.summary.total_excess.amount} руб'
        )
