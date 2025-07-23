from dataclasses import dataclass

@dataclass(frozen=True)
class Currency:
    """
    Представление валюты по её строковому коду (например, 'RUB', 'USD').
    Attributes:
        code: строковый код валюты
    """
    code: str

    def __eq__(self, other):
        """
        Проверка на равенство двух валют по строковому коду.
        Return:
            True, если оба объекта Currency и их коды совпадают.
        """
        return isinstance(other, Currency) and self.code == other.code

    def __repr__(self):
        """
        Return:
            Строковое представление валюты.
        """
        return self.code


# Предопределенные валюты
rub = Currency("RUB")
usd = Currency("USD")