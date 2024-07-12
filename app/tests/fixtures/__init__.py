from app.tests.fixtures.celery_fixture import mock_redis, mock_celery_event_loop
from app.tests.fixtures.dynamics_fixture import (
    dynamics_test_data,
    invalid_dynamics_data,
)
from app.tests.fixtures.add_data_fixture import (
    trade_result_test_add_data,
    invalid_trade_result_data,
)
from app.tests.fixtures.trade_result_fixture import (
    invalid_trade_result_request,
    trade_result_test_data,
)
from app.tests.fixtures.mock_aiohttp_fixture import mock_aiohttp_session
from app.tests.fixtures.fastapi_cache_fixture import fastapi_cache
from app.tests.fixtures.async_client_fixture import ac
from app.tests.fixtures.last_trading_dates_fixtures import (
    last_trading_dates_limit_test_data,
    last_trading_dates_test_data,
)
from app.tests.fixtures.get_link_fixture import expected_links, mock_html_content
from app.tests.fixtures.extract_report_data_fixture import mock_data, expected_result
