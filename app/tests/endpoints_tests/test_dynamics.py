import pytest
from httpx import AsyncClient
from datetime import datetime

from fastapi import status, HTTPException
from sqlalchemy import insert

from app.api.api_services.dynamics_service import DynamicsService
from app.api.schemas.dynamics_schemas import DynamicsResponse
from app.api.models import TradeResult
from app.database import async_session_maker


@pytest.mark.usefixtures("fastapi_cache")
class TestDynamics:
    @pytest.mark.asyncio(scope="session")
    async def test_get_dynamics(self, ac: AsyncClient, dynamics_test_data):
        async with async_session_maker() as session:
            stmt = insert(TradeResult).values(**dynamics_test_data)
            await session.execute(stmt)
            await session.commit()

        dynamics_request = {
            "oil_id": dynamics_test_data["oil_id"],
            "delivery_type_id": dynamics_test_data["delivery_type_id"],
            "delivery_basis_id": dynamics_test_data["delivery_basis_id"],
            "start_date": dynamics_test_data["date"].isoformat(),
            "end_date": dynamics_test_data["date"].isoformat(),
        }

        response = await ac.post("/api/v1/dynamics", json=dynamics_request)

        assert response.status_code == status.HTTP_200_OK

        dynamics_response = DynamicsResponse(**response.json())
        assert len(dynamics_response.data) == 1

        first_result = dynamics_response.data[0]
        for key, value in dynamics_test_data.items():
            if key == "date":
                assert getattr(first_result, key) == datetime.combine(
                    value, datetime.min.time()
                )
            else:
                assert getattr(first_result, key) == value

    @pytest.mark.asyncio(scope="session")
    async def test_get_dynamics_error(self, ac: AsyncClient, invalid_dynamics_data):
        invalid_request, expected_status = invalid_dynamics_data
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
