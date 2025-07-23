from dataclasses import dataclass
from decimal import Decimal
from typing import Dict

from src.wallets.currency import Currency
from src.wallets.exceptions import NegativeValueException, NotComparisonException


@dataclass
class Money:
    """
    Датакласс, представляющий денежную сумму и валюту.
    Attributes:
        value: числовое значение суммы,
        currency: объект валюты (Currency).
    """
    value: Decimal
    currency: Currency

    def __add__(self, other):
        """Складывает две суммы в одной валюте."""
        if self.currency != other.currency:
            raise NotComparisonException("Операция с разными валютами невозможна.")
        return Money(self.value + other.value, self.currency)

    def __sub__(self, other):
        """ Вычитает одну сумму из другой, при условии, что валюты совпадают."""
        if self.currency != other.currency:
            raise NotComparisonException("Операция с разными валютами невозможна.")
        return Money(self.value - other.value, self.currency)

    def is_negative(self):
        """Проверяет, является ли сумма отрицательной."""
        return self.value < 0


class Wallet:
    """Кошелёк, хранящий денежные суммы в разных валютах."""
    def __init__(self, *args: Money):
        """
        Инициализирует кошелёк с произвольным числом денежных сумм.
        Все суммы будут сгруппированы по валютам.
        """
        self._balances: Dict[Currency, Money] = {}
        for money in args:
            self.add(money)

    def __getitem__(self, currency: Currency) -> Money:
        """Возвращает сумму в указанной валюте."""
        return self._balances.get(currency, Money(Decimal(0), currency))

    def __setitem__(self, currency: Currency, money: Money):
        """Устанавливает сумму по валюте."""
        if currency != money.currency:
            raise ValueError("Несоответствие валют.")
        self._balances[currency] = money

    def __delitem__(self, currency: Currency):
        """Удаляет валюту из кошелька, если она там есть."""
        if currency in self._balances:
            del self._balances[currency]

    def __contains__(self, currency: Currency) -> bool:
        """Проверяет, содержится ли валюта в кошельке."""
        return currency in self._balances

    def __len__(self):
        """Возвращает количество различных валют в кошельке."""
        return len(self._balances)

    @property
    def currencies(self):
        """Возвращает список всех валют, имеющихся в кошельке."""
        return self._balances.keys()

    def add(self, money: Money) -> "Wallet":
        """Добавляет сумму к существующему балансу или создаёт новый."""
        current = self[money.currency]
        self[money.currency] = current + money
        return self

    def sub(self, money: Money) -> "Wallet":
        """Вычитает сумму из кошелька."""
        current = self[money.currency]
        result = current - money
        if result.is_negative():
            raise NegativeValueException(f"Недостаточно средств: {current.value} < {money.value}.")
        self[money.currency] = result
        return self