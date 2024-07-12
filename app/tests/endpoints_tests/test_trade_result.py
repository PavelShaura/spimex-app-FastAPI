import pytest
from httpx import AsyncClient
from datetime import datetime

from fastapi import status, HTTPException
from sqlalchemy import insert

from app.api.api_services.trade_result_service import GetTradingResultsService
from app.api.schemas.trade_result_schemas import TradeResultsResponse
from app.api.models import TradeResult
from app.database import async_session_maker


@pytest.mark.usefixtures("fastapi_cache")
class TestTradeResult:
    @pytest.mark.asyncio(scope="session")
    async def test_get_trading_results(self, ac: AsyncClient, trade_result_test_data):
        test_data, expected_count = trade_result_test_data
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
    async def test_get_trading_results_error(
        self, ac: AsyncClient, invalid_trade_result_request
    ):
        invalid_request, expected_status = invalid_trade_result_request
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
