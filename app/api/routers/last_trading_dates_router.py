from fastapi import APIRouter, Query, HTTPException, Depends
from fastapi_cache.decorator import cache
from typing import Annotated

from app.api.scemas.error_scemas import ErrorResponse
from app.api.scemas.last_trading_dates_scemas import LastTradingDatesResponse
from app.api.unit_of_work import UnitOfWork, get_uow

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
        dates = await uow.trade_result_repository.get_last_trading_dates(limit)
        return LastTradingDatesResponse(data=dates)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=ErrorResponse(details=f"error {e}").dict()
        )
