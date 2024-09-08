#!/bin/bash
set -e

# Initialize the database if it doesn't exist
if [ ! -s "$PGDATA/PG_VERSION" ]; then
    echo "Initializing database..."
    initdb -D "$PGDATA"
fi

# Start PostgreSQL
exec su postgres -c "postgres"