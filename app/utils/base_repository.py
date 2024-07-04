from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import List, Optional, Any


class BaseRepository(ABC):
    """
    Базовый класс репозитория для работы с асинхронной сессией SQLAlchemy.

    Этот класс предоставляет абстрактные методы для работы с данными о торгах.
    """

    def __init__(self, session: AsyncSession):
        """
        Инициализация репозитория с асинхронной сессией.

        Параметры:
            session: Асинхронная сессия SQLAlchemy.
        """
        self.session = session

    @abstractmethod
    async def get_last_report_date(self) -> Optional[date]:
        """
        Получить дату последнего отчета.

        Возвращает:
            Дата последнего отчета или None, если данных нет.
        """
        pass

    @abstractmethod
    async def delete_trade_results(self, date_from: date, date_to: date) -> int:
        """
        Удалить результаты торгов за указанный период.

        Параметры:
            date_from: Дата начала периода.
            date_to: Дата окончания периода.
        """
        pass

    @abstractmethod
    async def get_last_trading_dates(self, limit: int) -> List[date]:
        """
        Получить последние даты торгов.

        Параметры:
            limit: Ограничение на количество возвращаемых дат.

        Возвращает:
            Список последних дат торгов.
        """
        pass

    @abstractmethod
    async def get_dynamics(self, **kwargs: Any) -> List[Any]:
        """
        Получить динамику торгов.

        Параметры:
            kwargs: Дополнительные параметры для фильтрации динамики торгов.

        Возвращает:
            Список динамики торгов.
        """
        pass

    @abstractmethod
    async def add(self, entity: Any) -> None:
        """
        Добавить новый объект в базу данных.

        Параметры:
            entity: Объект для добавления.
        """
        pass

    @abstractmethod
    async def get_trading_results(self, **kwargs: Any) -> List[Any]:
        """
        Получить результаты торгов.

        Параметры:
            kwargs: Дополнительные параметры для фильтрации результатов торгов.

        Возвращает:
            Список результатов торгов.
        """
        pass
