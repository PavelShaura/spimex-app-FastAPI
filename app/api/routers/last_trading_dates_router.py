from fastapi import APIRouter, Query, HTTPException
from fastapi_cache.decorator import cache

from app.api.scemas.error_scemas import ErrorResponse
from app.api.scemas.last_trading_dates_scemas import LastTradingDatesResponse
from app.api.unit_of_work import UnitOfWork


last_trading_dates_router = APIRouter(prefix="/api/v1", tags=["API_SPIMEX"])


@last_trading_dates_router.get(
    "/last_trading_dates",
    response_model=LastTradingDatesResponse,
    responses={500: {"model": ErrorResponse}},
)
@cache(expire=60 * 60 * 24)
async def get_last_trading_dates(limit: int = Query(default=10, ge=1, le=100)):
    try:
        async with UnitOfWork() as uow:
            dates = await uow.trade_result_repository.get_last_trading_dates(limit)
        return LastTradingDatesResponse(data=dates)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=ErrorResponse(details=f"error {e}").dict()
        )
