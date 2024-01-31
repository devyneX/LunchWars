"""Celery configuration."""
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LunchWars.settings")
app = Celery("LunchWars")
app.conf.timezone = "Asia/Dhaka"
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "add-every-day": {
        "task": "wars.tasks.create_war",
        "schedule": crontab(hour=0, minute=0),
    },
}

app.autodiscover_tasks()
