#!/bin/bash
set -e

# Ensure POSTGRES_PASSWORD is set
if [ -z "$POSTGRES_PASSWORD" ]; then
  echo "ERROR: POSTGRES_PASSWORD is not set"
  exit 1
fi

# Run Django migrations
python manage.py makemigrations
python manage.py migrate

# Create Django superuser if the necessary environment variables are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
"
echo "Django superuser creation command executed."
fi

# Execute the CMD provided as argument (usually starts the application)
exec "$@"
