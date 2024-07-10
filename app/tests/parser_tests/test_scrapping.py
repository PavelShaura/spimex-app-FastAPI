from datetime import date

import pytest

from app.utils.parser.scrapping import scrape_reports


class TestScrapping:
    @pytest.mark.asyncio(scope="session")
    async def test_scrape_reports(self, mocker):
        mock_fetch_page = mocker.patch("app.utils.parser.scrapping.fetch_page")
        mock_get_report_links = mocker.patch(
            "app.utils.parser.scrapping.get_report_links"
        )
        mock_download_file = mocker.patch("app.utils.parser.scrapping.download_file")
        mock_extract_report_data = mocker.patch(
            "app.utils.parser.scrapping.extract_report_data"
        )

        mock_fetch_page.return_value = "<html>Test content</html>"
        mock_get_report_links.return_value = [
            ("https://example.com/report1.xls", date(2024, 7, 1)),
            ("https://example.com/report2.xls", date(2024, 7, 2)),
        ]
        mock_extract_report_data.return_value = [
            {
                "exchange_product_id": "PROD001",
                "exchange_product_name": "Product 1",
                "delivery_basis_name": "Base 1",
                "volume": 100.0,
                "total": 1000000.0,
                "count": 10,
            }
        ]

        result = await scrape_reports(start_page=1, end_page=1)

        assert len(result) == 2  # Два отчета
        assert "date" in result[0]
        assert "created_on" in result[0]
        assert "updated_on" in result[0]

    @pytest.mark.asyncio(scope="session")
    async def test_scrape_reports_with_last_report_date(self, mocker):
        mock_fetch_page = mocker.patch("app.utils.parser.scrapping.fetch_page")
        mock_get_report_links = mocker.patch(
            "app.utils.parser.scrapping.get_report_links"
        )
        mock_download_file = mocker.patch("app.utils.parser.scrapping.download_file")
        mock_extract_report_data = mocker.patch(
            "app.utils.parser.scrapping.extract_report_data"
        )

        mock_fetch_page.return_value = "<html>Test content</html>"
        mock_get_report_links.return_value = [
            ("https://example.com/report1.xls", date(2024, 7, 2)),
            ("https://example.com/report2.xls", date(2024, 7, 1)),
        ]
        mock_extract_report_data.return_value = [
            {
                "exchange_product_id": "PROD001",
                "exchange_product_name": "Product 1",
                "delivery_basis_name": "Base 1",
                "volume": 100.0,
                "total": 1000000.0,
                "count": 10,
            }
        ]

        result = await scrape_reports(
            start_page=1, end_page=1, last_report_date=date(2024, 7, 1)
        )

        assert len(result) == 1  # Только один отчет после указанной даты
        assert result[0]["date"] == date(2024, 7, 2)
