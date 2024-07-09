from httpx import AsyncClient
from datetime import date, datetime

import pytest
from sqlalchemy import insert
from fastapi import status

from app.api.schemas.dynamics_schemas import DynamicsResponse
from app.api.models import TradeResult
from app.database import async_session_maker



@pytest.mark.asyncio(scope="session")
async def test_get_dynamics(ac: AsyncClient, fastapi_cache):
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

    dynamics_request = {
        "oil_id": "OIL001",
        "delivery_type_id": "TYPE001",
        "delivery_basis_id": "BASIS001",
        "start_date": test_date.isoformat(),
        "end_date": test_date.isoformat(),
    }

    response = await ac.post("/api/v1/dynamics", json=dynamics_request)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "data" in data

    dynamics_response = DynamicsResponse(**data)
    assert len(dynamics_response.data) > 0

    first_result = dynamics_response.data[0]
    assert first_result.exchange_product_id == "TEST001"
    assert first_result.exchange_product_name == "Test Product"
    assert first_result.oil_id == "OIL001"
    assert first_result.delivery_basis_id == "BASIS001"
    assert first_result.delivery_type_id == "TYPE001"
    assert first_result.volume == 1000.0
    assert first_result.total == 100000.0
    assert first_result.count == 100
    assert first_result.date == datetime(test_date.year, test_date.month, test_date.day)


@pytest.mark.asyncio(scope="session")
async def test_get_dynamics_error(ac: AsyncClient, fastapi_cache):
    invalid_request = {
        "oil_id": "INVALID",
        "delivery_type_id": "INVALID",
        "delivery_basis_id": "INVALID",
        "start_date": "invalid_date",
        "end_date": "invalid_date",
    }
    response = await ac.post("/api/v1/dynamics", json=invalid_request)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
