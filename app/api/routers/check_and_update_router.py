from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from app.api.scemas.check_and_update_scemas import CheckAndUpdateResponse
from app.api.scemas.error_scemas import ErrorResponse
from app.api.unit_of_work import UnitOfWork
from parser.scrapping import scrape_reports
from parser.save_data import save_data_to_db

check_and_update_router = APIRouter(
    prefix="/api/v1/check_and_update", tags=["API_SPIMEX"]
)


@check_and_update_router.get(
    "/",
    response_model=CheckAndUpdateResponse,
    responses={500: {"model": ErrorResponse}},
)
@cache(expire=60 * 60 * 24)
async def check_and_update_data(start: int, end: int):
    try:
        async with UnitOfWork() as uow:
            last_report_date = await uow.trade_result_repository.get_last_report_date()
            if isinstance(last_report_date, datetime):
                last_report_date = last_report_date.date()

            new_data = await scrape_reports(start, end, last_report_date)

            if new_data:
                await save_data_to_db(new_data, uow)
                await uow.commit()
                return CheckAndUpdateResponse(
                    data=new_data, details=f"Added {len(new_data)} new reports"
                )
            else:
                return CheckAndUpdateResponse(data="No new reports to add")
    except Exception as e:
        await uow.rollback()
        raise HTTPException(
            status_code=500, detail=ErrorResponse(details=f"error {e}").dict()
        )
