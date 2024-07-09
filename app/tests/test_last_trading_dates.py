from httpx import AsyncClient
from datetime import date, timedelta

import pytest
from fastapi import status

from app.api.schemas.last_trading_dates_schemas import LastTradingDatesResponse
from app.api.models import TradeResult
from app.database import async_session_maker
from sqlalchemy import insert


@pytest.mark.asyncio(scope="session")
async def test_get_last_trading_dates(ac: AsyncClient, fastapi_cache):
    test_dates = [date(2024, 7, 1) - timedelta(days=i) for i in range(5)]
    async with async_session_maker() as session:
        for test_date in test_dates:
            stmt = insert(TradeResult).values(
                exchange_product_id=f"TEST{test_date.day}",
                exchange_product_name=f"Test Product {test_date.day}",
                oil_id="OIL001",
                delivery_basis_id="BASIS001",
                delivery_type_id="TYPE001",
                volume=1000.0,
                total=100000.0,
                count=100,
                date=test_date,
            )
            await session.execute(stmt)
        await session.commit()

    response = await ac.get("/api/v1/last_trading_dates?limit=3")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "data" in data

    last_trading_dates_response = LastTradingDatesResponse(**data)
    assert len(last_trading_dates_response.data) == 3

    for i, response_date in enumerate(last_trading_dates_response.data):
        expected_date = test_dates[i]
        assert response_date == expected_date


@pytest.mark.asyncio(scope="session")
async def test_get_last_trading_dates_limit(ac: AsyncClient, fastapi_cache):
    response_min = await ac.get("/api/v1/last_trading_dates?limit=0")
    assert response_min.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response_max = await ac.get("/api/v1/last_trading_dates?limit=101")
    assert response_max.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response_valid = await ac.get("/api/v1/last_trading_dates?limit=50")
    assert response_valid.status_code == status.HTTP_200_OK


@pytest.mark.asyncio(scope="session")
async def test_get_last_trading_dates_empty(ac: AsyncClient, fastapi_cache):
    async with async_session_maker() as session:
        await session.execute(TradeResult.__table__.delete())
        await session.commit()

    response = await ac.get("/api/v1/last_trading_dates?limit=10")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 0
