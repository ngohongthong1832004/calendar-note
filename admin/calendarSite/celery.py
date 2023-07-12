import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')

# Create an instance of the Celery application.
app = Celery('admin')

# Load the Celery configuration from your Django settings.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Optional: Load task modules from all registered Django app configs.
app.autodiscover_tasks()