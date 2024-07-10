import pytest
from aiohttp import ClientSession
from datetime import date
from unittest.mock import AsyncMock, MagicMock

from app.utils.parser.get_links import fetch_page, get_report_links


class TestGetLinks:
    @pytest.mark.asyncio(scope="session")
    async def test_fetch_page(self, mocker):
        mock_session = AsyncMock(spec=ClientSession)
        mock_response = AsyncMock()
        mock_response.text.return_value = "<html>Test content</html>"
        mock_session.get.return_value.__aenter__.return_value = mock_response

        url = "https://example.com"
        result = await fetch_page(mock_session, url)

        assert result == "<html>Test content</html>"
        mock_session.get.assert_called_once_with(url)
        mock_response.text.assert_called_once()

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.parametrize(
        "html_content, expected_links",
        [
            (
                """
                <div class="accordeon-inner__wrap-item">
                    <a href="/files/report1.xls" class="accordeon-inner__item-title link xls">Report 1</a>
                    <div class="accordeon-inner__item-inner__title"><span>01.07.2024</span></div>
                </div>
                <div class="accordeon-inner__wrap-item">
                    <a href="/report2.xls" class="accordeon-inner__item-title link xls">Report 2</a>
                    <div class="accordeon-inner__item-inner__title"><span>02.07.2024</span></div>
                </div>
                """,
                [
                    ("https://spimex.com/report2.xls", date(2024, 7, 1)),
                ],
            ),
        ],
    )
    async def test_get_report_links(self, html_content, expected_links):
        result = await get_report_links(html_content)
        assert result == expected_links
