from datetime import date

import pytest


@pytest.fixture(
    params=[
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
    ]
)
def dynamics_test_data(request):
    return request.param


@pytest.fixture(
    params=[
        (
            {
                "oil_id": "INVALID",
                "delivery_type_id": "INVALID",
                "delivery_basis_id": "INVALID",
                "start_date": "invalid_date",
                "end_date": "invalid_date",
            },
            422,
        ),
        (
            {
                "oil_id": "OIL001",
                "delivery_type_id": "TYPE001",
                "delivery_basis_id": "BASIS001",
                "start_date": "2024-07-01",
                "end_date": "2024-06-30",
            },
            200,
        ),
    ]
)
def invalid_dynamics_data(request):
    return request.param
