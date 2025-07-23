from dataclasses import dataclass, field
from more_itertools import batched
from typing import Iterable, TypeAlias

SomeRemoteData: TypeAlias = int


class Fibo:
    """
    Итератор ленивой генерации чисел Фибоначчи до заданного количества.
    Не использует генераторы. Класс сам хранит состояние:
    предыдущие два значения и текущую позицию.
    """
    def __init__(self, n: int):
        self.n = n  # заданный номер
        self.index = 0  # текущая позиция
        self.a = 0  # пред-предыдущее число
        self.b = 1  # предыдущее число

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= self.n:
            raise StopIteration  # возбуждаем исключение

        result = self.a  # записываем в результат первое число из будущей суммы двух
        self.a, self.b = self.b, self.a + self.b  # обновляем числа, чтобы в следующей итерации вернуть первое перед суммированием

        self.index += 1  # обновляем позицию
        return result


@dataclass
class Query:
    """
    Датакласс с параметрами запроса к API.
    Attributes:
        per_page: сколько элементов вернуть на одной странице,
        page: номер страницы.
    """
    per_page: int = 3
    page: int = 1


@dataclass
class Page:
    """
    Датакласс с ответами от API.
    Attributes:
        per_page: сколько элементов на странице
        results: список данных
        next: номер следующей страницы, если есть (иначе None)
    """
    per_page: int = 3
    results: Iterable[SomeRemoteData] = field(default_factory=list)
    next: int | None = None


def request(query: Query) -> Page:
    """
    Эмуляция API-запроса: возвращает "страницу" с числами.

    Данные — числа от 0 до 9. Они разбиваются на чанки по query.per_page.
    Возвращается один чанк (query.page) и номер следующей страницы.
    Parameters:
        query: объект Query с per_page и page
    Return:
        объект Page с результатами и next
    """
    data = [i for i in range(0, 10)]
    chunks = list(batched(data, query.per_page))
    return Page(
        per_page=query.per_page,
        results=chunks[query.page - 1],
        next=query.page + 1 if query.page < len(chunks) else None,
    )


class RetrieveRemoteData:
    """
    Класс-генератор, постранично получающий данные с API.

    Использует эмуляцию запросов через функцию request().
    При каждой итерации возвращает один элемент из текущей страницы.

    Когда данные на странице заканчиваются — делает следующий запрос.
    """
    def __init__(self, per_page: int = 3):
        self.per_page = per_page

    def __iter__(self):
        page = 1  # начинаем с первой страницы

        while True:
            # формируем объект запроса с текущим номером страницы
            query = Query(per_page=self.per_page, page=page)
            data = request(query)  # получаем страницу данных (эмуляция API)

            # возвращаем элементы страницы по одному
            for item in data.results:
                yield item

            # если next == None - страниц больше нет, выходим
            if data.next is None:
                break

            page = data.next  # иначе двигаемся к следующей странице