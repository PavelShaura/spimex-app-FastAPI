import pytest
from aiohttp import ClientSession
from datetime import date
from unittest.mock import AsyncMock, MagicMock

from app.utils.parser.download_files import download_file


class TestDownloadFile:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "url, report_date, folder",
        [
            ("https://example.com/file.xls", date(2024, 7, 1), "test_downloads"),
            (
                "https://example.com/another_file.xls",
                date(2024, 7, 2),
                "test_downloads",
            ),
        ],
    )
    async def test_download_file_success(
        self, mocker, url, report_date, folder, capsys
    ):
        mock_session = AsyncMock(spec=ClientSession)
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read = AsyncMock(return_value=b"file content")
        mock_session.get.return_value.__aenter__.return_value = mock_response

        mock_makedirs = mocker.patch("os.makedirs")
        mock_open = mocker.patch("builtins.open", mocker.mock_open())

        await download_file(mock_session, url, report_date, folder)

        captured = capsys.readouterr()

        mock_makedirs.assert_called_once_with(folder, exist_ok=True)
        mock_session.get.assert_called_once_with(url)
        mock_response.read.assert_called_once()

        expected_filename = f"{folder}/{report_date}.xls"

        mock_open.assert_called_once_with(expected_filename, "wb")
        mock_open().write.assert_called_once_with(b"file content")

    @pytest.mark.asyncio
    async def test_download_file_failure(self, mocker, capsys):
        mock_session = AsyncMock(spec=ClientSession)
        mock_response = MagicMock()
        mock_response.status = 404
        mock_session.get.return_value.__aenter__.return_value = mock_response

        url = "https://example.com/nonexistent.xls"
        report_date = date(2024, 7, 3)
        folder = "test_downloads"

        mock_makedirs = mocker.patch("os.makedirs")
        mock_open = mocker.patch("builtins.open", mocker.mock_open())

        await download_file(mock_session, url, report_date, folder)

        captured = capsys.readouterr()

        mock_makedirs.assert_called_once_with(folder, exist_ok=True)
        mock_session.get.assert_called_once_with(url)
        mock_open.assert_not_called()
