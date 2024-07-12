import pytest


@pytest.fixture
def mock_data():
    return [
        ["Единица измерения: Метрическая тонна"],
        [
            "код инструмента",
            "наименование инструмента",
            "базис поставки",
            "объем договоров в единицах измерения",
            "обьем договоров, руб.",
            "количество договоров, шт.",
        ],
        ["PROD001", "Product 1", "Basis 1", "100", "1000000", "10"],
        ["PROD002", "Product 2", "Basis 2", "200", "2000000", "20"],
    ]

@pytest.fixture
def expected_result():
    return [
        {
            "exchange_product_id": "PROD001",
            "exchange_product_name": "Product 1",
            "delivery_basis_name": "Basis 1",
            "volume": 100.0,
            "total": 1000000.0,
            "count": 10,
        },
        {
            "exchange_product_id": "PROD002",
            "exchange_product_name": "Product 2",
            "delivery_basis_name": "Basis 2",
            "volume": 200.0,
            "total": 2000000.0,
            "count": 20,
        },
    ]