from contextlib import asynccontextmanager
from app.database import get_async_session
from app.api.repository import TradeResultRepository
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.base_repository import BaseRepository


class UnitOfWork:
    """
    Инициализирует класс UnitOfWork с фабрикой асинхронных сессий.
    """

    def __init__(self):
        self.session_factory = get_async_session

    @asynccontextmanager
    async def __call__(self) -> "UnitOfWork":
        """
        Асинхронный контекстный менеджер для открытия сессии и инициализации репозиториев.

        Возвращает:
        - UnitOfWork: Объект текущего класса.
        """
        async with self.session_factory() as session:
            self.session: AsyncSession = session
            self.trade_result_repository: BaseRepository = TradeResultRepository(self.session)
            try:
                yield self
                await self.session.commit()
            except Exception:
                await self.session.rollback()
                raise
            finally:
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


async def get_uow():
    uow = UnitOfWork()
    async with uow() as unit_of_work:
        yield unit_of_work