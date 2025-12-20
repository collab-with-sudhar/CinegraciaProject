#!/bin/bash

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate

echo "Starting Gunicorn..."
gunicorn webproject.wsgi:application --bind=0.0.0.0:8000
