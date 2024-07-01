from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from app.api.scemas.error_scemas import ErrorResponse
from app.api.scemas.trade_result_scemas import TradeResultsResponse, TradeResultsRequest
from app.api.unit_of_work import UnitOfWork

trade_result_router = APIRouter(prefix="/api/v1", tags=["API_SPIMEX"])


@trade_result_router.post(
    "/trading_results",
    response_model=TradeResultsResponse,
    responses={500: {"model": ErrorResponse}},
)
@cache(expire=60 * 60 * 24)
async def get_trading_results(trade_results_request: TradeResultsRequest):
    print(f"Received request: {trade_results_request}")
    try:
        async with UnitOfWork() as uow:
            results = await uow.trade_result_repository.get_trading_results(
                oil_id=trade_results_request.oil_id,
                delivery_type_id=trade_results_request.delivery_type_id,
                delivery_basis_id=trade_results_request.delivery_basis_id,
                limit=trade_results_request.limit,
            )
        return TradeResultsResponse(data=results)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=ErrorResponse(details=f"error {e}").dict()
        )
