from typing import List
from datetime import date

from app.services.base_service import BaseService
from app.api.unit_of_work import UnitOfWork
from app.api.scemas.last_trading_dates_scemas import LastTradingDatesResponse


class LastTradingDatesService(BaseService):
    async def execute(self, uow: UnitOfWork, **kwargs) -> LastTradingDatesResponse:
        limit = kwargs.get("limit", 10)
        async with uow:
            dates = await self._get_last_trading_dates(uow, limit)
            return LastTradingDatesResponse(data=dates)

    async def _get_last_trading_dates(self, uow: UnitOfWork, limit: int) -> List[date]:
        return await uow.trade_result_repository.get_last_trading_dates(limit)
