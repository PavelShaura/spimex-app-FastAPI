from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, delete

from app.api.models import TradeResult


class TradeResultRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_last_report_date(self) -> int:
        result = await self.session.execute(select(func.max(TradeResult.date)))
        last_date = result.scalar()
        return last_date.date() if last_date else None

    async def delete_trade_results(self, date_from: date, date_to: date) -> int:
        stmt = (
            delete(TradeResult)
            .where(TradeResult.date >= date_from)
            .where(TradeResult.date <= date_to)
        )
        result = await self.session.execute(stmt)
        return len(result.all())
