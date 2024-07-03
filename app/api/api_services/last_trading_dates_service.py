from typing import List
from datetime import date

from app.utils.base_service import BaseService
from app.api.unit_of_work import UnitOfWork
from app.api.scemas.last_trading_dates_scemas import LastTradingDatesResponse
from app.utils.base_repository import BaseRepository


class LastTradingDatesService(BaseService):
    async def execute(self, uow: UnitOfWork, **kwargs) -> LastTradingDatesResponse:
        limit = kwargs.get("limit", 10)
        async with uow:
            dates = await self._get_last_trading_dates(uow.trade_result_repository, limit)
            return LastTradingDatesResponse(data=dates)

    async def _get_last_trading_dates(self, repository: BaseRepository, limit: int) -> List[date]:
        return await repository.get_last_trading_dates(limit)
