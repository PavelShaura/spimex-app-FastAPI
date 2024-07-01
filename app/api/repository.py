from datetime import date
from typing import List, Optional
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
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

    async def get_last_trading_dates(self, limit: int) -> List[date]:
        query = (
            select(TradeResult.date)
            .distinct()
            .order_by(TradeResult.date.desc())
            .limit(limit)
        )
        result = await self.session.execute(query)
        return [row[0].date() for row in result.fetchall()]

    async def get_dynamics(
        self,
        oil_id: Optional[str] = None,
        delivery_type_id: Optional[str] = None,
        delivery_basis_id: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[TradeResult]:
        query = select(TradeResult)
        if oil_id:
            query = query.where(TradeResult.oil_id == oil_id)
        if delivery_type_id:
            query = query.where(TradeResult.delivery_type_id == delivery_type_id)
        if delivery_basis_id:
            query = query.where(TradeResult.delivery_basis_id == delivery_basis_id)
        if start_date:
            query = query.where(TradeResult.date >= start_date)
        if end_date:
            query = query.where(TradeResult.date <= end_date)
        query = query.order_by(TradeResult.date.desc())
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_trading_results(
        self,
        oil_id: Optional[str] = None,
        delivery_type_id: Optional[str] = None,
        delivery_basis_id: Optional[str] = None,
        limit: int = 10,
    ) -> List[TradeResult]:
        query = select(TradeResult)
        if oil_id:
            query = query.where(TradeResult.oil_id == oil_id)
        if delivery_type_id:
            query = query.where(TradeResult.delivery_type_id == delivery_type_id)
        if delivery_basis_id:
            query = query.where(TradeResult.delivery_basis_id == delivery_basis_id)
        query = query.order_by(TradeResult.date.desc()).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()
