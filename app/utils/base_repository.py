from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def get_last_report_date(self):
        pass

    @abstractmethod
    async def delete_trade_results(self, date_from, date_to):
        pass

    @abstractmethod
    async def get_last_trading_dates(self, limit):
        pass

    @abstractmethod
    async def get_dynamics(self, **kwargs):
        pass

    @abstractmethod
    async def add(self, entity):
        pass

    @abstractmethod
    async def get_trading_results(self, **kwargs):
        pass
