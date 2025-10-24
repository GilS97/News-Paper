"""
Celery configuration for News Paper project.
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('newspaper')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Periodic tasks configuration
app.conf.beat_schedule = {
    'fetch-new-articles-every-hour': {
        'task': 'articles.tasks.fetch_new_articles',
        'schedule': crontab(minute=0),  # Every hour
    },
    'send-daily-emails': {
        'task': 'subscriptions.tasks.send_daily_digests',
        'schedule': crontab(hour=8, minute=0),  # Every day at 8:00 AM
    },
    'send-weekly-emails-monday': {
        'task': 'subscriptions.tasks.send_weekly_digests',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),  # Monday at 8:00 AM
    },
    'send-biweekly-emails': {
        'task': 'subscriptions.tasks.send_biweekly_digests',
        'schedule': crontab(hour=8, minute=0, day_of_week='1,4'),  # Monday and Thursday at 8:00 AM
    },
    'send-triweekly-emails': {
        'task': 'subscriptions.tasks.send_triweekly_digests',
        'schedule': crontab(hour=8, minute=0, day_of_week='1,3,5'),  # Monday, Wednesday, Friday at 8:00 AM
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
