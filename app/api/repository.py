from datetime import date
from typing import List, Optional, Dict, Any

from sqlalchemy import select, func, delete

from app.api.models import TradeResult
from app.utils.base_repository import BaseRepository


class TradeResultRepository(BaseRepository):
    """
    Репозиторий для работы с результатами торгов.

    Предоставляет методы для получения и удаления данных о торгах,
    а также для добавления новых записей и получения динамики торгов.
    """

    async def add(self, trade_result: TradeResult):
        self.session.add(trade_result)

    async def read(self, id: Any) -> Optional[TradeResult]:
        result = await self.session.execute(select(TradeResult).filter_by(id=id))
        return result.scalar_one_or_none()

    async def update(self, trade_result: TradeResult) -> TradeResult:
        await self.session.merge(trade_result)
        await self.session.flush()
        return trade_result

    async def delete(self, id: Any) -> bool:
        result = await self.session.execute(
            delete(TradeResult).where(TradeResult.id == id)
        )
        return result.rowcount > 0

    async def list(self, **kwargs) -> List[TradeResult]:
        query = select(TradeResult)
        for key, value in kwargs.items():
            if value is not None:
                query = query.filter(getattr(TradeResult, key) == value)
        result = await self.session.execute(query)
        return result.scalars().all()

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

        filters: Dict[str, Optional[str]] = {
            "oil_id": oil_id,
            "delivery_type_id": delivery_type_id,
            "delivery_basis_id": delivery_basis_id,
        }

        for column, value in filters.items():
            if value:
                query = query.where(getattr(TradeResult, column) == value)

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

        filters: Dict[str, Optional[str]] = {
            "oil_id": oil_id,
            "delivery_type_id": delivery_type_id,
            "delivery_basis_id": delivery_basis_id,
        }

        for column, value in filters.items():
            if value:
                query = query.where(getattr(TradeResult, column) == value)

        query = query.order_by(TradeResult.date.desc()).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()
