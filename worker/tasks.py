import asyncio

from celery import Celery
from celery.schedules import crontab

from app.config import settings


celery_event_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()

celery_app: Celery = Celery(
    "celery",
    # broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
    # backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
    broker='redis://127.0.0.1:6379/0'
)

celery_app.autodiscover_tasks(["worker.notify"])


celery_app.conf.beat_schedule = {
    "clear-cache-every-day-at-14:11": {
        "task": "worker.notify.start_periodic_task",
        "schedule": crontab(minute="11", hour="14"),
    },
}

celery_app.conf.update(timezone="Europe/Moscow")
