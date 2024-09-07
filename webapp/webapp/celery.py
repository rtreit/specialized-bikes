import os
from celery import Celery
from time import sleep


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")

app = Celery('webapp')

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    return 'hello world'