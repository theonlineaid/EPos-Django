#!/bin/bash

# Wait for PostgreSQL if needed (optional)
# echo "Waiting for postgres..."
# while ! nc -z db 5432; do
#   sleep 0.1
# done

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

exec "$@"
