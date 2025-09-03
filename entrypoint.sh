#!/bin/bash
set -e

# Wait for Postgres to be ready
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done

# Run migrations
python manage.py makemigrations
python manage.py migrate --noinput

# create supersuser if not exists
# set all input as env var
python manage.py createsuperuser --noinput || true


# Run the passed command
exec "$@"
