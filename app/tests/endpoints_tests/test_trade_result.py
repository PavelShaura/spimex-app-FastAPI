import pytest
from httpx import AsyncClient
from datetime import date, datetime

from fastapi import status, HTTPException
from sqlalchemy import insert

from app.api.api_services.trade_result_service import GetTradingResultsService
from app.api.schemas.trade_result_schemas import TradeResultsResponse
from app.api.models import TradeResult
from app.database import async_session_maker


@pytest.mark.usefixtures("fastapi_cache")
class TestTradeResult:
    @pytest.mark.asyncio(scope="session")
    @pytest.mark.parametrize(
        "test_data,expected_count",
        [
            (
                {
                    "exchange_product_id": "TEST001",
                    "exchange_product_name": "Test Product",
                    "oil_id": "OIL001",
                    "delivery_basis_id": "BASIS001",
                    "delivery_type_id": "TYPE001",
                    "volume": 1000.0,
                    "total": 100000.0,
                    "count": 100,
                    "date": date(2024, 7, 1),
                },
                1,
            ),
            (
                {
                    "exchange_product_id": "TEST002",
                    "exchange_product_name": "Test Product 2",
                    "oil_id": "OIL002",
                    "delivery_basis_id": "BASIS002",
                    "delivery_type_id": "TYPE002",
                    "volume": 2000.0,
                    "total": 200000.0,
                    "count": 200,
                    "date": date(2024, 7, 2),
                },
                1,
            ),
        ],
    )
    async def test_get_trading_results(
        self, ac: AsyncClient, test_data: dict, expected_count: int
    ):
        async with async_session_maker() as session:
            stmt = insert(TradeResult).values(**test_data)
            await session.execute(stmt)
            await session.commit()

        trade_results_request = {
            "oil_id": test_data["oil_id"],
            "delivery_type_id": test_data["delivery_type_id"],
            "delivery_basis_id": test_data["delivery_basis_id"],
            "limit": 10,
        }

        response = await ac.post("/api/v1/trading_results", json=trade_results_request)

        assert response.status_code == status.HTTP_200_OK

        trade_results_response = TradeResultsResponse(**response.json())
        assert len(trade_results_response.data) == expected_count

        first_result = trade_results_response.data[0]
        for key, value in test_data.items():
            if key == "date":
                assert getattr(first_result, key) == datetime.combine(
                    value, datetime.min.time()
                )
            else:
                assert getattr(first_result, key) == value

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.parametrize(
        "invalid_request,expected_status",
        [
            (
                {
                    "oil_id": "INVALID",
                    "delivery_type_id": "INVALID",
                    "delivery_basis_id": "INVALID",
                    "limit": "invalid_limit",
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            ),
            (
                {
                    "oil_id": "OIL001",
                    "delivery_type_id": "TYPE001",
                    "delivery_basis_id": "BASIS001",
                    "limit": -1,
                },
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            ),
        ],
    )
    async def test_get_trading_results_error(
        self, ac: AsyncClient, invalid_request: dict, expected_status: int
    ):
        response = await ac.post("/api/v1/trading_results", json=invalid_request)
        assert response.status_code == expected_status

    @pytest.mark.asyncio(scope="session")
    async def test_get_trading_results_empty(self, ac: AsyncClient):
        async with async_session_maker() as session:
            await session.execute(TradeResult.__table__.delete())
            await session.commit()

        empty_request = {
            "oil_id": "NONEXISTENT",
            "delivery_type_id": "NONEXISTENT",
            "delivery_basis_id": "NONEXISTENT",
            "limit": 10,
        }

        response = await ac.post("/api/v1/trading_results", json=empty_request)

        assert response.status_code == status.HTTP_200_OK
        trade_results_response = TradeResultsResponse(**response.json())
        assert len(trade_results_response.data) == 0

    @pytest.mark.asyncio(scope="session")
    async def test_get_trading_results_mock(self, ac: AsyncClient, mocker):
        mock_execute = mocker.patch.object(GetTradingResultsService, "execute")
        mock_execute.side_effect = HTTPException(
            status_code=500,
            detail={"status": "error", "details": "Internal Server Error"},
        )

        trade_results_request = {
            "oil_id": "OIL001",
            "delivery_type_id": "TYPE001",
            "delivery_basis_id": "BASIS001",
            "limit": 10,
        }

        response = await ac.post("/api/v1/trading_results", json=trade_results_request)

        assert response.status_code == 500
        assert response.json()["detail"]["status"] == "error"
        assert (
            response.json()["detail"]["details"]
            == "error 500: {'status': 'error', 'details': 'Internal Server Error'}"
        )
