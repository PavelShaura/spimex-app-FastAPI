from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi_cache.decorator import cache
from typing import Annotated

from app.api.schemas.error_schemas import ErrorResponse
from app.api.schemas.trade_result_schemas import TradeResultsResponse, TradeResultsRequest
from app.api.unit_of_work import UnitOfWork, get_uow
from app.api.api_services.trade_result_service import GetTradingResultsService

trade_result_router = APIRouter(prefix="/api/v1", tags=["API_SPIMEX"])


@trade_result_router.post(
    "/trading_results",
    response_model=TradeResultsResponse,
    responses={500: {"model": ErrorResponse}},
)
@cache(expire=60 * 60 * 24)
async def get_trading_results(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    trade_results_request: Annotated[TradeResultsRequest, Body()],
) -> TradeResultsResponse:
    """
    Получает результаты торгов.
    """
    try:
        results = await GetTradingResultsService()(
            uow,
            oil_id=trade_results_request.oil_id,
            delivery_type_id=trade_results_request.delivery_type_id,
            delivery_basis_id=trade_results_request.delivery_basis_id,
            limit=trade_results_request.limit,
        )
        return TradeResultsResponse(data=results)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=str(ErrorResponse(details=f"error {e}"))
        )
