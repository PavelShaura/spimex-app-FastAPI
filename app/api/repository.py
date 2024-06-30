from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from app.api.models import TradeResult


class TradeResultRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_last_report_date(self) -> int:
        result = await self.session.execute(select(func.max(TradeResult.date)))
        last_date = result.scalar()
        return last_date.date() if last_date else None
