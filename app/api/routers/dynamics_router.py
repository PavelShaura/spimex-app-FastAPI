from fastapi import APIRouter, HTTPException, Body
from fastapi_cache.decorator import cache

from app.api.scemas.dynamics_scemas import DynamicsResponse, DynamicsRequest
from app.api.scemas.error_scemas import ErrorResponse
from app.api.unit_of_work import UnitOfWork


dynamics_router = APIRouter(prefix="/api/v1", tags=["API_SPIMEX"])


@dynamics_router.post(
    "/dynamics",
    response_model=DynamicsResponse,
    responses={500: {"model": ErrorResponse}},
)
@cache(expire=60 * 60 * 24)
async def get_dynamics(dynamics_request: DynamicsRequest):
    try:
        async with UnitOfWork() as uow:
            results = await uow.trade_result_repository.get_dynamics(
                oil_id=dynamics_request.oil_id,
                delivery_type_id=dynamics_request.delivery_type_id,
                delivery_basis_id=dynamics_request.delivery_basis_id,
                start_date=dynamics_request.start_date,
                end_date=dynamics_request.end_date,
            )
        return DynamicsResponse(data=results)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=ErrorResponse(details=f"error {e}").dict()
        )
