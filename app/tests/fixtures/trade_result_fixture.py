from datetime import date

import pytest


@pytest.fixture(
    params=[
        (
            {
                "oil_id": "INVALID",
                "delivery_type_id": "INVALID",
                "delivery_basis_id": "INVALID",
                "limit": "invalid_limit",
            },
            422,
        ),
        (
            {
                "oil_id": "OIL001",
                "delivery_type_id": "TYPE001",
                "delivery_basis_id": "BASIS001",
                "limit": -1,
            },
            500,
        ),
    ]
)
def invalid_trade_result_request(request):
    return request.param


@pytest.fixture(
    params=[
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
    ]
)
def trade_result_test_data(request):
    return request.param
