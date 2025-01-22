from celery import Celery
from celery.schedules import crontab
from services.cache_services import redis_client

from core.settings import config


celery_app = Celery(
    broker_url=config.celery_url,
    broker_connection_retry_on_startup=True,
    include=["core.celery_app"],
)

celery_app.conf.timezone = config.TIMEZONE


@celery_app.task
def clear_cache():
    redis_client.flushdb()


celery_app.conf.beat_schedule = {
    "clear-every-day": {
        "task": "core.celery_app.clear_cache",
        "schedule": crontab(hour=2, minute=13),  # type: ignore[arg-type]
    },
}
