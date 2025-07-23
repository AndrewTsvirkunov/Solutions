from typing import Any, TypeAlias

# определяем алиас для типа JSON
JSON: TypeAlias = dict[str, Any]


class Model:
    """
    Базовая модель хранящая в себе JSON-данные.

    Attributes:
        payload: исходные данные модели. Все поля читаются и записываются напрямую в этот словарь.
    """
    def __init__(self, payload: JSON):
        self.payload = payload


class Field:
    """
    Дескриптор для поля модели, позволяющий работать с вложенными значениями в JSON по заданному пути.

    Attributes:
        path: путь до значения через точки (например, "meta.slug" или "meta.remote.href").
    """
    def __init__(self, path: str):
        self.path = path

    def _split_path(self) -> list[str]:
        """
        Разбивает строковый путь на список ключей.
        Returns:
            Список ключей (например ["meta", "remote", "href"])
        """
        return self.path.split(".")

    def _get_from_payload(self, payload: JSON):
        """
        Получает значение из JSON-словаря по указанному пути.
        Обходит вложенные словари по ключам, указанным в self.path.

        Parameters:
            payload: вложенный словарь, в котором нужно найти значение.
        Returns:
            Любое значение, находящееся по пути, или None.
        """
        current = payload
        for key in self._split_path():
            current = current.get(key)
            if current is None:
                return None
        return current

    def _set_to_payload(self, payload: JSON, value: Any) -> None:
        """
        Устанавливает значение по пути в JSON-словаре, если промежуточные ключи существуют.
        Parameters:
            payload: вложенный словарь, куда нужно записать значение,
            value: новое значение для установки.
        """
        keys = self._split_path()
        current = payload
        for key in keys[:-1]:
            current = current.get(key)
            if current is None:
                return
        if isinstance(current, dict):
            current[keys[-1]] = value

    def __get__(self, instance: Model, owner):
        """
        Получает значение по пути из JSON.
        Parameters:
            instance: объект модели, содержащий payload,
            owner: класс, в котором определён дескриптор (не используется).
        Returns:
            Любое значение из JSON по указанному пути, либо None, если путь обрывается.
        """
        if instance is None:
            return self
        return self._get_from_payload(instance.payload)

    def __set__(self, instance, value):
        """
        Устанавливает значение по пути в JSON.
        Parameters:
            instance: объект модели, содержащий payload,
            value: новое значение, которое нужно установить.
        """
        self._set_to_payload(instance.payload, value)
