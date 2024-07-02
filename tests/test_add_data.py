from datetime import date

from sqlalchemy import insert, select

from app.api.models import TradeResult
from tests.conftest import async_session_maker


async def test_add_data():
    async with async_session_maker() as session:
        stmt = insert(TradeResult).values(
            exchange_product_id="DT50SUR065F",
            exchange_product_name="ДТ вид 4 (ДТ-А-К5) минус 50, ст. Сургут (ст. отправления)",
            oil_id=None,
            delivery_basis_id=None,
            delivery_type_id="F",
            volume=1000.0,
            total=100000.0,
            count=100,
            date=date(2024, 7, 1),
        )
        await session.execute(stmt)
        await session.commit()

        query = select(TradeResult).limit(1)
        result = await session.execute(query)
        inserted_trade_result = result.scalar_one()

        assert inserted_trade_result.exchange_product_id == "DT50SUR065F"
        assert (
            inserted_trade_result.exchange_product_name
            == "ДТ вид 4 (ДТ-А-К5) минус 50, ст. Сургут (ст. отправления)"
        )
        assert inserted_trade_result.oil_id is None
        assert inserted_trade_result.delivery_basis_id is None
        assert inserted_trade_result.delivery_type_id == "F"
        assert inserted_trade_result.volume == 1000.0
