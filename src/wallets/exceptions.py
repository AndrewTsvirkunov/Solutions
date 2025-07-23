class NegativeValueException(Exception):
    """
    Исключение, возникающее при попытке вычесть больше, чем есть (получить отрицательное значение).
    """
    pass


class NotComparisonException(Exception):
    """
    Исключение, возникающее при попытке сложения или вычитания денег в разных валютах.
    """
    pass