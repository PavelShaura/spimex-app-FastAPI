import pytest
from datetime import date


@pytest.fixture
def mock_html_content():
    return """
    <div class="accordeon-inner__wrap-item">
        <a href="/files/report1.xls" class="accordeon-inner__item-title link xls">Report 1</a>
        <div class="accordeon-inner__item-inner__title"><span>01.07.2024</span></div>
    </div>
    <div class="accordeon-inner__wrap-item">
        <a href="/report2.xls" class="accordeon-inner__item-title link xls">Report 2</a>
        <div class="accordeon-inner__item-inner__title"><span>02.07.2024</span></div>
    </div>
    """


@pytest.fixture
def expected_links():
    return [
        ("https://spimex.com/report2.xls", date(2024, 7, 1)),
    ]
