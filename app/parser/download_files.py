import os

from aiohttp import ClientSession
from datetime import date


async def download_file(
    session: ClientSession, url: str, report_date: date, folder: str = "downloads"
) -> None:
    """
    Загружает файл по указанному URL и сохраняет его в указанную папку с названием на основе даты.

    :param session: Асинхронная сессия для выполнения HTTP-запросов.
    :param url: URL файла для загрузки.
    :param report_date: Дата для включения в имя файла.
    :param folder: Папка для сохранения загруженного файла. По умолчанию "downloads".
    """
    os.makedirs(folder, exist_ok=True)
    filename = f"{folder}/{report_date}.xls"
    print(f"Downloading file: {filename} from {url}")
    async with session.get(url) as response:
        if response.status == 200:
            content = await response.read()
            with open(filename, "wb") as f:
                f.write(content)
            print(f"Successfully downloaded {filename}")
        else:
            print(f"Failed to download {url}: HTTP {response.status}")
