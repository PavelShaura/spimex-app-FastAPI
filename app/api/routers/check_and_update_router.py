from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi_cache.decorator import cache
from typing import Annotated

from app.api.schemas.check_and_update_schemas import CheckAndUpdateResponse
from app.api.schemas.error_schemas import ErrorResponse
from app.api.unit_of_work import UnitOfWork, get_uow
from app.api.api_services.check_and_update_service import CheckAndUpdateService

check_and_update_router = APIRouter(
    prefix="/api/v1/check_and_update", tags=["API_SPIMEX"]
)


@check_and_update_router.get(
    "/",
    response_model=CheckAndUpdateResponse,
    responses={500: {"model": ErrorResponse}},
)
@cache(expire=60 * 60 * 24)
async def check_and_update_data(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    start: Annotated[int, Query(...)],
    end: Annotated[int, Query(...)],
) -> CheckAndUpdateResponse:
    """
    Обновляет данные, проверяя и добавляя новые отчёты.

    Параметры:
    - start (int): Начальная страница для парсинга.
    - end (int): Конечная страница для парсинга.
    """
    try:
        return await CheckAndUpdateService()(uow, start=start, end=end)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=ErrorResponse(details=f"error {e}").dict()
        )
