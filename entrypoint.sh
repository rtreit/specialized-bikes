#!/bin/bash
set -e

if [ -z "$POSTGRES_PASSWORD" ]; then
  echo "ERROR: POSTGRES_PASSWORD is not set"
  exit 1
fi

service postgresql start

psql -U postgres -tc "SELECT 1 FROM pg_roles WHERE rolname='${POSTGRES_USER}'" | grep -q 1 || psql -U postgres -c "CREATE USER ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';"
psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname='${POSTGRES_DB}'" | grep -q 1 || psql -U postgres -c "CREATE DATABASE ${POSTGRES_DB};"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};"

psql -U postgres -d ${POSTGRES_DB} -c "GRANT ALL PRIVILEGES ON SCHEMA public TO ${POSTGRES_USER};"
psql -U postgres -d ${POSTGRES_DB} -c "ALTER USER ${POSTGRES_USER} CREATEDB;"

echo "local   all             postgres                                peer" > /etc/postgresql/15/main/pg_hba.conf
echo "local   all             ${POSTGRES_USER}                            md5" >> /etc/postgresql/15/main/pg_hba.conf
echo "host    all             all             127.0.0.1/32            md5" >> /etc/postgresql/15/main/pg_hba.conf
echo "host    all             all             ::1/128                 md5" >> /etc/postgresql/15/main/pg_hba.conf

service postgresql restart

python webapp/manage.py makemigrations
python webapp/manage.py migrate

exec "$@"
