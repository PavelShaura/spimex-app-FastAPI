from datetime import datetime

import pytest
from sqlalchemy import insert, select

from app.api.models import TradeResult
from app.tests.conftest import async_session_maker


@pytest.mark.usefixtures("fastapi_cache")
class TestTradeResultModel:
    @pytest.mark.asyncio(scope="session")
    async def test_add_data(self, trade_result_test_add_data):
        async with async_session_maker() as session:
            stmt = insert(TradeResult).values(**trade_result_test_add_data)
            await session.execute(stmt)
            await session.commit()

            query = select(TradeResult).where(
                TradeResult.exchange_product_id
                == trade_result_test_add_data["exchange_product_id"]
            )
            result = await session.execute(query)
            inserted_trade_result = result.scalar_one()

            for key, value in trade_result_test_add_data.items():
                if key == "date":
                    assert getattr(inserted_trade_result, key) == datetime.combine(
                        value, datetime.min.time()
                    )
                else:
                    assert getattr(inserted_trade_result, key) == value

    @pytest.mark.asyncio(scope="session")
    async def test_add_invalid_data(self, invalid_trade_result_data):
        async with async_session_maker() as session:
            stmt = insert(TradeResult).values(**invalid_trade_result_data)

            with pytest.raises(Exception):
                await session.execute(stmt)
                await session.commit()
