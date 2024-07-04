from fastapi import APIRouter, Query, HTTPException, Depends
from fastapi_cache.decorator import cache
from typing import Annotated

from app.api.schemas.error_schemas import ErrorResponse
from app.api.schemas.last_trading_dates_schemas import LastTradingDatesResponse
from app.api.unit_of_work import UnitOfWork, get_uow
from app.api.api_services.last_trading_dates_service import LastTradingDatesService

last_trading_dates_router = APIRouter(prefix="/api/v1", tags=["API_SPIMEX"])


@last_trading_dates_router.get(
    "/last_trading_dates",
    response_model=LastTradingDatesResponse,
    responses={500: {"model": ErrorResponse}},
)
@cache(expire=60 * 60 * 24)
async def get_last_trading_dates(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    limit: int = Query(default=10, ge=1, le=100),
) -> LastTradingDatesResponse:
    """
    Получает последние даты торгов с ограничением на количество возвращаемых дат.
    """
    try:
        return await LastTradingDatesService()(uow, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=ErrorResponse(details=f"error {e}").dict()
        )
