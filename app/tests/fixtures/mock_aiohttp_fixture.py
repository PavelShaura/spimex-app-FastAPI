import pytest
from unittest.mock import patch


@pytest.fixture(autouse=True, scope="function")
def mock_aiohttp_session():
    with patch("aiohttp.ClientSession") as mock_session:
        yield mock_session
