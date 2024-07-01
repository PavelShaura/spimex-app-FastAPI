from redis import asyncio as aioredis

from app.config import settings
from worker.tasks import celery_event_loop, celery_app

redis = aioredis.from_url(settings.REDIS_HOST, encoding="utf8", decode_responses=True)


async def clear_cache():
    keys = redis.keys("fastapi-cache*")
    if keys:
        redis.delete(*keys)
    print("Cache cleared")


@celery_app.task
def start_periodic_task() -> None:
    """
    Запускает периодическую задачу.

    :return: None
    """
    celery_event_loop.run_until_complete(clear_cache())
    # Запуск:
    # celery -A worker.tasks:celery_app worker --loglevel=info &
    # celery -A worker.tasks:celery_app beat --loglevel=info
