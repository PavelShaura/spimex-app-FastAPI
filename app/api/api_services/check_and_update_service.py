from datetime import datetime
from typing import Any, Optional

from app.services.base_service import BaseService
from app.api.unit_of_work import UnitOfWork
from app.api.scemas.check_and_update_scemas import CheckAndUpdateResponse
from parser.scrapping import scrape_reports
from parser.save_data import save_data_to_db


class CheckAndUpdateService(BaseService):
    async def execute(self, uow: UnitOfWork, **kwargs) -> CheckAndUpdateResponse:
        start = kwargs.get("start")
        end = kwargs.get("end")
        async with uow:
            last_report_date = await self._get_last_report_date(uow)
            new_data = await self._scrape_new_reports(start, end, last_report_date)
            if new_data:
                await self._save_new_data(new_data, uow)
                await uow.commit()
                return CheckAndUpdateResponse(
                    data=new_data, details=f"Added {len(new_data)} new reports"
                )
            else:
                return CheckAndUpdateResponse(data="No new reports to add")

    async def _get_last_report_date(self, uow: UnitOfWork) -> Optional[datetime.date]:
        last_report_date = await uow.trade_result_repository.get_last_report_date()
        if isinstance(last_report_date, datetime):
            return last_report_date.date()
        return last_report_date

    async def _scrape_new_reports(
        self, start: int, end: int, last_report_date: Optional[datetime.date]
    ) -> Any:
        return await scrape_reports(start, end, last_report_date)

    async def _save_new_data(self, new_data: Any, uow: UnitOfWork) -> None:
        await save_data_to_db(new_data, uow)
