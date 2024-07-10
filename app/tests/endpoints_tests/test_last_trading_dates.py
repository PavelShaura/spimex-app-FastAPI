import pytest
from httpx import AsyncClient
from datetime import date, timedelta

from fastapi import status, HTTPException
from sqlalchemy import insert

from app.api.schemas.last_trading_dates_schemas import LastTradingDatesResponse
from app.api.models import TradeResult
from app.database import async_session_maker
from app.api.api_services.last_trading_dates_service import LastTradingDatesService


@pytest.mark.usefixtures("fastapi_cache")
class TestLastTradingDates:
    @pytest.mark.asyncio(scope="session")
    @pytest.mark.parametrize(
        "test_data,expected_count,limit",
        [
            (
                [date(2024, 7, 1) - timedelta(days=i) for i in range(5)],
                3,
                3,
            ),
            (
                [date(2024, 7, 1) - timedelta(days=i) for i in range(10)],
                5,
                5,
            ),
        ],
    )
    async def test_get_last_trading_dates(
        self, ac: AsyncClient, test_data: list, expected_count: int, limit: int
    ):
        async with async_session_maker() as session:
            for test_date in test_data:
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

        response = await ac.get(f"/api/v1/last_trading_dates?limit={limit}")

        assert response.status_code == status.HTTP_200_OK

        last_trading_dates_response = LastTradingDatesResponse(**response.json())
        assert len(last_trading_dates_response.data) == expected_count

        for i, response_date in enumerate(last_trading_dates_response.data):
            expected_date = test_data[i]
            assert response_date == expected_date

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.parametrize(
        "limit,expected_status",
        [
            (0, status.HTTP_422_UNPROCESSABLE_ENTITY),
            (101, status.HTTP_422_UNPROCESSABLE_ENTITY),
            (50, status.HTTP_200_OK),
        ],
    )
    async def test_get_last_trading_dates_limit(
        self, ac: AsyncClient, limit: int, expected_status: int
    ):
        response = await ac.get(f"/api/v1/last_trading_dates?limit={limit}")
        assert response.status_code == expected_status

    @pytest.mark.asyncio(scope="session")
    async def test_get_last_trading_dates_empty(self, ac: AsyncClient):
        async with async_session_maker() as session:
            await session.execute(TradeResult.__table__.delete())
            await session.commit()

        response = await ac.get("/api/v1/last_trading_dates?limit=10")

        assert response.status_code == status.HTTP_200_OK
        last_trading_dates_response = LastTradingDatesResponse(**response.json())
        assert len(last_trading_dates_response.data) == 0

    @pytest.mark.asyncio(scope="session")
    async def test_get_last_trading_dates_mock(self, ac: AsyncClient, mocker):
        mock_execute = mocker.patch.object(LastTradingDatesService, "execute")
        mock_execute.side_effect = HTTPException(
            status_code=500,
            detail={"status": "error", "details": "Internal Server Error"},
        )

        response = await ac.get("/api/v1/last_trading_dates?limit=10")

        assert response.status_code == 500
        assert response.json()["detail"]["status"] == "error"
        assert (
            response.json()["detail"]["details"]
            == "error 500: {'status': 'error', 'details': 'Internal Server Error'}"
        )
