import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'task_weekly_posts': {
        'task': 'NewsModels.tasks.task_weekly_posts',
        'schedule': crontab(day_of_week="mon", hour="08", minute="00"),
        'args': ()
    }
}