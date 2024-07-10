import pytest
from httpx import AsyncClient
from datetime import date, datetime

from fastapi import status, HTTPException
from sqlalchemy import insert

from app.api.api_services.dynamics_service import DynamicsService
from app.api.schemas.dynamics_schemas import DynamicsResponse
from app.api.models import TradeResult
from app.database import async_session_maker


@pytest.mark.usefixtures("fastapi_cache")
class TestDynamics:
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
    async def test_get_dynamics(
        self, ac: AsyncClient, test_data: dict, expected_count: int
    ):
        async with async_session_maker() as session:
            stmt = insert(TradeResult).values(**test_data)
            await session.execute(stmt)
            await session.commit()

        dynamics_request = {
            "oil_id": test_data["oil_id"],
            "delivery_type_id": test_data["delivery_type_id"],
            "delivery_basis_id": test_data["delivery_basis_id"],
            "start_date": test_data["date"].isoformat(),
            "end_date": test_data["date"].isoformat(),
        }

        response = await ac.post("/api/v1/dynamics", json=dynamics_request)

        assert response.status_code == status.HTTP_200_OK

        dynamics_response = DynamicsResponse(**response.json())
        assert len(dynamics_response.data) == expected_count

        first_result = dynamics_response.data[0]
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
                    "start_date": "invalid_date",
                    "end_date": "invalid_date",
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            ),
            (
                {
                    "oil_id": "OIL001",
                    "delivery_type_id": "TYPE001",
                    "delivery_basis_id": "BASIS001",
                    "start_date": "2024-07-01",
                    "end_date": "2024-06-30",
                },
                status.HTTP_200_OK,
            ),
        ],
    )
    async def test_get_dynamics_error(
        self, ac: AsyncClient, invalid_request: dict, expected_status: int
    ):
        response = await ac.post("/api/v1/dynamics", json=invalid_request)
        assert response.status_code == expected_status

    @pytest.mark.asyncio(scope="session")
    async def test_get_dynamics_empty(self, ac: AsyncClient):
        async with async_session_maker() as session:
            await session.execute(TradeResult.__table__.delete())
            await session.commit()

        dynamics_request = {
            "oil_id": "NONEXISTENT",
            "delivery_type_id": "NONEXISTENT",
            "delivery_basis_id": "NONEXISTENT",
            "start_date": "2024-07-01",
            "end_date": "2024-07-01",
        }

        response = await ac.post("/api/v1/dynamics", json=dynamics_request)

        assert response.status_code == status.HTTP_200_OK
        dynamics_response = DynamicsResponse(**response.json())
        assert len(dynamics_response.data) == 0

    @pytest.mark.asyncio(scope="session")
    async def test_get_dynamics_mock(self, ac: AsyncClient, mocker):
        mock_execute = mocker.patch.object(DynamicsService, "execute")
        mock_execute.side_effect = HTTPException(
            status_code=500,
            detail={"status": "error", "details": "Internal Server Error"},
        )

        dynamics_request = {
            "oil_id": "OIL001",
            "delivery_type_id": "TYPE001",
            "delivery_basis_id": "BASIS001",
            "start_date": "2024-07-01",
            "end_date": "2024-07-01",
        }

        response = await ac.post("/api/v1/dynamics", json=dynamics_request)

        assert response.status_code == 500
        assert response.json()["detail"]["status"] == "error"
        assert (
            response.json()["detail"]["details"]
            == "error 500: {'status': 'error', 'details': 'Internal Server Error'}"
        )
