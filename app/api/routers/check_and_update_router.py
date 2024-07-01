from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.repository import TradeResultRepository
from app.api.scemas.check_and_update_scemas import CheckAndUpdateResponse
from app.api.scemas.error_scemas import ErrorResponse
from parser.save_data import save_data_to_db
from parser.scrapping import scrape_reports
from app.database import get_async_session


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
    start: int, end: int, session: AsyncSession = Depends(get_async_session)
):
    try:
        rp = TradeResultRepository(session)
        last_report_date = await rp.get_last_report_date()
        if isinstance(last_report_date, datetime):
            last_report_date = last_report_date.date()
        new_data = await scrape_reports(start, end, last_report_date)
        if new_data:
            await save_data_to_db(new_data)
            return CheckAndUpdateResponse(
                data=new_data, details=f"Added {len(new_data)} new reports"
            )
        else:
            return CheckAndUpdateResponse(data=None, details="No new reports to add")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=ErrorResponse(details=f"error {e}").dict()
        )
