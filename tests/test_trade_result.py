import pytest
from httpx import AsyncClient
from datetime import date, datetime
from fastapi import status

from app.api.schemas.trade_result_schemas import (
    TradeResultsResponse,
    TradeResultsRequest,
)
from app.api.models import TradeResult
from app.database import async_session_maker
from sqlalchemy import insert


@pytest.mark.asyncio
async def test_get_trading_results(ac: AsyncClient, fastapi_cache):
    test_date = date(2024, 7, 1)
    async with async_session_maker() as session:
        stmt = insert(TradeResult).values(
            exchange_product_id="TEST001",
            exchange_product_name="Test Product",
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

    trade_results_request = {
        "oil_id": "OIL001",
        "delivery_type_id": "TYPE001",
        "delivery_basis_id": "BASIS001",
        "limit": 10,
    }

    response = await ac.post("/api/v1/trading_results", json=trade_results_request)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "data" in data

    trade_results_response = TradeResultsResponse(**data)
    assert len(trade_results_response.data) > 0

    first_result = trade_results_response.data[0]
    assert first_result.exchange_product_id == "TEST001"
    assert first_result.exchange_product_name == "Test Product"
    assert first_result.oil_id == "OIL001"
    assert first_result.delivery_basis_id == "BASIS001"
    assert first_result.delivery_type_id == "TYPE001"
    assert first_result.volume == 1000.0
    assert first_result.total == 100000.0
    assert first_result.count == 100
    assert first_result.date == datetime(test_date.year, test_date.month, test_date.day)


@pytest.mark.asyncio
async def test_get_trading_results_error(ac: AsyncClient, fastapi_cache):
    invalid_request = {
        "oil_id": "INVALID",
        "delivery_type_id": "INVALID",
        "delivery_basis_id": "INVALID",
        "limit": "invalid_limit",
    }

    response = await ac.post("/api/v1/trading_results", json=invalid_request)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_trading_results_empty(ac: AsyncClient, fastapi_cache):
    empty_request = {
        "oil_id": "NONEXISTENT",
        "delivery_type_id": "NONEXISTENT",
        "delivery_basis_id": "NONEXISTENT",
        "limit": 10,
    }

    response = await ac.post("/api/v1/trading_results", json=empty_request)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "data" in data
    assert len(data["data"]) == 0
