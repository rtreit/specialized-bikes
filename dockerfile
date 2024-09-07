FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql \
    rabbitmq-server \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get update \
    && apt-get install -y dos2unix \
    && apt-get install -y gcc \
    && apt-get install -y python3-dev \
    && apt-get install -y libpq-dev 

  
RUN if ! getent group rabbitmq > /dev/null 2>&1; then groupadd -g 105 rabbitmq; fi \
    && if ! id -u rabbitmq > /dev/null 2>&1; then useradd -u 105 -g 105 -M -s /sbin/nologin rabbitmq; fi

RUN mkdir -p /var/run/rabbitmq && chown -R rabbitmq:rabbitmq /var/run/rabbitmq

ENV PYTHONUNBUFFERED=1 \
    POSTGRES_USER=specialized \
    POSTGRES_DB=specialized_bikes \
    POSTGRES_HOST=localhost \
    POSTGRES_PORT=5432 \
    CELERY_BROKER_URL=amqp://specialized_celery_user:specialized!123@localhost:5672/myvhost


WORKDIR /app    

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

RUN rm -rf /var/lib/postgresql/15/main && \
    su postgres -c "/usr/lib/postgresql/15/bin/initdb -D /var/lib/postgresql/15/main"

RUN echo "local   all             postgres                                trust" > /etc/postgresql/15/main/pg_hba.conf && \
    echo "local   all             all                                     trust" >> /etc/postgresql/15/main/pg_hba.conf

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
# convert to UNIX format
RUN dos2unix /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# postgres
EXPOSE 5432 
# django
EXPOSE 8000
# celery
EXPOSE 5672 15672

USER root
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["python", "webapp/manage.py", "runserver", "0.0.0.0:8000"]
