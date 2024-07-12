from datetime import date, timedelta

import pytest


@pytest.fixture(
    params=[
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
    ]
)
def last_trading_dates_test_data(request):
    return request.param


@pytest.fixture(
    params=[
        (0, 422),
        (101, 422),
        (50, 200),
    ]
)
def last_trading_dates_limit_test_data(request):
    return request.param
