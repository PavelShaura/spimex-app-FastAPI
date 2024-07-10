import pytest
from datetime import date
from unittest.mock import AsyncMock, patch, MagicMock

from app.utils.parser.scrapping import scrape_reports
from app.utils.parser.download_files import download_file
from app.utils.parser.get_links import get_report_links
from app.utils.parser.extract_xml import extract_report_data


@pytest.mark.asyncio(scope="session")
class TestScraping:

    @pytest.mark.parametrize(
        "start_page,end_page,last_report_date,expected_calls",
        [
            (1, 3, None, 3),
            (1, 2, date(2023, 1, 1), 2),
            (1, 5, date(2024, 1, 1), 5),
        ]
    )
    async def test_scrape_reports(self, mock_aiohttp_session, start_page, end_page, last_report_date, expected_calls):

        mock_fetch_page = AsyncMock(return_value="<html>Mocked HTML</html>")

        mock_get_report_links = AsyncMock(return_value=[
            ("https://example.com/report1.xls", date(2024, 1, 1)),
            ("https://example.com/report2.xls", date(2024, 1, 2)),
        ])

        mock_download_file = AsyncMock()

        mock_extract_report_data = MagicMock(return_value=[
            {"exchange_product_id": "TEST001", "volume": 100, "date": date(2024, 1, 1)},
            {"exchange_product_id": "TEST002", "volume": 200, "date": date(2024, 1, 2)},
        ])

        with patch('app.utils.parser.scrapping.fetch_page', mock_fetch_page), \
                patch('app.utils.parser.scrapping.get_report_links', mock_get_report_links), \
                patch('app.utils.parser.scrapping.download_file', mock_download_file), \
                patch('app.utils.parser.scrapping.extract_report_data', mock_extract_report_data):
            result = await scrape_reports(start_page, end_page, last_report_date)

            assert len(result) > 0
            assert isinstance(result[0], dict)
            assert "exchange_product_id" in result[0]
            assert "volume" in result[0]
            assert "date" in result[0]

            assert mock_fetch_page.call_count == expected_calls
            assert mock_get_report_links.call_count == expected_calls
            assert mock_download_file.call_count == len(mock_get_report_links.return_value) * expected_calls
            assert mock_extract_report_data.call_count == len(mock_get_report_links.return_value)

    @pytest.mark.parametrize(
        "html_content,expected_links,expected_dates",
        [
            (
                    '<div class="accordeon-inner__wrap-item"><a class="accordeon-inner__item-title link xls" href="/report1.xls"></a><div class="accordeon-inner__item-inner__title"><span>01.01.2024</span></div></div>',
                    ["https://spimex.com/report1.xls"],
                    [date(2024, 1, 1)]
            ),
            (
                    '<div class="accordeon-inner__wrap-item"><a class="accordeon-inner__item-title link xls" href="/report1.xls"></a><div class="accordeon-inner__item-inner__title"><span>01.01.2024</span></div></div><div class="accordeon-inner__wrap-item"><a class="accordeon-inner__item-title link xls" href="/report2.xls"></a><div class="accordeon-inner__item-inner__title"><span>02.01.2024</span></div></div>',
                    ["https://spimex.com/report1.xls", "https://spimex.com/report2.xls"],
                    [date(2024, 1, 1), date(2024, 1, 2)]
            ),
        ]
    )
    async def test_get_report_links(self, html_content, expected_links, expected_dates):
        result = await get_report_links(html_content)
        assert len(result) == len(expected_links)
        for (link, date_obj), expected_link, expected_date in zip(result, expected_links, expected_dates):
            assert link == expected_link
            assert date_obj == expected_date

    @pytest.mark.parametrize(
        "file_content,expected_data",
        [
            (
                    "Код инструмента\tНаименование инструмента\tБазис поставки\tОбъем договоров в единицах измерения\tОбьем договоров, руб.\tКоличество договоров, шт.\nTEST001\tTest Product\tTest Basis\t100\t1000000\t10",
                    [{"exchange_product_id": "TEST001", "exchange_product_name": "Test Product",
                      "delivery_basis_name": "Test Basis", "volume": 100.0, "total": 1000000.0, "count": 10}]
            ),
        ]
    )
    def test_extract_report_data(self, tmp_path, file_content, expected_data):
        file_path = tmp_path / "test_report.xls"
        with open(file_path, "w") as f:
            f.write(file_content)

        result = extract_report_data(str(file_path))
        assert result == expected_data

    async def test_download_file(self, mock_aiohttp_session, tmp_path):
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read.return_value = b"Test file content"
        mock_session = AsyncMock()
        mock_session.get.return_value.__aenter__.return_value = mock_response

        url = "https://example.com/test.xls"
        report_date = date(2024, 1, 1)
        folder = str(tmp_path)

        await download_file(mock_session, url, report_date, folder)

        expected_file_path = tmp_path / "2024-01-01.xls"
        assert expected_file_path.exists()
        assert expected_file_path.read_bytes() == b"Test file content"