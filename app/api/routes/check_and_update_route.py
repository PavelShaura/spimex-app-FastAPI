from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.repository import TradeResultRepository
from app.parser.save_data import save_data_to_db
from app.parser.scrapping import scrape_reports
from app.database import get_async_session

check_and_update_router = APIRouter(prefix="/api/v1/check_and_update", tags=["API"])


@check_and_update_router.get("/")
async def check_and_update_data(
    start: int, end: int, session: AsyncSession = Depends(get_async_session)
):
    rp = TradeResultRepository(session)
    last_report_date = await rp.get_last_report_date()
    if isinstance(last_report_date, datetime):
        last_report_date = last_report_date.date()
    new_data = await scrape_reports(start, end, last_report_date)
    if new_data:
        await save_data_to_db(new_data)
        return {"message": f"Added {len(new_data)} new reports"}
    else:
        return {"message": "No new reports to add"}
