FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    POSTGRES_USER=specialized \
    POSTGRES_DB=specialized_bikes \
    POSTGRES_HOST=localhost \
    POSTGRES_PORT=5432

WORKDIR /app    

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app


RUN rm -rf /var/lib/postgresql/15/main && \
    su postgres -c "/usr/lib/postgresql/15/bin/initdb -D /var/lib/postgresql/15/main"

RUN echo "local   all             postgres                                trust" > /etc/postgresql/15/main/pg_hba.conf && \
    echo "local   all             all                                     trust" >> /etc/postgresql/15/main/pg_hba.conf

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 5432 8000

USER postgres
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["python", "webapp/manage.py", "runserver", "0.0.0.0:8000"]
