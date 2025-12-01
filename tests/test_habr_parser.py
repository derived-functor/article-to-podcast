import re
import pytest
from src.errors import ParseError
from src.parsers import Parser, HabrParser

class TestHabrParser:

    @pytest.fixture
    def parser(self) -> Parser[str, str]:
        return HabrParser()

    def test_parse(
        self,
        parser: Parser[str, str],
        habr_article: str
    ):
        content: str = parser.parse(habr_article)

        print(content)

        assert content, \
        f"Ожидался не пустой ответ. Получили {content}"

    def test_parse_no_content(
        self,
        parser: Parser[str, str],
        habr_article: str
    ):
        habr_article = re.sub("<div class=\"article-body\".*>", "", habr_article)

        with pytest.raises(ParseError, match="HTML have no content"):
            parser.parse(habr_article)

    def test_parse_no_title(
        self,
        parser: Parser[str, str],
        habr_article: str
    ):
        habr_article = re.sub("<h1.*>", "", habr_article)

        print(habr_article)

        with pytest.raises(ParseError, match="Article has no title"):
            parser.parse(habr_article)
