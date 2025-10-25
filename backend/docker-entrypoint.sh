#!/bin/bash
set -e

echo "=== Starting Django Application ==="

echo "Waiting for services to be ready..."
sleep 3

echo "Creating migrations..."
python manage.py makemigrations users
python manage.py makemigrations articles
python manage.py makemigrations subscriptions

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
