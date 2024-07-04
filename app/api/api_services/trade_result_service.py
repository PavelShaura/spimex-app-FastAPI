from typing import List, Optional

from app.api.models import TradeResult
from app.api.unit_of_work import UnitOfWork
from app.utils.base_service import BaseService
from app.utils.base_repository import BaseRepository


class GetTradingResultsService(BaseService):
    """
    Сервис для получения результатов торгов.

    Предоставляет методы для выполнения основного процесса
    получения результатов торговых данных.
    """

    async def execute(self, uow: UnitOfWork, **kwargs) -> List[TradeResult]:
        oil_id: Optional[str] = kwargs.get("oil_id")
        delivery_type_id: Optional[str] = kwargs.get("delivery_type_id")
        delivery_basis_id: Optional[str] = kwargs.get("delivery_basis_id")
        limit: int = kwargs.get("limit", 10)
        async with uow:
            return await self._get_trading_results(
                uow.trade_result_repository,
                oil_id=oil_id,
                delivery_type_id=delivery_type_id,
                delivery_basis_id=delivery_basis_id,
                limit=limit,
            )

    async def _get_trading_results(
        self,
        repository: BaseRepository,
        oil_id: Optional[str] = None,
        delivery_type_id: Optional[str] = None,
        delivery_basis_id: Optional[str] = None,
        limit: int = 10,
    ) -> List[TradeResult]:
        return await repository.get_trading_results(
            oil_id=oil_id,
            delivery_type_id=delivery_type_id,
            delivery_basis_id=delivery_basis_id,
            limit=limit,
        )
