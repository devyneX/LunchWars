"""Celery tasks for the wars app."""
from celery import shared_task
from . import models


@shared_task
def create_war():
    """Create a war."""
    models.War.objects.create()
