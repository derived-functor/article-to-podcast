"""Базовые реализации"""

from typing import Any
from httpx import URL, Response, AsyncClient
from .abc import HttpClient
from src.http.models import Method

class BaseHttpClient(HttpClient):
    """Базовая реализация HTTP-клиента

    :param client: асинхронный клиент.
    """

    def __init__(
        self,
        client: AsyncClient = AsyncClient()
    ):
        self._client = client

    @property
    def client(self) -> AsyncClient:
        return self._client

    async def request(
        self,
        method: Method,
        url: str | URL,
        **kwargs: Any
    ) -> Response:
        """Делает запрос по URL

        :param method: тип метода.
        :param url: URL запроса.
        :param kwargs: дополнительные параметры.
            Если содержит `close_connection` (bool),
            то клиент будет закрыт после вызова метода.
            Данный параметр не идёт в запросы.

        :return: ответ на запрос.
        """

        close_connection: bool = False
        try:
            close_connection_arg = kwargs.pop("close_connection")

            if not isinstance(close_connection_arg, bool):
                raise ValueError(
                    "`close_connection` appeared to be not a bool value"
                )

            close_connection = close_connection_arg
        except KeyError:
            pass

        match method:

            case Method.GET:
                response = await self._client.get(url, **kwargs)

                if close_connection:
                    await self.close()

                return response

    async def close(self) -> None: # pragma: no cover
        """Закрывает соединение клиента"""

        await self._client.aclose()
