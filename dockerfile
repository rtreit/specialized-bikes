# Base image
FROM python:3.12-slim

# Install PostgreSQL and other dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get update \
    && apt-get install -y dos2unix    

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    POSTGRES_USER=specialized \
    POSTGRES_DB=specialized_bikes \
    POSTGRES_HOST=localhost \
    POSTGRES_PORT=5432

# Set the working directory
WORKDIR /app    

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the application code
COPY . /app

RUN python webapp/manage.py collectstatic --noinput

# Initialize PostgreSQL database
RUN rm -rf /var/lib/postgresql/15/main && \
    su postgres -c "/usr/lib/postgresql/15/bin/initdb -D /var/lib/postgresql/15/main"

# Configure PostgreSQL to use trust authentication
RUN echo "local   all             postgres                                trust" > /etc/postgresql/15/main/pg_hba.conf && \
    echo "local   all             all                                     trust" >> /etc/postgresql/15/main/pg_hba.conf

# Copy and set up the entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN dos2unix /usr/local/bin/entrypoint.sh && chmod +x /usr/local/bin/entrypoint.sh

# Expose the necessary ports
EXPOSE 8000

# Switch to the postgres user
USER postgres

# Set the entrypoint to the custom script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

VOLUME /app/staticfiles

# Replace the CMD to use Gunicorn as the production server
# CMD ["python", "webapp/manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "--chdir", "/app/webapp", "--bind", "0.0.0.0:8000", "webapp.wsgi:application"]

