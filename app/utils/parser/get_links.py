from typing import List, Tuple
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from datetime import datetime, date


async def fetch_page(session: ClientSession, url: str) -> str:
    """
    Загружает HTML-страницу по указанному URL.

    :param session: Асинхронная сессия для выполнения HTTP-запросов.
    :param url: URL страницы для загрузки.
    :return: HTML содержимое страницы.
    """
    print(f"Fetching page: {url}")
    async with session.get(url) as response:
        return await response.text()


async def get_report_links(page_html: str) -> List[Tuple[str, date]]:
    """
    Извлекает ссылки на отчеты и соответствующие даты из HTML-страницы.

    :param page_html: HTML содержимое страницы.
    :return: Список кортежей, содержащих ссылки на отчеты и даты.
    """
    print("Extracting report links and dates...")
    soup = BeautifulSoup(page_html, "html.parser")
    report_links = []
    dates = []
    for item in soup.select(".accordeon-inner__wrap-item"):
        link = item.select_one(".accordeon-inner__item-title.link.xls")
        if link and "files" not in link.get("href").split("/"):
            report_links.append("https://spimex.com" + link.get("href"))
        date_elem = item.select_one(".accordeon-inner__item-inner__title span")
        if date_elem:
            date_str = date_elem.text.strip()
            dates.append(datetime.strptime(date_str, "%d.%m.%Y").date())
    return list(zip(report_links, dates))
