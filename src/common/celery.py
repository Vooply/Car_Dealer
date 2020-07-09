import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('car_dealer')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'refresh-token-every-seven-days': {
        'task': 'refresh_dealer_tokens',
        'schedule': crontab(day_of_week=1),
    },
}
