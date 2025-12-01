import pytest

@pytest.fixture
def habr_article() -> str:
    with open(
        "tests/data/habr_article.html",
        "r",
        encoding="utf-8"
    ) as f:
        content = f.read()

    return content

