"""Парсеры для Habr"""

from typing import Any
from .abc import Parser
from ..errors import ParseError

from bs4 import BeautifulSoup

class HabrParser(
    Parser[str, str]
):
    """Реализация парсера для Habr"""

    def parse(
        self,
        obj: str,
        **kwargs: Any
    ) -> str:

        soup = BeautifulSoup(obj, "html.parser")

        content_div    = soup.find("div", class_="article-body")
        article_header = soup.find(
            "h1",
            class_="tm-title tm-title_h1",
        )

        if not article_header:
            raise ParseError("Article has no title")

        if not content_div:
            raise ParseError("HTML have no content")

        text = content_div.get_text(" ")
        title = article_header.get_text(" ")

        title = "Название статьи: " + title

        return title + "\n\n" + text
