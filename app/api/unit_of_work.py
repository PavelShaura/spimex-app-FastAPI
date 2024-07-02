from app.database import async_session_maker
from app.api.repository import TradeResultRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:
    def __init__(self):
        """
        Инициализирует класс UnitOfWork с фабрикой асинхронных сессий.
        """
        self.session_factory = async_session_maker

    async def __aenter__(self) -> "UnitOfWork":
        """
        Асинхронный контекстный менеджер для открытия сессии и инициализации репозиториев.

        Возвращает:
        - UnitOfWork: Объект текущего класса.
        """
        self.session: AsyncSession = self.session_factory()
        self.trade_result_repository = TradeResultRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Асинхронный контекстный менеджер для закрытия сессии.

        Параметры:
        - exc_type: Тип исключения.
        - exc_val: Значение исключения.
        - exc_tb: Трассировка стека исключения.
        """
        await self.session.close()

    async def commit(self):
        """
        Асинхронно фиксирует (коммитит) текущую транзакцию.
        """
        await self.session.commit()

    async def rollback(self):
        """
        Асинхронно откатывает (rollback) текущую транзакцию.
        """
        await self.session.rollback()
