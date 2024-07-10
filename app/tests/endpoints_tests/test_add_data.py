from datetime import date, datetime

import pytest
from sqlalchemy import insert, select

from app.api.models import TradeResult
from app.tests.conftest import async_session_maker


@pytest.mark.usefixtures("fastapi_cache")
class TestTradeResultModel:
    @pytest.mark.asyncio(scope="session")
    @pytest.mark.parametrize(
        "test_data",
        [
            {
                "exchange_product_id": "DT50SUR065F",
                "exchange_product_name": "ДТ вид 4 (ДТ-А-К5) минус 50, ст. Сургут (ст. отправления)",
                "oil_id": None,
                "delivery_basis_id": None,
                "delivery_type_id": "F",
                "volume": 1000.0,
                "total": 100000.0,
                "count": 100,
                "date": date(2024, 7, 1),
            },
            {
                "exchange_product_id": "AI92REG066F",
                "exchange_product_name": "АИ-92 (АИ-92-К5), ст. Регион (ст. отправления)",
                "oil_id": "OIL002",
                "delivery_basis_id": "BASIS002",
                "delivery_type_id": "F",
                "volume": 2000.0,
                "total": 200000.0,
                "count": 200,
                "date": date(2024, 7, 2),
            },
        ],
    )
    async def test_add_data(self, test_data: dict):
        async with async_session_maker() as session:
            stmt = insert(TradeResult).values(**test_data)
            await session.execute(stmt)
            await session.commit()

            query = select(TradeResult).where(
                TradeResult.exchange_product_id == test_data["exchange_product_id"]
            )
            result = await session.execute(query)
            inserted_trade_result = result.scalar_one()

            for key, value in test_data.items():
                if key == "date":
                    assert getattr(inserted_trade_result, key) == datetime.combine(
                        value, datetime.min.time()
                    )
                else:
                    assert getattr(inserted_trade_result, key) == value

    @pytest.mark.asyncio(scope="session")
    async def test_add_invalid_data(self):
        async with async_session_maker() as session:
            invalid_data = {
                "exchange_product_id": "INVALID",
                "exchange_product_name": "Invalid Product",
                "oil_id": "INVALID",
                "delivery_basis_id": "INVALID",
                "delivery_type_id": "INVALID",
                "volume": "invalid_volume",
                "total": "invalid_total",
                "count": "invalid_count",
                "date": "invalid_date",
            }

            stmt = insert(TradeResult).values(**invalid_data)

            with pytest.raises(Exception):

                await session.execute(stmt)
                await session.commit()
