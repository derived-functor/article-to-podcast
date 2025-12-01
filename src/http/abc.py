"""Абстрактные классы"""

from abc import ABC, abstractmethod
from typing import Any

from httpx import URL, Response

from .models import Method

class HttpClient(ABC):
    """Абстрактный HTTP-клиент"""
    
    @abstractmethod
    async def request(
        self,
        method: Method,
        url: str | URL,
        **kwargs: Any
    ) -> Response:
        """Делает запрос

        :param method: тип метода.
        :param url: URL запроса.
        :param kwargs: дополнительные параметры запроса.

        :return: ответ на запрос.
        """
