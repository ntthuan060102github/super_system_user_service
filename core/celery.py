import os
from celery import Celery

from pkg_helpers.services.queue_name import USER_QUEUE

# celery -A core worker -l info --autoscale 3,10

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery(USER_QUEUE)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.task_default_queue = USER_QUEUE