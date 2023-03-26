import os

from celery import Celery
#from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
#crontab(hour=17, minute=23, day_of_week=1),

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

#app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
#    'check_membership_expired-every-monday-morning': {
#        'task': 'core.utils.functions.check_membership_expired',
#        'schedule': crontab(minute='*/1'),
#    },
#}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
