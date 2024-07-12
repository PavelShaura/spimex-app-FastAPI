import pytest


@pytest.fixture()
def mock_redis(mocker):
    return mocker.patch("app.worker.notify.redis")


@pytest.fixture
def mock_celery_event_loop(mocker):
    return mocker.patch("app.worker.notify.celery_event_loop")
