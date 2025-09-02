import os
from celery import Celery

# Make sure Django settings are loaded before Celery starts
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crawler_service.settings')

# Create a Celery app instance
app = Celery('crawler_service')

# Load config from Django settings (keys prefixed with "CELERY_")
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks.py files in all Django apps
app.autodiscover_tasks()
