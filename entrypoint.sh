#!/bin/bash
set -e

if [ -z "$POSTGRES_PASSWORD" ]; then
  echo "ERROR: POSTGRES_PASSWORD is not set"
  exit 1
fi

# postgres
# service postgresql start
# psql -U postgres -tc "SELECT 1 FROM pg_roles WHERE rolname='${POSTGRES_USER}'" | grep -q 1 || psql -U postgres -c "CREATE USER ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';"
# psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname='${POSTGRES_DB}'" | grep -q 1 || psql -U postgres -c "CREATE DATABASE ${POSTGRES_DB};"
# psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};"

# psql -U postgres -d ${POSTGRES_DB} -c "GRANT ALL PRIVILEGES ON SCHEMA public TO ${POSTGRES_USER};"
# psql -U postgres -d ${POSTGRES_DB} -c "ALTER USER ${POSTGRES_USER} CREATEDB;"

# echo "local   all             postgres                                peer" > /etc/postgresql/15/main/pg_hba.conf
# echo "local   all             ${POSTGRES_USER}                            md5" >> /etc/postgresql/15/main/pg_hba.conf
# echo "host    all             all             127.0.0.1/32            md5" >> /etc/postgresql/15/main/pg_hba.conf
# echo "host    all             all             ::1/128                 md5" >> /etc/postgresql/15/main/pg_hba.conf

# service postgresql restart

# # rabbit mq
# rabbitmq-plugins enable rabbitmq_management
# service rabbitmq-server start
# sleep 10
# rabbitmqctl add_user specialized_celery_user specialized!123
# rabbitmqctl set_user_tags specialized_celery_user administrator
# rabbitmqctl add_vhost myvhost
# rabbitmqctl set_permissions -p myvhost specialized_celery_user '.*' '.*' '.*'
# service rabbitmq-server restart

# django
python manage.py makemigrations
python manage.py migrate

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
"
echo "Django superuser creation command executed."
fi

exec "$@"
