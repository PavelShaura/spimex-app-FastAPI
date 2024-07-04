from typing import List

from app.utils.base_repository import BaseRepository
from app.utils.base_service import BaseService
from app.api.unit_of_work import UnitOfWork
from app.api.schemas.dynamics_schemas import DynamicsResponse, DynamicsRequest
from app.api.models import TradeResult


class DynamicsService(BaseService):
    """
    Сервис для получения динамики торгов.

    Предоставляет методы для выполнения основного процесса
    получения динамики торговых данных.
    """
    async def execute(self, uow: UnitOfWork, **kwargs) -> DynamicsResponse:
        dynamics_request: DynamicsRequest = kwargs.get("dynamics_request")
        async with uow:
            results = await self._get_dynamics(
                uow.trade_result_repository, dynamics_request
            )
            return DynamicsResponse(data=results)

    async def _get_dynamics(
        self, repository: BaseRepository, dynamics_request: DynamicsRequest
    ) -> List[TradeResult]:
        return await repository.get_dynamics(
            oil_id=dynamics_request.oil_id,
            delivery_type_id=dynamics_request.delivery_type_id,
            delivery_basis_id=dynamics_request.delivery_basis_id,
            start_date=dynamics_request.start_date,
            end_date=dynamics_request.end_date,
        )
