import pytest
from aiohttp import ClientSession
from unittest.mock import AsyncMock

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
    async def test_get_report_links(self, mock_html_content, expected_links):
        result = await get_report_links(mock_html_content)
        assert result == expected_links
