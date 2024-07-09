import aiohttp
import asyncio
from datetime import date, datetime
from typing import List, Dict, Any

from app.utils.parser.download_files import download_file
from app.utils.parser.get_links import fetch_page, get_report_links
from app.utils.parser.extract_xml import extract_report_data

BASE_URL = "https://spimex.com/markets/oil_products/trades/results/"


async def scrape_reports(
    start_page: int = 1, end_page: int = 3, last_report_date: date = None
) -> List[Dict[str, Any]]:
    """
    Сканирует отчеты с сайта и извлекает данные.

    :param start_page: Начальная страница для сканирования. По умолчанию 1.
    :param end_page: Конечная страница для сканирования. По умолчанию 365.
    :return: Список словарей с данными отчетов.
    """
    print("Starting report scraping...")

    tasks = []
    all_data = []
    link_date_map = {}

    async with aiohttp.ClientSession() as session:
        for page in range(start_page, end_page + 1):
            page_url = f"{BASE_URL}?page=page-{page}"
            page_html = await fetch_page(session, page_url)
            report_links_and_dates = await get_report_links(page_html)

            found_old_data = False

            for link, date in report_links_and_dates:
                if last_report_date and date <= last_report_date:
                    found_old_data = True
                    break

                if date.year >= 2023:
                    link_date_map[link] = date
                    task = asyncio.create_task(download_file(session, link, date))
                    tasks.append(task)

            if found_old_data:
                break

        await asyncio.gather(*tasks)

        print("Extracting report data...")
        for link, date in link_date_map.items():
            file_path = f"downloads/{date}.xls"
            report_data = extract_report_data(file_path)
            for item in report_data:
                item["date"] = date
                item["created_on"] = datetime.now()
                item["updated_on"] = datetime.now()
            all_data.extend(report_data)
    return all_data
