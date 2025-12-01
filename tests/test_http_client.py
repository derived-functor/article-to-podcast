import pytest
from unittest.mock import AsyncMock, patch
from src.http import (
    HttpClient,
    BaseHttpClient,
    Method,
)
from httpx import Response

class TestHttpClient:

    @pytest.fixture
    def url(self) -> str:
        return "https://habr.com/ru/news/958160/"

    @pytest.fixture
    def http_client(self) -> HttpClient:
        return BaseHttpClient()

    @pytest.fixture
    def habr_article(self) -> str:
        with open(
            "tests/data/habr_article.html",
            "r",
            encoding="utf-8"
        ) as f:
            content = f.read()

        return content

    @pytest.fixture
    def habr_article_response(self, habr_article: str) -> Response:
        response = Response(
            status_code=200,
            content=habr_article.encode("utf-8"),
        )

        return response

    @patch(
        "src.http.base.AsyncClient.get",
        new_callable=AsyncMock
    )
    async def test_request(
        self,
        mock_get: AsyncMock,
        http_client: HttpClient,
        url: str,
        habr_article_response: Response
    ):
        mock_get.return_value = habr_article_response

        response: Response = await http_client.request(
            method=Method.GET,
            url=url,
        )

        mock_get.assert_called_once_with(
            url
        )

        assert response, \
        f"Ожидался не пустой ответ. Получили {response}"

        assert response.is_success, \
        f"Ожидался успешный ответ. Получили {response.status_code}"

        assert response.text, \
        f"Ожидался контент. Получили {response.text}"

    @patch(
        "src.http.base.AsyncClient.get",
        new_callable=AsyncMock
    )
    async def test_request_close_connection(
        self,
        mock_get: AsyncMock,
        http_client: BaseHttpClient,
    ):
        await http_client.request(
            method=Method.GET,
            url="url",
            close_connection=True
        )

        assert http_client.client.is_closed, \
        "Ожидалось, что клиент будет закрыт после вызова"

    @patch(
        "src.http.base.AsyncClient.get",
        new_callable=AsyncMock
    )
    async def test_request_close_connection_value_error(
        self,
        mock_get: AsyncMock,
        http_client: BaseHttpClient,
    ):

        with pytest.raises(
            ValueError,
            match="`close_connection` appeared to be not a bool value"
        ):
            await http_client.request(
                method=Method.GET,
                url="url",
                close_connection=123
            )


    async def test_close_client(
        self,
        http_client: BaseHttpClient
    ):
        await http_client.close()

        assert http_client.client.is_closed, \
        "Ожидалось, что клиент будет закрыт."
