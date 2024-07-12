from datetime import date

import pytest


@pytest.fixture(
    params=[
        {
            "exchange_product_id": "DT50SUR065F",
            "exchange_product_name": "ДТ вид 4 (ДТ-А-К5) минус 50, ст. Сургут (ст. отправления)",
            "oil_id": None,
            "delivery_basis_id": None,
            "delivery_type_id": "F",
            "volume": 1000.0,
            "total": 100000.0,
            "count": 100,
            "date": date(2024, 7, 1),
        },
        {
            "exchange_product_id": "AI92REG066F",
            "exchange_product_name": "АИ-92 (АИ-92-К5), ст. Регион (ст. отправления)",
            "oil_id": "OIL002",
            "delivery_basis_id": "BASIS002",
            "delivery_type_id": "F",
            "volume": 2000.0,
            "total": 200000.0,
            "count": 200,
            "date": date(2024, 7, 2),
        },
    ]
)
def trade_result_test_add_data(request):
    return request.param


@pytest.fixture
def invalid_trade_result_data():
    return {
        "exchange_product_id": "INVALID",
        "exchange_product_name": "Invalid Product",
        "oil_id": "INVALID",
        "delivery_basis_id": "INVALID",
        "delivery_type_id": "INVALID",
        "volume": "invalid_volume",
        "total": "invalid_total",
        "count": "invalid_count",
        "date": "invalid_date",
    }
