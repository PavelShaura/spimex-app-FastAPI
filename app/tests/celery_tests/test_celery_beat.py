import asyncio

import pytest
from celery.schedules import crontab
from fastapi import HTTPException

from app.worker.tasks import celery_app
from app.worker.notify import start_periodic_task, clear_cache


@pytest.mark.usefixtures("mock_redis", "mock_celery_event_loop")
class TestCeleryTasks:

    def test_celery_beat_schedule(self):
        assert "clear-cache-every-day-at-14:11" in celery_app.conf.beat_schedule
        task = celery_app.conf.beat_schedule["clear-cache-every-day-at-14:11"]
        assert task["task"] == "worker.notify.start_periodic_task"
        assert isinstance(task["schedule"], crontab)
        assert task["schedule"].minute == {11}
        assert task["schedule"].hour == {14}

    @pytest.mark.asyncio(scope="session")
    async def test_clear_cache(self, mock_redis):
        mock_redis.keys.return_value = ["fastapi-cache:1", "fastapi-cache:2"]
        mock_redis.delete.return_value = 2

        await clear_cache()

        mock_redis.keys.assert_called_once_with("fastapi-cache*")
        mock_redis.delete.assert_called_once_with("fastapi-cache:1", "fastapi-cache:2")

    def test_start_periodic_task(self, mocker, mock_celery_event_loop):
        mock_clear_cache = mocker.patch(
            "app.worker.notify.clear_cache", return_value=None
        )
        start_periodic_task()
        mock_celery_event_loop.run_until_complete.assert_called_once()
        called_arg = mock_celery_event_loop.run_until_complete.call_args[0][0]
        assert asyncio.iscoroutine(called_arg)
        mock_clear_cache.assert_called_once()

    @pytest.mark.asyncio(scope="session")
    async def test_clear_cache_exception(self, mock_redis):
        mock_redis.keys.side_effect = HTTPException(
            status_code=500, detail="Redis connection error"
        )

        with pytest.raises(HTTPException) as exc_info:
            await clear_cache()

        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Redis connection error"
