from datetime import date
from unittest.mock import MagicMock, AsyncMock

import pytest

from app.utils.parser.save_data import save_data_to_db
from app.api.models import TradeResult
from app.api.unit_of_work import UnitOfWork


class TestSaveData:
    @pytest.mark.asyncio(scope="session")
    async def test_save_data_to_db(self, mocker):
        mock_uow = MagicMock(spec=UnitOfWork)
        mock_repo = AsyncMock()
        mock_uow.trade_result_repository = mock_repo

        test_data = [
            {
                "exchange_product_id": "PROD001BASE1",
                "exchange_product_name": "Product 1",
                "delivery_basis_name": "Base 1",
                "volume": 100.0,
                "total": 1000000.0,
                "count": 10,
                "date": date(2024, 7, 1),
            }
        ]

        await save_data_to_db(test_data, mock_uow)

        mock_repo.add.assert_called_once()
        called_with = mock_repo.add.call_args[0][0]

        assert isinstance(called_with, TradeResult)

        expected_values = {
            "exchange_product_id": "PROD001BASE1",
            "exchange_product_name": "Product 1",
            "oil_id": "PROD",
            "delivery_basis_id": "001",
            "delivery_basis_name": "Base 1",
            "delivery_type_id": "1",
            "volume": 100.0,
            "total": 1000000.0,
            "count": 10,
            "date": date(2024, 7, 1),
        }

        for attr, expected_value in expected_values.items():
            assert (
                getattr(called_with, attr) == expected_value
            ), f"Unexpected value for {attr}"

    @pytest.mark.asyncio(scope="session")
    async def test_save_data_to_db_error(self, mocker):
        mock_uow = mocker.Mock(spec=UnitOfWork)
        mock_repo = mocker.Mock()
        mock_uow.trade_result_repository = mock_repo
        mock_repo.add.side_effect = Exception("Database error")

        test_data = [
            {
                "exchange_product_id": "PROD001BASE1",
                "exchange_product_name": "Product 1",
                "delivery_basis_name": "Base 1",
                "volume": 100.0,
                "total": 1000000.0,
                "count": 10,
                "date": "2024-07-01",
            }
        ]

        with pytest.raises(Exception, match="Database error"):
            await save_data_to_db(test_data, mock_uow)
