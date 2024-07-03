from typing import List, Optional

from app.api.models import TradeResult
from app.api.unit_of_work import UnitOfWork
from app.utils.base_service import BaseService


class GetTradingResultsService(BaseService):
    async def execute(
        self,
        uow: UnitOfWork,
        oil_id: Optional[str] = None,
        delivery_type_id: Optional[str] = None,
        delivery_basis_id: Optional[str] = None,
        limit: int = 10,
    ) -> List[TradeResult]:
        async with uow:
            return await uow.trade_result_repository.get_trading_results(
                oil_id=oil_id,
                delivery_type_id=delivery_type_id,
                delivery_basis_id=delivery_basis_id,
                limit=limit,
            )
