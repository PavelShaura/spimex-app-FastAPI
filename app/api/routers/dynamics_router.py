from fastapi import APIRouter, HTTPException, Body, Depends
from fastapi_cache.decorator import cache
from typing import Annotated

from app.api.scemas.dynamics_scemas import DynamicsResponse, DynamicsRequest
from app.api.scemas.error_scemas import ErrorResponse
from app.api.unit_of_work import UnitOfWork, get_uow
from app.api.api_services.dynamics_service import DynamicsService

dynamics_router = APIRouter(prefix="/api/v1", tags=["API_SPIMEX"])


@dynamics_router.post(
    "/dynamics",
    response_model=DynamicsResponse,
    responses={500: {"model": ErrorResponse}},
)
@cache(expire=60 * 60 * 24)
async def get_dynamics(
    dynamics_request: Annotated[DynamicsRequest, Body()],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> DynamicsResponse:
    """
    Получает динамику данных для указанных параметров.
    """
    try:
        return await DynamicsService()(uow, dynamics_request=dynamics_request)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=ErrorResponse(details=f"error {e}").dict()
        )
