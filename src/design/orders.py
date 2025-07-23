from dataclasses import dataclass
from typing import List


@dataclass
class Order:
    """
    Датакласс, представляющий заказ.
    Attributes:
        total_amount: исходная сумма заказа,
        is_loyal_customer: флаг постоянного клиента,
        discount_codes: список промокодов, указывающих на определенную скидку (например ["FIX10", "PERCENT5"]).
    """
    total_amount: float
    is_loyal_customer: bool
    discount_codes: List[str]


class Discount:
    """
    Абстрактный класс, все классы скидок должны иметь метод apply().
    """
    def apply(self, order: Order):
        """
        Вычисляет сумму скидки к заказу.
        Parameters:
            order: объект заказа
        Return:
            Сумма скидки
        """
        raise NotImplementedError("Метод apply() должен быть реализован в подклассе.")


class FixedDiscount(Discount):
    """
    Скидка фиксированной суммы (например -10).
    """
    def __init__(self, amount: float):
        self.amount = amount

    def apply(self, order: Order) -> float:
        """
        Возвращает скидку фиксированной суммы.
        Parameters:
            order: объект заказа
        Return:
            Сумма скидки
        """
        return self.amount


class PercentageDiscount(Discount):
    """
    Скидка в процентах от суммы заказа (например -5%).
    """
    def __init__(self, percent: float):
        self.percent = percent

    def apply(self, order: Order) -> float:
        """
        Возвращает скидку в процентах от суммы заказа.
        Parameters
            order: объект заказа
        Return:
            Сумма скидки
        """
        return order.total_amount * (self.percent / 100)


class LoyaltyDiscount(Discount):
    """
    Скидка для постоянных клиентов.
    """
    def __init__(self, amount: float):
        self.amount = amount

    def apply(self, order: Order) -> float:
        """
        Возвращает скидку, если клиент постоянный.
        Parameters
            order: объект заказа
        Return:
            Сумма скидки, иначе 0
        """
        if order.is_loyal_customer:
            return self.amount
        return 0.0


class DiscountFactory:
    """
    Фабрика для выбора и создания подходящих скидок.
    """
    @staticmethod
    def get_discounts_for_order(order: Order) -> List[Discount]:
        """
        Возвращает список применимых скидок для переданного заказа.
        Parameters
            order: объект заказа
        Return:
            Список объектов классов-скидок.
        """
        discounts = []

        for code in order.discount_codes:
            if code == "FIX10":
                discounts.append(FixedDiscount(10))
            elif code == "PERCENT5":
                discounts.append(PercentageDiscount(5))

        if order.is_loyal_customer:
            discounts.append(LoyaltyDiscount(5))

        return discounts


def apply_discounts(order: Order) -> float:
    """
    Применяет все подходящие скидки к заказу и возвращает итоговую сумму.
    Parameters:
        order: исходный заказ
    Return:
        Финальная сумма после применения всех скидок (не меньше 0).
    """
    discounts = DiscountFactory.get_discounts_for_order(order)

    total_discount = 0.0
    for discount in discounts:
        discount_value = discount.apply(order)
        total_discount += discount_value

    final_amount = max(0.0, order.total_amount - total_discount)
    return final_amount


if __name__ == "__main__":
    example_order = Order(
        total_amount=100.0,
        is_loyal_customer=True,
        discount_codes=["FIX10", "PERCENT5"]
    )

    final_price = apply_discounts(example_order)
    print(f"Итоговая сумма с заказа с учетом скидок: {final_price}")