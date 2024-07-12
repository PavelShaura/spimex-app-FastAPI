import pytest
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


@pytest.fixture(autouse=True, scope="function")
def fastapi_cache():
    FastAPICache.init(InMemoryBackend())
    yield
