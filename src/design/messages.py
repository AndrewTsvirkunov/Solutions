import enum
import json
from dataclasses import dataclass
from typing import Dict, Any


class MessageType(enum.Enum):
    """
    Перечисление поддерживаемых источников сообщений.
    Используется для определения какой парсер выбрать.
    """
    TELEGRAM = enum.auto()
    MATTERMOST = enum.auto()
    SLACK = enum.auto()


@dataclass
class JsonMessage:
    """
    Сообщение, полученное из внешней системы.
    Attributes:
        message_type: тип источника,
        payload: строка с JSON-данными, содержащими имя пользователя и текст.
    """
    message_type: MessageType
    payload: str


@dataclass
class ParsedMessage:
    """
    Сообщение приведенное к единому внутреннему формату.
    Attributes:
        user: имя пользователя,
        text: текст сообщения.
    """
    user: str
    text: str


class MessageParser:
    """
    Абстрактный класс парсера сообщений.
    Все конкретные классы-парсеры должны реализовать метод parse(),
    который преобразует JSON-строку в ParsedMessage.
    """
    def parse(self, payload: str) -> ParsedMessage:
        """
        Преобразует JSON-payload в ParsedMessage.
        Parameters:
            payload: строка в формате JSON
        Return:
            Объект класса внутреннего формата.
        """
        raise NotImplementedError("Метод parse() должен быть реализован в подклассе.")


class TelegramParser(MessageParser):
    """
    Парсер сообщений из Telegram.

    Примерный формат payload:
    {
        "from": "Имя пользователя",
        "message": "Текст сообщения"
    }
    """
    def parse(self, payload: str) -> ParsedMessage:
        data: Dict[str, Any] = json.loads(payload)
        return ParsedMessage(user=data["from"], text=data["message"])


class MattermostParser(MessageParser):
    """
    Парсер сообщений из Mattermost.

    Примерный формат payload:
    {
        "username": "Имя пользователя",
        "text": "Текст сообщения"
    }
    """
    def parse(self, payload: str) -> ParsedMessage:
        data: Dict[str, Any] = json.loads(payload)
        return ParsedMessage(user=data["username"], text=data["text"])


class SlackParser(MessageParser):
    """
    Парсер сообщений из Slack.

    Примерный формат payload:
    {
        "user_name": "ИмяПользователя",
        "content": "Текст сообщения"
    }
    """
    def parse(self, payload: str) -> ParsedMessage:
        data: Dict[str, Any] = json.loads(payload)
        return ParsedMessage(user=data["user_name"], text=data["content"])


class ParserFactory:
    """
    Фабрика для выбора подходящего парсера на основе типа сообщения.
    """
    def __init__(self):
        self._parsers = {
            MessageType.TELEGRAM: TelegramParser(),
            MessageType.MATTERMOST: MattermostParser(),
            MessageType.SLACK: SlackParser()
        }

    def get_parser(self, message_type: MessageType) -> MessageParser:
        """
        Возвращает соответствующий парсер.
        Parameters:
            message_type: тип источника (например, MessageType.TELEGRAM)
        Return:
            Экземпляр соответствующего парсера.
        """
        parser = self._parsers.get(message_type)
        if not parser:
            raise ValueError(f"Парсер не найден для типа: {message_type}")
        return parser


def handle_message(json_message: JsonMessage) -> ParsedMessage:
    """
    Обрабатывает входящее сообщение, выбирает нужный парсер
    и возвращает ParsedMessage.
    Parameters:
        json_message: объект JsonMessage с типом источника и данными
    Return:
        ParsedMessage - сообщение приведенное к единому внутреннему формату.
    """
    factory = ParserFactory()
    parser = factory.get_parser(json_message.message_type)
    return parser.parse(json_message.payload)


if __name__ == "__main__":
    telegram_mes = JsonMessage(
        message_type=MessageType.TELEGRAM,
        payload='{"from": "Andrew", "message": "Hello, reviewer!"}'
    )

    parsed = handle_message(telegram_mes)
    print(parsed)