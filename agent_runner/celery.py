from celery import Celery
from .config import task_config

celery = Celery(
    "agent_runner", broker="redis://localhost:6379/0", include=["agent_runner.tasks"]
)

celery.conf.task_serializer = "json"
celery.conf.timezone = "UTC"
celery.conf.beat_schedule = task_config

if __name__ == "__main__":
    celery.start()
