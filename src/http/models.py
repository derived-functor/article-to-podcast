"""Модели данных"""

from enum import Enum

class Method(str, Enum):
    """Метод запроса

    :ivar GET: GET запрос.
    """
    GET  = "get"
