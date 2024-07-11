from typing import AsyncGenerator
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from app.main import app


@pytest.fixture()
def mock_redis(mocker):
    return mocker.patch("app.worker.notify.redis")


@pytest.fixture
def mock_celery_event_loop(mocker):
    return mocker.patch("app.worker.notify.celery_event_loop")


@pytest.fixture(autouse=True, scope="function")
def mock_aiohttp_session():
    with patch("aiohttp.ClientSession") as mock_session:
        yield mock_session


@pytest.fixture(autouse=True, scope="function")
def fastapi_cache():
    FastAPICache.init(InMemoryBackend())
    yield


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
