#!/bin/bash

# Gunicorn
gunicorn --bind 0.0.0.0:8000 webapp.wsgi:application &

# Celery worker
celery -A webapp worker --loglevel=DEBUG --logfile=celery_worker.log &

# Celery beat
celery -A webapp beat --loglevel=DEBUG --logfile=celery_beat.log &

# Wait for all background processes to finish
wait